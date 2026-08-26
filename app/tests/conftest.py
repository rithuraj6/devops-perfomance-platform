import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database import Base, get_db
from src.main import app


TEST_DATABASE_URL = "sqlite://"


engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)


TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture(scope="function")
def client(monkeypatch):
    Base.metadata.create_all(bind=engine)

    test_cache = {}

    def fake_get_cache(key: str):
        return test_cache.get(key)

    def fake_set_cache(
        key: str,
        value: str,
        ttl: int = 60,
    ):
        test_cache[key] = value

    def fake_delete_cache(key: str):
        test_cache.pop(key, None)

    monkeypatch.setattr(
        "src.routers.products.get_cache",
        fake_get_cache,
    )

    monkeypatch.setattr(
        "src.routers.products.set_cache",
        fake_set_cache,
    )

    monkeypatch.setattr(
        "src.routers.products.delete_cache",
        fake_delete_cache,
    )

    def override_get_db():
        db = TestingSessionLocal()

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

    Base.metadata.drop_all(bind=engine)
