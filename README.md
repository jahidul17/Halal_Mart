# 🛒 Halal Mart eCommerce API

**Project Description:** Halal Mart is a modern eCommerce platform designed to provide a seamless online shopping experience for customers seeking halal-certified products. The backend API is built to manage products, orders, carts, user accounts, reviews, and payments efficiently. The API ensures secure, fast, and scalable operations to support a full-featured online grocery store or food delivery service.

This project focuses on creating a robust and modular backend using Django REST Framework, enabling smooth interaction with any frontend (web, mobile apps) through well-documented API endpoints.

---
## 📄 Attached here are more details Document:

- [Functional Backend Requirements Document](https://docs.google.com/document/d/1FXxEKHWxtpDGKQPsrtQMkyKRpFqjVGCS2hWPBAVqZ2k/edit?usp=sharing)
- [Postman API Documentation](https://documenter.getpostman.com/view/37745715/2sB3WjxhyB)

---

## 🔑 Core Features

- **User Authentication & Management:** Secure registration, login, and profile management.
- **Product & Category Management:** CRUD operations for products, categories, and attributes.
- **Shopping Cart & Checkout:** Persistent cart, order creation, and checkout process.
- **Order Management:** Order tracking, status updates, and history.
- **Admin Dashboard:** Tools for managing users, products, and orders.
- **API Documentation:** Comprehensive Postman collection for seamless integration.

---

## ⚙️ Tech Stack

- **Backend:** Django, Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JWT or Token-based
- **API Documentation:** Postman

---


## Setup Instructions

1. **Clone the repository**
    ```bash
    git clone https://github.com/jahidul17/Halal_Mart
    cd Halal_Mart
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```


4. **Create a superuser (As admin login -Optional)**
    ```bash
    python manage.py createsuperuser
    ```


5. **Create a superuser (As admin login -Optional)**
Create .env file:
    ```bash
    EMAIL=Your_email
    EMAIL_PASSWORD=Email_generated_app_password_not_email_pass
    SECRET_KEY=your_secret_key
    DEBUG=True

    ```



5. **Apply migrations**
    ```bash
    python manage.py migrate
    ```

6. **Run the server**
    ```bash
    python manage.py runserver
    ```

7. **Access the project:**
    Open your browser and go to `http://127.0.0.1:8000/`<br>

---


