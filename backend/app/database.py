from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
\
SQLALCHEMY_DATABASE_URL = "sqlite:///./sweetshop.db"
\
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
\
Base = declarative_base()
\
def init_db():
    from . import models
    \
    with engine.connect() as conn:
        \
        try:
            res = conn.execute("PRAGMA table_info(users)")
            cols = {row[1] for row in res.fetchall()}
            if "is_admin" not in cols:
                conn.execute("ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0")
            if "created_at" not in cols:
                conn.execute("ALTER TABLE users ADD COLUMN created_at DATETIME")
        except Exception:
            pass
        try:
            res = conn.execute("PRAGMA table_info(sweets)")
            cols = {row[1] for row in res.fetchall()}
            if "description" not in cols:
                conn.execute("ALTER TABLE sweets ADD COLUMN description VARCHAR")
            if "image_url" not in cols:
                conn.execute("ALTER TABLE sweets ADD COLUMN image_url VARCHAR")
            if "created_at" not in cols:
                conn.execute("ALTER TABLE sweets ADD COLUMN created_at DATETIME")
            if "updated_at" not in cols:
                conn.execute("ALTER TABLE sweets ADD COLUMN updated_at DATETIME")
        except Exception:
            pass
    Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
