# 🛒 FoodMarket - Интернет-магазин продуктов питания

## 📌 Описание
Интернет-магазин продуктов питания с возможностью просмотра каталога, фильтрации товаров, добавления в корзину, оформления заказов и управления профилем.

## 📋 Содержание

- [Технологии](#технологии)
- [Клонирование репозитория](#-клонирование-репозитория)
- [Запуск проекта](#-запуск-проекта)
  - [Backend (Django + DRF)](#-backend-django--drf)
  - [Frontend (React + Vite)](#-frontend-react--vite)
- [API Эндпоинты](#-api-эндпоинты)
  - [Аутентификация](#-аутентификация-apiauth)
  - [Товары](#-товары-apiproducts)
  - [Категории](#-категории-apiproducts)
  - [Корзина](#-корзина-apicart)
  - [Заказы](#-заказы-apiorders)
- [Права доступа](#-права-доступа)
- [Структура проекта](#-структура-проекта)
- [Скриншоты программы](#-скриншоты-программы)
- [Автор](#-автор)

## 🛠 Технологии

| Часть проекта | Технологии |
|---------------|------------|
| Backend | Django, Django REST Framework, JWT (SimpleJWT), SQLite3, Django Filter, CORS |
| Frontend | React 18, React Router v6, Axios, Context API, Bootstrap 5 |
| Стили | Bootstrap, CSS3 |

## 🚀 Запуск проекта

### 📦 Клонирование репозитория

```bash
git clone https://github.com/ваш-логин/foodmarket.git
cd foodmarket
📂 Backend (Django + DRF)
bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # Создать админа
python manage.py runserver
📂 Frontend (React)
bash
cd frontend
npm install
npm start
🌐 API Эндпоинты
Базовый URL:
bash
http://localhost:8000/api/
📌 Аутентификация (/api/auth/)
Эндпункт	Метод	Описание	Доступ
/auth/register/	POST	Регистрация нового пользователя	Все
/auth/login/	POST	Авторизация (получение JWT-токенов: access и refresh)	Все
/auth/token/refresh/	POST	Обновление access-токена по refresh-токену	Авторизованные
/auth/profile/	GET	Получение данных профиля пользователя	Авторизованные
/auth/profile/	PUT/PATCH	Обновление данных профиля	Авторизованные
📌 Товары (/api/products/)
Эндпункт	Метод	Описание	Доступ
/products/	GET	Список всех опубликованных товаров (с пагинацией, фильтрацией, поиском)	Все
/products/	POST	Создание нового товара	Администратор
/products/{id}/	GET	Получение информации о товаре (увеличивает счётчик просмотров)	Все
/products/{id}/	PUT/PATCH	Обновление товара	Администратор
/products/{id}/	DELETE	Удаление товара	Администратор
/products/all/	GET	Все товары (включая неопубликованные)	Администратор
Параметры фильтрации для /products/:

Параметр	Тип	Описание	Пример
page	int	Номер страницы	?page=2
search	string	Поиск по названию или описанию	?search=хлеб
category	int	Фильтр по категории	?category=1
min_price	decimal	Минимальная цена	?min_price=50
max_price	decimal	Максимальная цена	?max_price=500
sort	string	Сортировка: price_asc, price_desc, newest, popular	?sort=price_asc
📌 Категории (/api/categories/)
Эндпункт	Метод	Описание	Доступ
/categories/	GET	Список всех категорий	Все
/categories/	POST	Создание новой категории	Администратор
/categories/{id}/	PUT/PATCH	Обновление категории	Администратор
/categories/{id}/	DELETE	Удаление категории	Администратор
📌 Корзина (/api/cart/)
Эндпункт	Метод	Описание	Доступ
/cart/	GET	Получение корзины пользователя	Авторизованные
/cart/add_item/	POST	Добавление товара в корзину	Авторизованные
/cart/update_item/	POST	Обновление количества товара в корзине	Авторизованные
/cart/remove_item/	POST	Удаление товара из корзины	Авторизованные
/cart/clear/	POST	Очистка корзины	Авторизованные
📌 Заказы (/api/orders/)
Эндпункт	Метод	Описание	Доступ
/orders/	GET	Список заказов пользователя (всех заказов для админа)	Авторизованные
/orders/	POST	Создание заказа из корзины	Авторизованные
/orders/{id}/	GET	Получение информации о заказе	Авторизованные
/orders/{id}/cancel/	POST	Отмена заказа	Авторизованные
/orders/{id}/update_status/	POST	Обновление статуса заказа	Администратор
🔐 Права доступа
Роль	Описание	Что может делать
Гость	Неавторизованный пользователь	Просматривать товары, категории, информацию о товарах
Пользователь	Авторизованный пользователь	Всё, что гость + добавлять в корзину, оформлять заказы, управлять профилем, просматривать свои заказы
Администратор	Пользователь с правами is_staff=True	Всё, что пользователь + управлять товарами, категориями, заказами, просматривать все заказы
📁 Структура проекта
text
foodmarket/
├── backend/                 # Django + DRF бэкенд
│   ├── config/              # Настройки Django
│   │   ├── settings.py
│   │   └── urls.py
│   ├── users/               # Приложение пользователей (JWT)
│   ├── products/            # Приложение товаров и категорий
│   ├── cart/                # Приложение корзины
│   ├── orders/              # Приложение заказов
│   ├── manage.py
│   └── requirements.txt
├── frontend/                # React фронтенд
│   ├── src/
│   │   ├── components/      # Переиспользуемые компоненты (Navigation, Footer, ProductFilter, Pagination)
│   │   ├── pages/           # Страницы приложения (Products, ProductDetail, Cart, Checkout, Orders, Profile, AdminPanel, Login, Register)
│   │   ├── contexts/        # Context API (AuthContext, CartContext)
│   │   ├── services/        # Axios и API запросы
│   │   ├── App.js
│   │   └── index.js
│   ├── public/
│   ├── package.json
│   └── .env.example
├── .gitignore
└── README.md