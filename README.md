
## Setup

### Prerequisites
- Python 3.x
- Virtual environment tool (optional but recommended)

### Installation

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd insurance-portal-backend
    ```

2. **Create a virtual environment** (optional but recommended):
    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment**:
    - On Windows:
      ```sh
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```sh
      source venv/bin/activate
      ```

4. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

5. **Initialize the database**:
    ```sh
    python
    >>> from run import app
    >>> from app.extensions import db
    >>> with app.app_context():
    ...     db.create_all()
    ...     exit()
    ```

### Running the Application

1. **Run the application**:
    ```sh
    python run.py
    ```

2. **Access the application**:
    Open your web browser and go to `http://127.0.0.1:5000`.

## API Endpoints

- **GET /api/users/**: Retrieve all users.
- **GET /api/users/<user_id>**: Retrieve a specific user by ID.
- **POST /api/users/**: Create a new user.
- **PUT /api/users/<user_id>**: Update an existing user by ID.

## Running Tests

1. **Install `pytest`** (if not already installed):
    ```sh
    pip install pytest
    ```

2. **Run the tests**:
    ```sh
    pytest
    ```

## Project Structure Details

- **app/**: Contains the main application code.
  - **__init__.py**: Initializes the Flask app and extensions.
  - **config.py**: Contains configuration settings.
  - **extensions.py**: Initializes and configures extensions like SQLAlchemy.
  - **models/**: Contains SQLAlchemy models.
  - **routes/**: Contains route definitions.
  - **services/**: Contains business logic and service classes.
  - **utils/**: Contains utility functions and helpers.

- **tests/**: Contains test cases.
  - **__init__.py**: Makes the directory a package.
  - **test_users.py**: Contains unit tests for user routes.

- **migrations/**: Contains database migration files (if using Flask-Migrate).

- **run.py**: Entry point to run the application.
- **requirements.txt**: Lists project dependencies.
- **README.md**: Project documentation.