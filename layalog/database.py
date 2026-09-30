import os
import sqlite3
import json
from typing import List, Optional, Dict, Any
from pathlib import Path
from datetime import datetime
from layalog.models import AnalysisRecord, LogStats, ErrorIncident, GravityProfile, ProfileSnapshot
from layalog.profiles import get_builtin_profiles, get_default_profile

DB_PATH = Path(os.getenv("LAYALOG_DB_PATH", "layalog.db"))

def get_db_path() -> Path:
    return Path(os.getenv("LAYALOG_DB_PATH", "layalog.db"))

def init_db(db_path: Optional[Path] = None):
    if db_path is None:
        db_path = get_db_path()

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Table: analyses
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            created_at TEXT NOT NULL,
            total_lines INTEGER NOT NULL,
            stats_json TEXT NOT NULL,
            incidents_json TEXT NOT NULL,
            raw_log_text TEXT,
            file_path TEXT,
            profile_id TEXT,
            profile_snapshot_json TEXT
        )
    """)
    
    # Migration checks for columns in analyses
    for col, col_type in [("file_path", "TEXT"), ("profile_id", "TEXT"), ("profile_snapshot_json", "TEXT")]:
        try:
            cursor.execute(f"ALTER TABLE analyses ADD COLUMN {col} {col_type}")
        except sqlite3.OperationalError:
            pass

    # Table: profiles
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            system_context TEXT,
            criteria_baixa TEXT NOT NULL,
            criteria_media TEXT NOT NULL,
            criteria_critica TEXT NOT NULL,
            is_builtin INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    # Seed built-in profiles if not present or update their definitions
    for p in get_builtin_profiles():
        cursor.execute("""
            INSERT INTO profiles (id, name, description, system_context, criteria_baixa, criteria_media, criteria_critica, is_builtin, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name=excluded.name,
                description=excluded.description,
                system_context=excluded.system_context,
                criteria_baixa=excluded.criteria_baixa,
                criteria_media=excluded.criteria_media,
                criteria_critica=excluded.criteria_critica,
                is_builtin=1
        """, (
            p.id,
            p.name,
            p.description,
            p.system_context,
            p.criteria_baixa,
            p.criteria_media,
            p.criteria_critica,
            p.created_at or datetime.utcnow().isoformat(),
            p.updated_at or datetime.utcnow().isoformat()
        ))

    conn.commit()
    conn.close()

def get_profile(profile_id: str, db_path: Optional[Path] = None) -> Optional[GravityProfile]:
    db_path = db_path or get_db_path()
    init_db(db_path)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, description, system_context, criteria_baixa, criteria_media, criteria_critica, is_builtin, created_at, updated_at
        FROM profiles
        WHERE id = ?
    """, (profile_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return GravityProfile(
        id=row["id"],
        name=row["name"],
        description=row["description"] or "",
        system_context=row["system_context"] or "",
        criteria_baixa=row["criteria_baixa"],
        criteria_media=row["criteria_media"],
        criteria_critica=row["criteria_critica"],
        is_builtin=bool(row["is_builtin"]),
        created_at=row["created_at"],
        updated_at=row["updated_at"]
    )

def list_profiles(db_path: Optional[Path] = None) -> List[GravityProfile]:
    db_path = db_path or get_db_path()
    init_db(db_path)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, description, system_context, criteria_baixa, criteria_media, criteria_critica, is_builtin, created_at, updated_at
        FROM profiles
        ORDER BY is_builtin DESC, created_at ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [
        GravityProfile(
            id=r["id"],
            name=r["name"],
            description=r["description"] or "",
            system_context=r["system_context"] or "",
            criteria_baixa=r["criteria_baixa"],
            criteria_media=r["criteria_media"],
            criteria_critica=r["criteria_critica"],
            is_builtin=bool(r["is_builtin"]),
            created_at=r["created_at"],
            updated_at=r["updated_at"]
        ) for r in rows
    ]

def save_profile(profile: GravityProfile, db_path: Optional[Path] = None) -> GravityProfile:
    db_path = db_path or get_db_path()
    init_db(db_path)
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    created_at = profile.created_at or now
    updated_at = now

    cursor.execute("""
        INSERT INTO profiles (id, name, description, system_context, criteria_baixa, criteria_media, criteria_critica, is_builtin, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            name=excluded.name,
            description=excluded.description,
            system_context=excluded.system_context,
            criteria_baixa=excluded.criteria_baixa,
            criteria_media=excluded.criteria_media,
            criteria_critica=excluded.criteria_critica,
            updated_at=excluded.updated_at
    """, (
        profile.id,
        profile.name,
        profile.description or "",
        profile.system_context or "",
        profile.criteria_baixa,
        profile.criteria_media,
        profile.criteria_critica,
        1 if profile.is_builtin else 0,
        created_at,
        updated_at
    ))
    conn.commit()
    conn.close()
    profile.created_at = created_at
    profile.updated_at = updated_at
    return profile

def delete_profile(profile_id: str, db_path: Optional[Path] = None) -> bool:
    db_path = db_path or get_db_path()
    init_db(db_path)
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Check if profile is builtin
    cursor.execute("SELECT is_builtin FROM profiles WHERE id = ?", (profile_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False
    if row[0]:
        conn.close()
        raise ValueError("Cannot delete built-in profile.")

    cursor.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def save_analysis(record: AnalysisRecord, raw_text: str = "", file_path: str = "", db_path: Optional[Path] = None) -> str:
    db_path = db_path or get_db_path()
    init_db(db_path)
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    snapshot_json = record.profile_snapshot.model_dump_json() if record.profile_snapshot else None

    cursor.execute("""
        INSERT OR REPLACE INTO analyses (id, filename, created_at, total_lines, stats_json, incidents_json, raw_log_text, file_path, profile_id, profile_snapshot_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record.id,
        record.filename,
        record.created_at,
        record.total_lines,
        record.stats.model_dump_json(),
        json.dumps([inc.model_dump() for inc in record.incidents]),
        raw_text,
        file_path,
        record.profile_id,
        snapshot_json
    ))
    conn.commit()
    conn.close()
    return record.id

def list_analyses(limit: int = 50, db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    db_path = db_path or get_db_path()
    init_db(db_path)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, filename, created_at, total_lines, stats_json, profile_id, profile_snapshot_json
        FROM analyses
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    results = []
    for r in rows:
        stats = json.loads(r["stats_json"])
        snapshot = json.loads(r["profile_snapshot_json"]) if r["profile_snapshot_json"] else None
        results.append({
            "id": r["id"],
            "filename": r["filename"],
            "created_at": r["created_at"],
            "total_lines": r["total_lines"],
            "total_errors": stats.get("total_errors", 0),
            "critical_errors": stats.get("critical_errors", 0),
            "unavailability_rate": stats.get("unavailability_rate", 0.0),
            "profile_id": r["profile_id"],
            "profile_name": snapshot.get("profile_name") if snapshot else None
        })
    conn.close()
    return results

def get_analysis(analysis_id: str, include_raw: bool = False, db_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    db_path = db_path or get_db_path()
    init_db(db_path)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, filename, created_at, total_lines, stats_json, incidents_json, raw_log_text, profile_id, profile_snapshot_json
        FROM analyses
        WHERE id = ?
    """, (analysis_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
        
    snapshot = json.loads(row["profile_snapshot_json"]) if row["profile_snapshot_json"] else None

    return {
        "id": row["id"],
        "filename": row["filename"],
        "created_at": row["created_at"],
        "total_lines": row["total_lines"],
        "stats": json.loads(row["stats_json"]),
        "incidents": json.loads(row["incidents_json"]),
        "raw_log_text": (row["raw_log_text"] or "") if include_raw else None,
        "profile_id": row["profile_id"],
        "profile_snapshot": snapshot
    }

def get_analysis_lines(analysis_id: str, start_line: int = 1, limit: int = 200, db_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    db_path = db_path or get_db_path()
    init_db(db_path)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT total_lines, raw_log_text, file_path FROM analyses WHERE id = ?", (analysis_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None

    total_lines = row["total_lines"]
    file_path = row["file_path"] if "file_path" in row.keys() else None
    
    start_idx = max(0, start_line - 1)
    chunk: List[str] = []

    # Try reading from physical file if exists
    if file_path and Path(file_path).exists():
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                for idx, line in enumerate(f):
                    if idx >= start_idx:
                        chunk.append(line.rstrip("\r\n"))
                        if len(chunk) >= limit:
                            break
        except Exception:
            chunk = []

    # Fallback to database text
    if not chunk and row["raw_log_text"]:
        all_lines = row["raw_log_text"].splitlines()
        chunk = all_lines[start_idx : start_idx + limit]

    return {
        "analysis_id": analysis_id,
        "start_line": start_line,
        "limit": limit,
        "total_lines": total_lines,
        "lines": chunk
    }

def delete_analysis(analysis_id: str, db_path: Optional[Path] = None) -> bool:
    db_path = db_path or get_db_path()
    init_db(db_path)
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Retrieve file_path before deleting record
    cursor.execute("SELECT file_path FROM analyses WHERE id = ?", (analysis_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False

    file_path = row[0]
    if file_path:
        p = Path(file_path)
        try:
            if p.exists() and p.is_file():
                p.unlink(missing_ok=True)
        except Exception:
            pass

    # Safety cleanup for any associated files in uploads directory
    upload_dir = Path("uploads")
    if upload_dir.exists():
        for matched in upload_dir.glob(f"{analysis_id}_*"):
            try:
                if matched.is_file():
                    matched.unlink(missing_ok=True)
            except Exception:
                pass

    cursor.execute("DELETE FROM analyses WHERE id = ?", (analysis_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

