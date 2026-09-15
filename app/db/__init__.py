"""Database package.

The legacy SQLite helper is re-exported for older modules while the new
production-style backend uses SQLAlchemy via app.db.session.
"""

try:
    from app.legacy_sqlite_db import get_connection, init_db
except Exception:  # pragma: no cover - compatibility only
    get_connection = None
    init_db = None
