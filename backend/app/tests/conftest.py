\
import pytest
import sys, os
\
\
CURRENT_DIR = os.path.dirname(__file__)
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, engine
from app import models
from sqlalchemy.orm import sessionmaker
from app.database import Base
\
@pytest.fixture(scope="function")
def client():
    \
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
