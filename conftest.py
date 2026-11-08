import pytest
import requests
import allure

from data import (
    REGISTER_ENDPOINT,
    DELETE_USER_ENDPOINT,
    INGREDIENTS_ENDPOINT,
    unique_user_payload,
    bearer_headers,
)

# Одна requests-сессия на тест
@pytest.fixture
def session():
    with requests.Session() as http:
        yield http

# Получает актуальные ID ингредиентов из API
@pytest.fixture
def ingredients(session):
    response = session.get(INGREDIENTS_ENDPOINT, timeout=15)
    return response.json().get("data", [])

# Создание и удаление тестового пользователя
@pytest.fixture
def user(session):
    payload = unique_user_payload()

    response = session.post(
        REGISTER_ENDPOINT,
        json=payload,
    )

    body = response.json()

    test_user = {
        "payload": payload,
        "response": response,
        "body": body,
        "access_token": body.get("accessToken"),
    }

    yield test_user

    # Очистка выполняется после завершения теста
    if test_user["access_token"]:
        session.delete(
            DELETE_USER_ENDPOINT,
            headers=bearer_headers(test_user["access_token"]),
        )

# Возвращает ID ингредиентов, пригодные для создания заказа
@pytest.fixture
def valid_ingredient_ids(ingredients):
    # Для валидного заказа достаточно одного или нескольких реальных ID.
    return [item["_id"] for item in ingredients[:2] if item.get("_id")]
