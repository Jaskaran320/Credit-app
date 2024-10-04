# Credit-app

Credit-app is a simple backend-only CRUD application built using FastAPI for the backend, SQLAlchemy for ORM, Pydantic for data validation, Pytest for testing, and PostgreSQL for the database. It runs asynchronously using the Uvicorn ASGI server. Authentication is done using JWT.

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Jaskaran320/Credit-app.git
    cd credit-app
    ```

2. **Run the setup script:**

    ```bash
    python setup.py --dbname <name_of_postgres_db>
    ```

    By default, the database name is `credit_app`.

### What the Setup Script Does

1. Creates a Python virtual environment named `env`.
2. Installs the required packages mentioned in `requirements.txt`.
3. Creates a `.env` file with the required environment variables. The PostgreSQL username is set as `postgres` by   default. The user needs to set the password in the `DATABASE_URL` variable.
4. Creates the database with the name provided by the user.

### Running the Application

1. **Activate the virtual environment:**

    - For Windows:

        ```bash
        .\env\Scripts\activate
        ```

    - For Linux:

        ```bash
        source env/bin/activate
        ```

2. **Start the application:**

    ```bash
    uvicorn app.main:app --reload
    ```

    The application will be running at <a href="http:localhost:8000">`http:localhost:8000`</a>. The API documentation and interactive interface can be accessed at <a href="http:localhost:8000/api/docs">`http:localhost:8000/api/docs`</a>.

### Running Tests

To run the tests, execute the following command in the root directory:

```bash
pytest tests
```