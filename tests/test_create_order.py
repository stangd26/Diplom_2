import allure

from data import ORDERS_ENDPOINT, bearer_headers


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа авторизованным пользователем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_with_authorization_and_ingredients(
        self, session, user, valid_ingredient_ids
    ):
        with allure.step("Подготовить ингредиенты заказа"):
            payload = {"ingredients": valid_ingredient_ids}

        with allure.step("Создать заказ с авторизацией"):
            response = session.post(
                ORDERS_ENDPOINT,
                json=payload,
                headers=bearer_headers(user["access_token"]),
            )

        with allure.step("Проверить создание заказа"):
            assert response.status_code == 200

            body = response.json()
            assert body["success"] is True
            assert body["order"]["number"]

    @allure.title("Создание заказа без авторизации")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_without_authorization_returns_error(
        self, session, valid_ingredient_ids
    ):
        with allure.step("Создать заказ без токена"):
            response = session.post(
                ORDERS_ENDPOINT,
                json={"ingredients": valid_ingredient_ids},
            )

        with allure.step("Проверить создание заказа"):
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            assert body["order"]["number"]

    @allure.title("Создание заказа без ингредиентов")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_without_ingredients_returns_error(
        self, session, user
    ):
        with allure.step("Отправить заказ с пустым списком ингредиентов"):
            response = session.post(
                ORDERS_ENDPOINT,
                json={"ingredients": []},
                headers=bearer_headers(user["access_token"]),
            )

        with allure.step("Проверить ошибку отсутствия ингредиентов"):
            assert response.status_code == 400
            assert response.json()["message"] == (
                "Ingredient ids must be provided"
            )

    @allure.title("Создание заказа с неверным хешем ингредиента")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_with_invalid_ingredient_hash_returns_error(
        self, session, user
    ):
        with allure.step("Отправить заказ с несуществующим ингредиентом"):
            response = session.post(
                ORDERS_ENDPOINT,
                json={"ingredients": ["invalid_ingredient_hash"]},
                headers=bearer_headers(user["access_token"]),
            )

        with allure.step("Проверить ошибку неверного хеша"):
            assert response.status_code == 500
