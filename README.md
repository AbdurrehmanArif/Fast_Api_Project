# FastAPI Auth + LLM API

A production-grade FastAPI backend with JWT authentication, single-session enforcement, and Google Gemini LLM integration.

---

## 🚀 Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Edit `.env` with your real values:

```env
SECRET_KEY=<generate with: python generate_secret.py>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./auth_app.db
GEMINI_API_KEY=<your key from https://aistudio.google.com/app/apikey>
```

### 3. Run the Server

```bash
uvicorn app.main:app --reload
```

> Tables are created automatically on first startup via SQLAlchemy.

### 4. Open Swagger UI

Navigate to **http://127.0.0.1:8000/docs**

---

## 📁 Project Structure

```
app/
├── main.py               ← FastAPI app entry point
├── database.py           ← SQLAlchemy engine + session
├── models.py             ← User ORM model
├── schemas.py            ← Pydantic request/response schemas
├── auth.py               ← JWT + session validation dependency
├── core/
│   ├── config.py         ← Settings (loaded from .env)
│   └── security.py       ← Password hashing + JWT utilities
└── routes/
    ├── auth_routes.py    ← POST /auth/signup, POST /auth/login
    ├── protected_routes.py ← GET /protected/me, GET /protected/dashboard
    └── llm_routes.py     ← POST /llm/ask-llm
```

---

## 🔐 API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/` | ❌ | Health check |
| POST | `/auth/signup` | ❌ | Register new user |
| POST | `/auth/login` | ❌ | Login → receive JWT |
| GET | `/protected/me` | ✅ | Get current user profile |
| GET | `/protected/dashboard` | ✅ | Sample protected data |
| POST | `/llm/ask-llm` | ✅ | Send prompt to Gemini |

---

## 🛡️ How Session Invalidation Works

Each login generates a fresh **`session_id`** (UUID v4) that is:
1. Stored in the `users.current_session_id` column in the database
2. Embedded inside the JWT payload alongside `sub` (user ID)

On every protected request, the backend:
1. Decodes the JWT → extracts `session_id`
2. Looks up the user in the database
3. **Compares** JWT `session_id` with `user.current_session_id`
4. If they **don't match** → returns `401 Session expired due to login from another device`

**Result**: Logging in from a new device immediately invalidates all previously issued tokens. Only one active session is possible at any time.

---

## 🤖 How LLM Integration Works

1. User logs in → receives JWT
2. Sends `POST /llm/ask-llm` with `Authorization: Bearer <token>` and a JSON body:
   ```json
   { "prompt": "Explain quantum computing in simple terms" }
   ```
3. Backend validates JWT + session, then calls **Google Gemini** (`gemini-1.5-flash`)
4. Returns:
   ```json
   { "response": "Quantum computing uses qubits that can be..." }
   ```

Error cases handled:
- `503` – Missing API key
- `502` – Gemini API error or empty response
- `504` – Request timeout

---

## 🧪 Test Sequence (Swagger UI)

1. `POST /auth/signup` → create account
2. `POST /auth/login` → copy the `access_token`
3. Click **Authorize** (top right) → paste token
4. `GET /protected/me` → see your profile ✅
5. `POST /auth/login` again (simulate new device login)
6. Use the **old token** with `GET /protected/me` → `401 Session expired` ✅
7. `POST /llm/ask-llm` with new token + any prompt ✅

---

## ⚙️ Database Migrations (Alembic)

For schema changes after initial deployment:

```bash
# Initialize (already done)
alembic init migrations

# Create a new migration after editing models.py
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```
