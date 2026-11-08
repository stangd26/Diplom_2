import uuid

import allure

BASE_URL = "https://stellarburgers.education-services.ru/api"

REGISTER_ENDPOINT = f"{BASE_URL}/auth/register"
LOGIN_ENDPOINT = f"{BASE_URL}/auth/login"
DELETE_USER_ENDPOINT = f"{BASE_URL}/auth/user"
INGREDIENTS_ENDPOINT = f"{BASE_URL}/ingredients"
ORDERS_ENDPOINT = f"{BASE_URL}/orders"

DEFAULT_PASSWORD = "TestPassword123!"

# Возвращает данные нового пользователя
@allure.step("Подготовить данные уникального пользователя")
def unique_user_payload():
    unique_id = uuid.uuid4().hex

    return {
        "email": f"test_{unique_id}@example.com",
        "password": DEFAULT_PASSWORD,
        "name": f"TestUser_{unique_id}",
    }

# Формирует заголовок с access token
@allure.step("Сформировать заголовок авторизации")
def bearer_headers(access_token):
    return {
        "Authorization": access_token
        if access_token.startswith("Bearer ")
        else f"Bearer {access_token}"
    }
