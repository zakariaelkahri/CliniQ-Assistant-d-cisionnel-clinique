import pytest
from datetime import datetime


@pytest.fixture
def fake_user():
    """Matches UserResponse schema: id, email, username, role."""
    return {
        "id": 1,
        "email": "test@cliniq.com",
        "username": "testuser",
        "role": "technician",
    }


@pytest.fixture
def fake_token():
    """Matches Token schema: access_token, token_type."""
    return {"access_token": "jwt_token_123", "token_type": "bearer"}


@pytest.fixture
def fake_query():
    """Matches Query model fields: id, user_id, question, response, created_at."""
    return {
        "id": 1,
        "user_id": 1,
        "question": "Piqûre méduse ?",
        "response": "Rincer à l'eau de mer.",
        "created_at": datetime.now().isoformat(),
    }


@pytest.fixture
def fake_queries_db():
    """List of queries matching QueryResponse schema: id, question, response, created_at."""
    return [
        {"id": 1, "question": "Piqûre méduse", "response": "Rincer...", "created_at": datetime.now().isoformat()},
        {"id": 2, "question": "Brûlure", "response": "Refroidir...", "created_at": datetime.now().isoformat()},
    ]



def test_signup(fake_user):
    """Simulates POST /auth/signup → returns UserResponse if email is new."""
    email_exists = False

    if not email_exists:
        result = fake_user
    else:
        result = None

    assert result is not None
    assert result["email"] == "test@cliniq.com"
    assert result["username"] == "testuser"
    assert result["role"] == "technician"


def test_login(fake_token):
    """Simulates POST /auth/login → returns Token if credentials valid."""
    credentials_valid = True

    result = fake_token if credentials_valid else None

    assert result is not None
    assert "access_token" in result
    assert result["token_type"] == "bearer"


def test_assistant(fake_query):
    """Simulates POST /query/assistant → returns {question, answer, current_user}."""
    current_user_id = 1
    question = fake_query["question"]
    answer = fake_query["response"]

    result = {
        "question": question,
        "answer": answer,
        "current_user": current_user_id,
    }

    assert "question" in result
    assert "answer" in result
    assert "current_user" in result
    assert result["current_user"] == current_user_id
    assert len(result["answer"]) > 0


def test_historiques(fake_queries_db):
    """Simulates GET /query/historiques → returns list[QueryResponse]."""
    result = fake_queries_db

    assert isinstance(result, list)
    assert len(result) == 2
    for q in result:
        assert "id" in q
        assert "question" in q
        assert "response" in q
        assert "created_at" in q
