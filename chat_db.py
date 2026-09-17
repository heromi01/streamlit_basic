import sqlite3
import json
import os
from datetime import datetime

# ========================================================
# SQLite 대화 기록 데이터베이스 관리 모듈
# - 전체 세션 최대 10개 유지 (오래된 세션 자동 삭제 FIFO)
# - 세션당 최대 100개 대화(턴) 저장 제한 (사용자 질문 1 + AI 답변 1 = 1개)
# ========================================================
DB_PATH = "chat_history.db"
MAX_SESSIONS = 10              # DB에 저장 유지할 최대 세션 수 (10개)
MAX_TURNS_PER_SESSION = 100    # 한 세션당 허용되는 최대 대화 턴 수 (100개)

def get_connection(db_path=DB_PATH):
    """데이터베이스 연결 객체 반환"""
    # check_same_thread=False: Streamlit 멀티스레드 환경에서 안전하게 DB 연결 허용
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

def enforce_max_sessions(max_limit=MAX_SESSIONS, db_path=DB_PATH):
    """DB에 보관할 최대 세션 개수(10개) 초과 시 가장 오래된 세션부터 자동 삭제 (FIFO)"""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # 생성일시(created_at) 오름차순으로 모든 세션 조회 (오래된 순)
    cursor.execute("SELECT id FROM sessions ORDER BY created_at ASC")
    rows = cursor.fetchall()

    # 허용 개수(10개)를 초과하는 경우 초과분만큼 삭제 진행
    if len(rows) > max_limit:
        excess_count = len(rows) - max_limit
        oldest_sessions_to_delete = [r[0] for r in rows[:excess_count]]
        for old_id in oldest_sessions_to_delete:
            # 연관 메시지 및 세션 삭제
            cursor.execute("DELETE FROM messages WHERE session_id = ?", (old_id,))
            cursor.execute("DELETE FROM sessions WHERE id = ?", (old_id,))
        conn.commit()

    conn.close()

def get_all_sessions(db_path=DB_PATH):
    """저장된 모든 대화 세션 목록 최신순 조회 (최대 10개)"""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, created_at FROM sessions ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "title": row[1], "created_at": row[2]} for row in rows]

def create_session(session_id, title="새로운 대화", db_path=DB_PATH):
    """신규 대화 세션 생성 및 최대 10개 초과 시 FIFO 자동 삭제 적용"""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 세션 추가
    cursor.execute(
        "INSERT OR REPLACE INTO sessions (id, title, created_at) VALUES (?, ?, ?)",
        (session_id, title, now_str)
    )
    conn.commit()
    conn.close()

    # 세션 추가 후 10개 초과 여부 확인 및 오래된 세션 자동 정리
    enforce_max_sessions(max_limit=MAX_SESSIONS, db_path=db_path)

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

def get_session_turn_count(session_id, db_path=DB_PATH):
    """특정 세션의 대화 턴 수(사용자 질문 1회 + AI 답변 1회 = 1턴) 조회"""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    # 사용자가 작성한 질문 메시지(role='user') 개수를 세어 턴 수 계산
    cursor.execute(
        "SELECT COUNT(*) FROM messages WHERE session_id = ? AND role = 'user'",
        (session_id,)
    )
    turn_count = cursor.fetchone()[0]
    conn.close()
    return turn_count

def is_turn_limit_reached(session_id, max_turns=MAX_TURNS_PER_SESSION, db_path=DB_PATH):
    """세션의 대화 턴 수가 제한(100개)에 도달했는지 확인"""
    return get_session_turn_count(session_id, db_path=db_path) >= max_turns

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
        f"# 💬 대화 기록: {title}",
        f"- **세션 ID**: `{session_id}`",
        f"- **생성 일시**: {created_at}",
        f"- **총 메시지 수**: {len(messages)}개",
        "",
        "---",
        ""
    ]

    for idx, msg in enumerate(messages, 1):
        role_label = "👤 사용자" if msg["role"] == "user" else "🤖 AI 어시스턴트"
        md_lines.append(f"### {idx}. {role_label} `[{msg['created_at']}]`")
        md_lines.append("")
        md_lines.append(msg["content"])
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

    return "\n".join(md_lines)

# 모듈 로드 시 기본 DB 테이블 자동 초기화 및 세션 10개 초과 시 정리
init_db()
enforce_max_sessions()
