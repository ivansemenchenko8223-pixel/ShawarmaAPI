# test_api.py
import requests
import json
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

BASE_URL = "http://localhost:1000/api/v1"

def print_section(title):
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_response(response):
    print(f"Статус: {response.status_code}")
    try:
        print("Ответ:", json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print("Ответ (не JSON):", response.text)

def ensure_admin_user():
    """Создаёт администратора, если его нет"""
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        print("Создаём администратора...")
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            is_admin=True
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print("✅ Администратор создан: admin / admin123")
    else:
        if not admin.is_admin:
            admin.is_admin = True
            db.commit()
            print(f"✅ Пользователь {admin.username} теперь администратор")
        else:
            print(f"✅ Администратор уже существует: {admin.username}")
    db.close()
    return "admin", "admin123"

def create_user(username, password, email=None):
    """Регистрирует нового пользователя через API"""
    if email is None:
        email = f"{username}@example.com"
    register_data = {
        "username": username,
        "password": password,
        "email": email
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print_response(response)
    return response

def login(username, password):
    """Логин и получение токена"""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": username, "password": password}
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"✅ Токен получен для {username}")
        return token
    else:
        print(f"❌ Ошибка логина для {username}")
        print_response(response)
        return None

def test_public_endpoints():
    """Тест публичных эндпоинтов (без токена)"""
    print_section("Тест публичных эндпоинтов")

    # GET /products/
    print("\n1. GET /products/ (список продуктов)")
    response = requests.get(f"{BASE_URL}/products/")
    print_response(response)

def test_protected_endpoints(token, username, is_admin=False):
    """Тест защищённых эндпоинтов с токеном"""
    print_section(f"Тест защищённых эндпоинтов (пользователь: {username}, admin={is_admin})")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # POST /products/ (создание продукта)
    print("\n2. POST /products/ (создание продукта)")
    product_data = {
        "name": f"Шаверма от {username}",
        "description": "Тестовое описание",
        "price": 250.00
    }
    response = requests.post(f"{BASE_URL}/products/", json=product_data, headers=headers)
    print_response(response)
    if response.status_code == 200:
        product_id = response.json()["id"]
        print(f"✅ Создан продукт с id={product_id}")
    else:
        print("❌ Не удалось создать продукт (возможно, недостаточно прав)", response.status_code)

    # POST /orders/order (создание заказа)
    print("\n3. POST /orders/order (создание заказа)")
    # Сначала нужно получить список продуктов, чтобы выбрать id
    products_resp = requests.get(f"{BASE_URL}/products/")
    if products_resp.status_code == 200:
        products = products_resp.json()
        if products:
            product_id = products[0]["id"]
            order_data = {
                "items": [{"product_id": product_id, "quantity": 2}]
            }
            response = requests.post(f"{BASE_URL}/orders/order", json=order_data, headers=headers)
            print_response(response)
            if response.status_code == 200:
                print("✅ Заказ создан")
            else:
                print("❌ Не удалось создать заказ")
        else:
            print("Нет продуктов для создания заказа. Сначала создайте продукт через админа.")
    else:
        print("Не удалось получить список продуктов")

def test_admin_operations(admin_token):
    """Дополнительные админские операции (например, обновление/удаление продукта)"""
    print_section("Дополнительные админские операции")
    headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json"
    }

    # Создаём продукт для дальнейших операций
    product_data = {
        "name": "Админский продукт",
        "description": "Для теста обновления",
        "price": 300.00
    }
    resp = requests.post(f"{BASE_URL}/products/", json=product_data, headers=headers)
    if resp.status_code != 201:
        print("Не удалось создать продукт для теста")
        return
    product_id = resp.json()["id"]
    print(f"Создан продукт id={product_id}")

    # PUT /products/{id}
    print("\n4. PUT /products/{id} (обновление)")
    update_data = {"name": "Обновлённый продукт", "price": 350.00}
    response = requests.put(f"{BASE_URL}/products/{product_id}", json=update_data, headers=headers)
    print_response(response)

    # DELETE /products/{id}
    print("\n5. DELETE /products/{id} (удаление)")
    response = requests.delete(f"{BASE_URL}/products/{product_id}", headers=headers)
    print(f"Статус: {response.status_code}")
    if response.status_code == 204:
        print("✅ Продукт удалён")
    else:
        print_response(response)

def main():
    # 1. Убедимся, что админ существует
    admin_username, admin_password = ensure_admin_user()

    # 2. Создаём тестового пользователя (если его нет)
    test_username = "testuser"
    test_password = "testpass"
    # Пытаемся зарегистрировать, если уже есть - проигнорируем ошибку
    print_section("Регистрация тестового пользователя")
    resp = create_user(test_username, test_password)
    if resp.status_code != 200:
        print("Возможно, пользователь уже существует, продолжаем...")

    # 3. Логинимся админом и получаем токен
    print_section("Логин администратора")
    admin_token = login(admin_username, admin_password)
    if not admin_token:
        print("Не удалось получить токен админа, выходим")
        return

    # 4. Тест публичных эндпоинтов (без токена)
    test_public_endpoints()

    # 5. Тест защищённых эндпоинтов админом (должно работать)
    test_protected_endpoints(admin_token, admin_username, is_admin=True)

    # 6. Дополнительные админские операции
    test_admin_operations(admin_token)

    # 7. Тест защищённых эндпоинтов обычным пользователем (должно быть 403)
    print_section("Логин обычного пользователя")
    user_token = login(test_username, test_password)
    if user_token:
        test_protected_endpoints(user_token, test_username, is_admin=False)
    else:
        print("Не удалось получить токен обычного пользователя")

if __name__ == "__main__":
    main()