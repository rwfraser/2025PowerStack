"""
Utility functions for managing conversation memory and checkpoints.
"""
import sqlite3
from typing import List, Dict

def list_all_threads(db_path: str = "checkpoints.db") -> List[str]:
    """List all conversation thread IDs in the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT DISTINCT thread_id FROM checkpoints")
        threads = [row[0] for row in cursor.fetchall()]
        return threads
    except sqlite3.OperationalError:
        return []
    finally:
        conn.close()

def delete_thread(thread_id: str, db_path: str = "checkpoints.db") -> bool:
    """Delete all checkpoints for a specific thread."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM checkpoints WHERE thread_id = ?", (thread_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.OperationalError:
        return False
    finally:
        conn.close()

def get_thread_stats(db_path: str = "checkpoints.db") -> Dict:
    """Get statistics about stored conversations."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT COUNT(DISTINCT thread_id) FROM checkpoints")
        thread_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM checkpoints")
        checkpoint_count = cursor.fetchone()[0]
        
        return {
            "total_threads": thread_count,
            "total_checkpoints": checkpoint_count
        }
    except sqlite3.OperationalError:
        return {"total_threads": 0, "total_checkpoints": 0}
    finally:
        conn.close()
