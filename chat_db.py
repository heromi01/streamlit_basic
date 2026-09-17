import sqlite3
import json
import os
from datetime import datetime

# ========================================================
# SQLite 대화 기록 데이터베이스 관리 모듈
# ========================================================
DB_PATH = "chat_history.db"

def get_connection(db_path=DB_PATH):
    """데이터베이스 연결 객체 반환"""
    conn = sqlite3.connect(db_path, check_same_thread=False)
    return conn

def init_db(db_path=DB_PATH):
    """대화 세션 및 메시지 테이블 초기화 생성"""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # 1. 대화 세션 목록 테이블 (ID, 제목, 생성일시)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # 2. 세션별 메시지 내역 테이블 (ID, 세션ID, 발신자, 텍스트내용, 첨부이미지JSON, 첨부파일JSON, 생성일시)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            images_json TEXT,
            files_json TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()

def get_all_sessions(db_path=DB_PATH):
    """저장된 모든 대화 세션 목록 최신순 조회"""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, created_at FROM sessions ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "title": row[1], "created_at": row[2]} for row in rows]

def create_session(session_id, title="새로운 대화", db_path=DB_PATH):
    """신규 대화 세션 생성"""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT OR REPLACE INTO sessions (id, title, created_at) VALUES (?, ?, ?)",
        (session_id, title, now_str)
    )
    conn.commit()
    conn.close()

def update_session_title(session_id, title, db_path=DB_PATH):
    """대화 세션 제목 갱신 (첫 질문 내용으로 자동 축약 등)"""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE sessions SET title = ? WHERE id = ?",
        (title, session_id)
    )
    conn.commit()
    conn.close()

def get_session_messages(session_id, db_path=DB_PATH):
    """특정 세션의 모든 메시지 내역 시간순 조회"""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content, images_json, files_json, created_at FROM messages WHERE session_id = ? ORDER BY id ASC",
        (session_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        images = json.loads(row[2]) if row[2] else []
        files = json.loads(row[3]) if row[3] else []
        result.append({
            "role": row[0],
            "content": row[1],
            "images": images,
            "files": files,
            "created_at": row[4]
        })
    return result

def save_message(session_id, role, content, images=None, files=None, db_path=DB_PATH):
    """특정 세션에 신규 메시지 저장"""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    images_json = json.dumps(images) if images else None
    files_json = json.dumps(files) if files else None

    cursor.execute(
        "INSERT INTO messages (session_id, role, content, images_json, files_json, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (session_id, role, content, images_json, files_json, now_str)
    )
    conn.commit()
    conn.close()

def delete_session(session_id, db_path=DB_PATH):
    """특정 대화 세션 및 관련 메시지 삭제"""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()

def get_db_stats(db_path=DB_PATH):
    """전체 대화 세션 및 메시지 통계 조회"""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sessions")
    total_sessions = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM messages")
    total_messages = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM messages WHERE role = 'user'")
    user_messages = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM messages WHERE role = 'assistant'")
    assistant_messages = cursor.fetchone()[0]

    conn.close()
    return {
        "total_sessions": total_sessions,
        "total_messages": total_messages,
        "user_messages": user_messages,
        "assistant_messages": assistant_messages
    }

def get_daily_stats(db_path=DB_PATH):
    """일자별 메시지 발화량 통계 (날짜, 전체, 사용자, AI)"""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    query = """
        SELECT 
            substr(created_at, 1, 10) as msg_date,
            COUNT(*) as total_count,
            SUM(CASE WHEN role = 'user' THEN 1 ELSE 0 END) as user_count,
            SUM(CASE WHEN role = 'assistant' THEN 1 ELSE 0 END) as assistant_count
        FROM messages
        GROUP BY msg_date
        ORDER BY msg_date ASC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "date": r[0],
            "total": r[1],
            "user": r[2],
            "assistant": r[3]
        }
        for r in rows
    ]

def get_session_message_counts(db_path=DB_PATH):
    """세션별 메시지 수 상위 목록"""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    query = """
        SELECT s.id, s.title, s.created_at, COUNT(m.id) as msg_count
        FROM sessions s
        LEFT JOIN messages m ON s.id = m.session_id
        GROUP BY s.id, s.title, s.created_at
        ORDER BY msg_count DESC, s.created_at DESC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "title": r[1],
            "created_at": r[2],
            "msg_count": r[3]
        }
        for r in rows
    ]

def search_messages(keyword, db_path=DB_PATH):
    """키워드가 포함된 메시지와 해당 세션 정보 검색"""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    query = """
        SELECT m.id, m.session_id, s.title, m.role, m.content, m.created_at
        FROM messages m
        JOIN sessions s ON m.session_id = s.id
        WHERE m.content LIKE ?
        ORDER BY m.created_at DESC
    """
    cursor.execute(query, (f"%{keyword}%",))
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "session_id": r[1],
            "session_title": r[2],
            "role": r[3],
            "content": r[4],
            "created_at": r[5]
        }
        for r in rows
    ]

def export_session_markdown(session_id, db_path=DB_PATH):
    """특정 세션의 대화 내역을 마크다운 문서 형식 텍스트로 변환"""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT title, created_at FROM sessions WHERE id = ?", (session_id,))
    session = cursor.fetchone()
    if not session:
        conn.close()
        return ""

    title, created_at = session
    messages = get_session_messages(session_id, db_path=db_path)
    conn.close()

    md_lines = [
        f"# 대화 기록: {title}",
        f"- **세션 ID**: `{session_id}`",
        f"- **생성 일시**: {created_at}",
        f"- **총 메시지 수**: {len(messages)}개",
        "",
        "---",
        ""
    ]

    for idx, msg in enumerate(messages, 1):
        role_label = "👤 사용자 (User)" if msg["role"] == "user" else "🤖 AI 어시스턴트 (Assistant)"
        md_lines.append(f"### {idx}. {role_label} `[{msg['created_at']}]`")
        if msg.get("files"):
            md_lines.append(f"> **첨부 문서**: {', '.join(msg['files'])}")
        if msg.get("images"):
            md_lines.append(f"> **첨부 이미지 수**: {len(msg['images'])}개")
        md_lines.append("")
        md_lines.append(msg["content"])
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

    return "\n".join(md_lines)

# 모듈 로드 시 기본 DB 테이블 자동 초기화
init_db()
