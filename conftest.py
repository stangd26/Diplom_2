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
    assert response.status_code == 200, (
        f"Не удалось получить ингредиенты: {response.status_code}, {response.text}"
    )
    body = response.json()
    assert body.get("success") is True
    ingredient_list = body.get("data", [])
    assert ingredient_list, "API вернул пустой список ингредиентов"
    return ingredient_list

# Создание и удаление тестового пользователя
@pytest.fixture
def user(session):
    with allure.step("Создать тестового пользователя"):
        payload = unique_user_payload()
        response = session.post(REGISTER_ENDPOINT, json=payload)

        assert response.status_code == 200, response.text

        body = response.json()
        test_user = {
            "payload": payload,
            "access_token": body["accessToken"],
        }

    yield test_user

    with allure.step("Удалить тестового пользователя"):
        session.delete(
            DELETE_USER_ENDPOINT,
            headers=bearer_headers(test_user["access_token"]),
        )

# Возвращает ID ингредиентов, пригодные для создания заказа
@pytest.fixture
def valid_ingredient_ids(ingredients):
    # Для валидного заказа достаточно одного или нескольких реальных ID.
    return [item["_id"] for item in ingredients[:2] if item.get("_id")]
