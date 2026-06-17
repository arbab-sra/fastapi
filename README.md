
# FastAPI Project — Developer Guide

**Overview**

This is a small FastAPI project using Beanie (MongoDB), Motor, JWT auth, and `uvicorn` for the ASGI server.

**Prerequisites**

- Python 3.13 or newer
- Git
- (Optional) Docker & Docker Compose

**Install (local)**

1. Clone the repo and enter the folder:

   `git clone <repo-url> && cd fastapi`

2. Create and activate a virtual environment:

   macOS / Linux:

   `python -m venv .venv`

   `source .venv/bin/activate`

   Windows (PowerShell):

   `python -m venv .venv`  
    `.\.venv\Scripts\Activate.ps1`

3. Install dependencies (recommended: `uv`)

- Using `uv` (recommended):

  If your team uses the `uv` CLI for dependency management, use it as the primary workflow. Example commands (your `uv` version may differ; run `uv --help` if any command fails):

  - Install all project dependencies from the lock/project file:

    ```bash
    uv install
    ```

  - Add a new package and update project metadata/lock:

    ```bash
    uv add <package-name>
    ```

  - Update dependencies:

    ```bash
    uv update
    ```

  - Sync / install from lock (if your `uv` supports it):

    ```bash
    uv sync
    ```

- Using a virtual environment with `uv` (recommended):

  Create and activate a venv, then run `uv install` so packages are installed into the venv.

  macOS / Linux:

  ```bash
  python -m venv .venv
  source .venv/bin/activate
  uv install
  ```

  Windows (PowerShell):

  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  uv install
  ```

- Pip fallback (if you don't use `uv`):

  ```bash
  pip install -e .
  # or
  pip install bcrypt beanie fastapi[standard] motor passlib pyjwt python-dotenv uvicorn
  ```

**Environment**

The project loads environment variables with `python-dotenv`. Create a `.env` in the project root with at least the MongoDB connection string:

`DB_URL=mongodb://root:example@localhost:27017/`

Adjust the value to match your MongoDB server. The code initializes a database named `arbabsra` by default.

**Run (development)**

Start the server with `uvicorn` (the FastAPI app is defined in `main.py` as `app`):

`uvicorn main:app --reload --host 0.0.0.0 --port 8000`

Open the interactive API docs at: `http://localhost:8000/docs` (or `/redoc`).

**Run with Docker / Docker Compose**

If you prefer containers, build and run with Docker Compose:

`docker-compose up --build`

Or build the image and run directly:

`docker build -t fastapi-app .`  
`docker run -p 8000:8000 --env-file .env fastapi-app`

**Notes & Troubleshooting**

- The app's startup event calls `init_db()` to connect Beanie / Motor to MongoDB — ensure `DB_URL` is reachable.
- If you get dependency or build errors, confirm you are using Python 3.13+ and that your virtual environment is active.
- Use `pip install -e .` so the package metadata in `pyproject.toml` is used.

## API Endpoints & Responses

Here is the list of available API endpoints with their request formats and expected responses.

### 1. Root Endpoint
* **Path:** `/`
* **Method:** `GET`
* **Authentication:** None
* **Response (Success - `200 OK`):**
  ```json
  {
    "message": "Hello World"
  }
  ```

### 2. User Sign Up
* **Path:** `/signup`
* **Method:** `POST`
* **Authentication:** None
* **Request Body (JSON):**
  ```json
  {
    "name": "John Doe",
    "email": "johndoe@example.com",
    "password": "securepassword123"
  }
  ```
* **Responses:**
  * **Success (`200 OK`):**
    ```json
    {
      "message": "user created successfully User(id=ObjectId('...'), name='John Doe', email='johndoe@example.com', password='...')"
    }
    ```
  * **Failure (`400 Bad Request` - e.g., Email already exists):**
    ```json
    {
      "detail": "Email already exists"
    }
    ```

### 3. User Login
* **Path:** `/login`
* **Method:** `POST`
* **Authentication:** None
* **Request Body (JSON):**
  ```json
  {
    "email": "johndoe@example.com",
    "password": "securepassword123"
  }
  ```
* **Responses:**
  * **Success (`200 OK`):**
    * *Side effect:* Sets an HTTPOnly, SameSite=Lax cookie: `access_token=<JWT_TOKEN>`
    ```json
    {
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```
  * **Failure (`400 Bad Request` - e.g., User not found):**
    ```json
    {
      "detail": "user not found"
    }
    ```
  * **Failure (`401 Unauthorized` - Incorrect password):**
    ```json
    {
      "detail": "email or password is incorrect"
    }
    ```

### 4. User Profile
* **Path:** `/profile`
* **Method:** `GET`
* **Authentication:** Required (JWT token)
* **Authentication Methods:**
  * `Authorization` header (e.g. `Bearer <token>`)
  * `token` cookie
  * `token` query parameter (e.g. `?token=<token>`)
* **Responses:**
  * **Success (`200 OK`):**
    ```json
    {
      "_id": "667000572e92c2df9e5e7fa8",
      "name": "John Doe",
      "email": "johndoe@example.com",
      "password": "$2b$12$hashedpassword..."
    }
    ```
  * **Failure (`401 Unauthorized` - Invalid or missing token):**
    ```json
    {
      "detail": "Unauthorized token not found"
    }
    ```

**Relevant files**

- `main.py` — FastAPI app entrypoint
- `pyproject.toml` — declared dependencies
- `utility/connectDb.py` — DB initialization (reads `DB_URL`)
- `routes/auth.py` — authentication routes
- `controlar/usercontrolar.py` — authentication controllers/logic
- `middleware/authorized.py` — route authorization middleware
- `model/usermodle.py` — User Beanie document model
