# 🛒 ShopSite — Django E-Commerce Platform

A full-featured, production-ready **e-commerce web application** built with Django, featuring complete user authentication, role-based access, shopping cart, and an admin dashboard with a clean Bootstrap 5 interface.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)

---

## ✨ Features

### 🔐 Authentication & Security
- User registration with email validation (prevents duplicate emails)
- Login/Logout with session management
- Password reset via email (token-based, expires in 24 hours)
- Password change for logged-in users
- Secure password hashing using Django's PBKDF2

### 👥 Role-Based Access
- **Two roles**: Customer & Admin
- Customers can browse, add to cart, checkout, and track orders
- Admins have full access to product management and order processing
- Custom decorators (`@login_required` + `@admin_required`)

### 🛍️ Store Features
- Product catalog with search functionality
- Detailed product pages with stock status
- Add to cart, quantity management, remove items
- Checkout with shipping address
- Order placement with automatic stock deduction
- Order history for customers

### 📊 Admin Dashboard
- Add, edit, and delete products (with image upload)
- View all orders and update statuses:
  - Pending → Processing → Shipped → Delivered → Cancelled

---

## 🛠️ Tech Stack

| Layer       | Technology                  |
|-------------|-----------------------------|
| Backend     | Django 4.2                  |
| Database    | SQLite (Development)        |
| Frontend    | Bootstrap 5 + Custom CSS    |
| Authentication | Django Auth + Custom Models |

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/kvsajith34/Codveda-Technologies.git
   cd Codveda-Technologies/A-Task1-Django_Web_Application

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # For Windows:
   venv\Scripts\activate
   # For macOS / Linux:
   source venv/bin/activate

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt

4. **Apply database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate

5. **Create a superuser (Admin account)**
   ```bash
   python manage.py createsuperuser

6. **Start the development server**
   ```bash
   python manage.py runserver

**Open your browser and go to:**
http://127.0.0.1:8000/

---

## 🌐 Application Routes

| Page | URL | Access |
|--------|--------|--------|
| Home / Products | `/` | Public |
| Product Detail | `/product/<slug>/` | Public |
| Cart | `/cart/` | Login Required |
| Checkout | `/checkout/` | Login Required |
| My Orders | `/orders/` | Login Required |
| Admin Dashboard | `/dashboard/` | Admin Only |
| Register | `/accounts/register/` | Public |
| Login | `/accounts/login/` | Public |

---

## ✨ Features

- ✅ User Registration & Authentication
- ✅ Secure Login & Logout
- ✅ Password Reset Functionality
- ✅ Role-Based Access Control (Customer & Admin)
- ✅ Product Listing & Product Detail Pages
- ✅ Shopping Cart with Quantity Management
- ✅ Checkout & Order Placement
- ✅ Order History for Customers
- ✅ Product Management via Admin Dashboard
- ✅ Order Status Tracking & Updates
- ✅ Responsive User Interface using Bootstrap 5
- ✅ SQLite Database Integration

---

## 🛠️ Tech Stack

### Backend
- Django

### Frontend
- Bootstrap 5
- HTML5
- CSS3

### Database
- SQLite

---

## 📂 Project Structure

```text
shopsite/

├── manage.py
├── requirements.txt
├── .env.example
├── shopsite/               # Project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/               # Auth app
│   ├── models.py           # Custom User with role field
│   ├── views.py            # Register, login, logout, profile, password flows
│   ├── forms.py
│   ├── urls.py
│   └── templates/accounts/
├── store/                  # E-commerce app
│   ├── models.py           # Product, Cart, CartItem, Order, OrderItem
│   ├── views.py            # Product, cart, checkout, orders, admin CRUD
│   ├── forms.py
│   ├── decorators.py       # @admin\_required
│   ├── context\_processors.py
│   └── templates/store/
└── templates/
&#x20;   └── base.html           # Shared layout with navbar and messages

```

---

## 🔐 User Roles

### Customer
- Browse Products
- Add Products to Cart
- Place Orders
- View Order History

### Admin
- Manage Products
- Update Order Status
- Monitor Orders
- Access Dashboard

---

## 📈 Future Enhancements

- Payment Gateway Integration
- Product Reviews & Ratings
- Wishlist Functionality
- Search & Filter System
- Email Notifications
- Inventory Management
- Coupon & Discount System

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**Venkata Sai Ajith**

