import allure

from data import LOGIN_ENDPOINT


@allure.feature("Авторизация пользователя")
class TestLoginUser:

    @allure.title("Успешный вход зарегистрированного пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_existing_user_successfully(self, session, user):
        payload = user["payload"]

        with allure.step("Выполнить вход"):
            response = session.post(
                LOGIN_ENDPOINT,
                json={
                    "email": payload["email"],
                    "password": payload["password"],
                },
            )

        with allure.step("Проверить успешную авторизацию"):
            assert response.status_code == 200

            body = response.json()
            assert body["success"] is True
            assert body["accessToken"]
            assert body["refreshToken"]

    @allure.title("Вход с неверными учётными данными")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_incorrect_credentials_returns_error(
        self, session, user
    ):
        with allure.step("Отправить запрос с неверным паролем"):
            response = session.post(
                LOGIN_ENDPOINT,
                json={
                    "email": user["payload"]["email"],
                    "password": "WrongPassword123!",
                },
            )

        with allure.step("Проверить ошибку авторизации"):
            assert response.status_code == 401
            assert response.json()["message"] == (
                "email or password are incorrect"
            )
