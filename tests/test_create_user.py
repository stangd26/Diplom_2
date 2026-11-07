import allure
import requests

from data import (
    REGISTER_ENDPOINT,
    DELETE_USER_ENDPOINT,
    unique_user_payload,
)


@allure.feature("Регистрация пользователя")
class TestCreateUser:

    @allure.title("Успешная регистрация уникального пользователя")
    @allure.description(
        "Проверяем регистрацию нового пользователя и получение токенов."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_unique_user_successfully(self, session):
        payload = unique_user_payload()

        with allure.step("Отправить запрос на регистрацию"):
            response = session.post(REGISTER_ENDPOINT, json=payload)

        with allure.step("Проверить успешный ответ"):
            assert response.status_code == 200

            body = response.json()
            assert body["success"] is True
            assert body["accessToken"]
            assert body["refreshToken"]
            assert body["user"]["email"] == payload["email"]

        with allure.step("Удалить созданного пользователя"):
            session.delete(
                DELETE_USER_ENDPOINT,
                headers={
                    "Authorization": body["accessToken"]
                },
            )

    @allure.title("Повторная регистрация существующего пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_already_registered_user_returns_error(self, session, user):
        with allure.step("Повторно зарегистрировать пользователя"):
            response = session.post(
                REGISTER_ENDPOINT,
                json=user["payload"],
            )

        with allure.step("Проверить ошибку повторной регистрации"):
            assert response.status_code == 403
            assert response.json()["message"] == "User already exists"

    @allure.title("Регистрация без обязательного поля")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_without_required_field_returns_error(self, session):
        payload = unique_user_payload()
        payload.pop("name")

        with allure.step("Отправить запрос без имени"):
            response = session.post(
                REGISTER_ENDPOINT,
                json=payload,
            )

        with allure.step("Проверить сообщение об ошибке"):
            assert response.status_code == 403
            assert (
                response.json()["message"]
                == "Email, password and name are required fields"
            )
