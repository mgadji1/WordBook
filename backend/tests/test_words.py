from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from app.main import app
from app.config import settings
from app.database.database import get_db


test_engine = create_async_engine(
    settings.DATABASE_URL,
    poolclass=NullPool
)


TestSession = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False
)


async def override_get_db():
    async with TestSession() as db:
        yield db


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


def test_get_all_words():
    response = client.get("/api/words")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_word():
    response = client.post(
        "/api/words",
        json={
            "word": "man",
            "translation": "мужчина"
        }
    )

    assert response.status_code == 201
    assert isinstance(response.json(), dict)
    assert response.json()["word"] == "man"
    assert response.json()["translation"] == "мужчина"


def test_get_specific_word():
    client.post(
        "/api/words",
        json={
            "word": "apple",
            "translation": "яблоко"
        }
    )

    response = client.get("/api/words/apple")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()["word"] == "apple"
    assert response.json()["translation"] == "яблоко"


def test_update_translation():
    client.post(
        "/api/words",
        json={
            "word": "hello",
            "translation": "привет"
        }
    )
    
    response = client.put(
        "/api/words/hello",
        json={
            "translation": "здравствуй"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()["word"] == "hello"
    assert response.json()["translation"] == "здравствуй"


def test_delete_word():
    client.post(
        "/api/words",
        json={
            "word": "butter",
            "translation": "масло"
        }
    )
    
    response = client.delete("/api/words/butter")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()["message"] == "Word deleted"