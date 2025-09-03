import sqlite3

DB_NAME = "evidence_cases.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS evidence_cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            url TEXT,
            evidence_type TEXT,
            evidence_file BLOB,
            post_text TEXT,
            image_match_url TEXT,
            reason TEXT,
            additional_info TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_case(platform, url, evidence_type, evidence_file, post_text, image_match_url, reason, additional_info):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO evidence_cases 
        (platform, url, evidence_type, evidence_file, post_text, image_match_url, reason, additional_info)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (platform, url, evidence_type, evidence_file, post_text, image_match_url, reason, additional_info))
    conn.commit()
    conn.close()

# Initialize DB at import
init_db()
