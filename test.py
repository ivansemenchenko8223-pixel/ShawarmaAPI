#!/usr/bin/env python3
"""
Тестовый клиент для API магазина.
Выполняет запросы ко всем эндпоинтам: регистрация, логин, создание товара,
получение списка товаров, создание заказа.
"""

import requests
import random
import string

# Базовый URL API (измените при необходимости)
BASE_URL = "http://localhost:9000/api/v1"

def random_string(length=8):
    """Генерирует случайную строку из букв и цифр."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def test_api():
    # 1. Регистрация нового пользователя
    username = f"user_{random_string()}"
    email = f"{username}@example.com"
    password = "testpass123"
    
    register_data = {
        "username": username,
        "email": email,
        "password": password
    }
    
    print("1. Регистрация пользователя...")
    resp = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    if resp.status_code == 200:
        print("   Успешно:", resp.json())
    else:
        print(f"   Ошибка {resp.status_code}:", resp.text)
        return

    # 2. Логин (получение токена)
    print("\n2. Логин...")
    login_data = {
        "username": username,
        "password": password
    }
    resp = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if resp.status_code == 200:
        token = resp.json().get("access_token")
        print("   Токен получен")
    else:
        print(f"   Ошибка {resp.status_code}:", resp.text)
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 3. Создание продукта (требует авторизации)
    print("\n3. Создание продукта...")
    product_data = {
        "name": f"Тестовый товар {random_string(4)}",
        "description": "Описание товара",
        "price": 99.99
    }
    resp = requests.post(f"{BASE_URL}/products/", json=product_data, headers=headers)
    if resp.status_code == 200:
        product = resp.json()
        product_id = product.get("id")
        print(f"   Продукт создан, ID: {product_id}")
    else:
        print(f"   Ошибка {resp.status_code}:", resp.text)
        return

    # 4. Получение списка продуктов (без авторизации)
    print("\n4. Получение списка продуктов...")
    resp = requests.get(f"{BASE_URL}/products/", params={"offset": 0, "limit": 10})
    if resp.status_code == 200:
        products = resp.json()
        print(f"   Получено продуктов: {len(products)}")
        if products:
            print(f"   Первый продукт: {products[0].get('name')}")
    else:
        print(f"   Ошибка {resp.status_code}:", resp.text)

    # 5. Создание заказа (требует авторизации) с правильным форматом items
    print("\n5. Создание заказа...")
    order_data = {
        "items": [
            {
                "product_id": product_id,
                "quantity": 2
            }
        ]
    }
    resp = requests.post(f"{BASE_URL}/orders/order", json=order_data, headers=headers)
    if resp.status_code == 200:
        print("   Заказ создан:", resp.json())
    else:
        print(f"   Ошибка {resp.status_code}:", resp.text)

    print("\nТестирование завершено.")

if __name__ == "__main__":
    test_api()