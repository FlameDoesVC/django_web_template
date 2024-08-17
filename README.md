# Shop Template Project

This is a Django-based e-commerce project.

## Prerequisites

- Python 3.x
- pip (Python package installer)
- virtualenv (optional but recommended)

## Setup

1. **Clone the repository:**

    ```sh
    git clone git@github.com:FlameDoesVC/django_web_template shop_template
    cd shop_template
    ```

2. **Create a virtual environment (optional but recommended):**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Apply the migrations:**

    ```sh
    python manage.py migrate
    ```

5. **Create a superuser:**

    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server:**

    ```sh
    python manage.py runserver
    ```

7. **Access the application:**

    Open your web browser and go to `http://127.0.0.1:8000/`.

## Project Structure

- `manage.py`: Django's command-line utility for administrative tasks.
- `shop/`: Main application directory.
	- `urls.py`: URL configuration.
	- `views.py`: Views for the application.
	- `models.py`: Models for the application.
	- `admin.py`: Admin panel configuration.
	- `templates/`: HTML templates.
	- `products/`: Static files (images for products).
	- `migrations/`: Database migrations.
- `shop_template/`: Project settings and configuration.
	- `settings.py`: Project settings and configuration.
- `requirements.txt`: List of dependencies.

## Additional Information

- **Admin Panel:** Access the admin panel at `http://127.0.0.1:8000/admin/` using the superuser credentials.
- **Static Files:** Ensure you have configured static files correctly for production.

For more information, refer to the [Django documentation](https://docs.djangoproject.com/en/stable/).