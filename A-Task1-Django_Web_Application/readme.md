\# ShopSite — Django E-Commerce Web Application



A full-stack, production-minded e-commerce web application built with Django. Includes complete user authentication, role-based access control, a shopping cart and order system, and an admin dashboard — all rendered with clean Bootstrap 5 UI.



\---



\## Features



\### Authentication

\- User registration with validation (duplicate email check)

\- Login and logout with session management

\- Password reset via email (token-based, expires in 24 hours)

\- Password change for logged-in users

\- Secure password storage using Django's built-in PBKDF2 hashing



\### Roles \& Permissions

\- Two roles: \*\*Customer\*\* and \*\*Admin\*\*

\- Customers can browse products, manage their cart, place and view orders

\- Admins get a full dashboard to manage products and update order statuses

\- All protected views use `@login\_required` and a custom `@admin\_required` decorator



\### Store

\- Product listing page with keyword search

\- Product detail page with stock status

\- Add to cart, update quantity, remove items

\- Checkout with shipping address input

\- Order placement with automatic stock deduction

\- Order history page for customers



\### Admin Dashboard

\- Add, edit, and delete products (with image upload)

\- View all orders and update their status (Pending → Processing → Shipped → Delivered → Cancelled)



\---



\## Tech Stack



| Layer | Technology |

|-------|-----------|

| Backend | Django 4.2 |

| Database | SQLite (development) |

| Frontend | Bootstrap 5 + Bootstrap Icons |

| Auth | Django built-in auth system |

| Email | Console backend (dev) / SMTP (production) |

| Config | `django-environ` + `.env` file |

| Images | Pillow |



\---



\## Project Structure



```

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



\---



\## Getting Started



\### Prerequisites

\- Python 3.10 or higher

\- pip



\### Installation



\*\*1. Clone the repository\*\*

```bash

git clone https://github.com/kvsajith34/Codveda-Technologies.git

cd Codveda-Technologies/A-Task1-Django\_Web\_Application

```



\*\*2. Create and activate a virtual environment\*\*



macOS/Linux:

```bash

python -m venv venv

source venv/bin/activate

```



Windows:

```cmd

python -m venv venv

venv\\Scripts\\activate

```



\*\*3. Install dependencies\*\*

```bash

pip install -r requirements.txt

```



\*\*4. Set up environment variables\*\*



macOS/Linux:

```bash

cp .env.example .env

```



Windows:

```cmd

copy .env.example .env

```



Open `.env` and set your `SECRET\_KEY`. Generate one with:

```bash

python -c "from django.core.management.utils import get\_random\_secret\_key; print(get\_random\_secret\_key())"

```



\*\*5. Apply migrations\*\*

```bash

python manage.py migrate

```



\*\*6. Create a superuser (admin account)\*\*

```bash

python manage.py createsuperuser

```



\*\*7. Start the development server\*\*

```bash

python manage.py runserver

```



Visit: \*\*http://127.0.0.1:8000\*\*



\---



\## Email Configuration



\### Development (default)

Emails print to the terminal. No setup needed. Look for the reset link in your console output when `runserver` is running.



```env

EMAIL\_BACKEND=django.core.mail.backends.console.EmailBackend

```



\### Production (Gmail SMTP)

1\. Enable 2-Step Verification on your Google account

2\. Generate an \*\*App Password\*\* at myaccount.google.com → Security → App Passwords

3\. Update `.env`:



```env

EMAIL\_BACKEND=django.core.mail.backends.smtp.EmailBackend

EMAIL\_HOST=smtp.gmail.com

EMAIL\_PORT=587

EMAIL\_USE\_TLS=True

EMAIL\_HOST\_USER=you@gmail.com

EMAIL\_HOST\_PASSWORD=your-16-char-app-password

DEFAULT\_FROM\_EMAIL=ShopSite <you@gmail.com>

```



\### Testing (Mailtrap — no real inbox needed)

Sign up free at \[mailtrap.io](https://mailtrap.io) and paste your SMTP credentials into `.env`.



\---



\## Key URLs



| URL | Description |

|-----|-------------|

| `/` | Product listing |

| `/product/<slug>/` | Product detail |

| `/cart/` | Shopping cart |

| `/checkout/` | Place an order |

| `/orders/` | My order history |

| `/dashboard/` | Admin dashboard (admin only) |

| `/accounts/register/` | Register |

| `/accounts/login/` | Login |

| `/accounts/profile/` | Edit profile |

| `/accounts/password-reset/` | Forgot password |

| `/admin/` | Django admin panel |



\---



\## Environment Variables Reference



| Variable | Description | Default |

|----------|-------------|---------|

| `SECRET\_KEY` | Django secret key | \*(required)\* |

| `DEBUG` | Debug mode | `True` |

| `ALLOWED\_HOSTS` | Comma-separated hosts | `localhost,127.0.0.1` |

| `EMAIL\_BACKEND` | Email backend class | Console backend |

| `EMAIL\_HOST` | SMTP host | `smtp.gmail.com` |

| `EMAIL\_PORT` | SMTP port | `587` |

| `EMAIL\_USE\_TLS` | Use TLS | `True` |

| `EMAIL\_HOST\_USER` | SMTP username | — |

| `EMAIL\_HOST\_PASSWORD` | SMTP password | — |

| `DEFAULT\_FROM\_EMAIL` | Sender address | `noreply@shopsite.com` |



\---



\## Screenshots



> Register, login, product listing, cart, checkout, admin dashboard — all styled with Bootstrap 5.



\---



\## License



This project was built as part of the \*\*Codveda Technologies\*\* internship program.

