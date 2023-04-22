import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from cakeshop.main import app
from cakeshop.dependencies import get_db
from cakeshop.db.base_class import Base
from cakeshop.db.models import *


SQLALCHEMY_TEST_DATABASE_URI = "sqlite:///test_cakeshop.db"
test_engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URI, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def fastapi_client():
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
