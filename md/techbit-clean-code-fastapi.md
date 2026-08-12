---
layout: page
---

# Clean Code in FastAPI

*A complete practical guide (beginner → expert) to writing clean, maintainable, production-grade FastAPI code.*

FastAPI makes it easy to build APIs quickly — but clean, scalable APIs require careful design. This guide details how to write clean, maintainable, production-grade FastAPI code, even in large systems. All examples use Python 3.10+ and FastAPI.

## 1. Project Structure: Organize for Scalability

A clean FastAPI application avoids dumping everything into `main.py`.

**Recommended project layout:**

```text
app/
│── main.py
│── api/
│   ├── v1/
│   │   ├── routers/
│   │   │   └── users.py
│   │   ├── dependencies/
│   │   │   └── auth.py
│   │   └── schemas/
│   │       └── user.py
│── core/
│   ├── config.py
│   ├── security.py
│── services/
│   └── user_service.py
│── repositories/
│   └── user_repository.py
│── models/
│   └── user.py
│── utils/
│   └── hashing.py
```

This is the core foundation of clean architecture for FastAPI.

## 2. Clean API Design: Keep Routers Slim

Routers should only contain:

- Endpoint declaration
- Input / output schema
- Calls to services
- Status codes
- Dependencies

**Bad — fat router:**

```python
@router.post("/users")
def create_user(user: UserCreate):
    hashed = bcrypt.hashpw(user.password, bcrypt.gensalt())
    db_user = User(name=user.name, password=hashed)
    session.add(db_user)
    session.commit()
    send_email(db_user.email)
    return db_user
```

**Good — thin router:**

```python
@router.post("/users", status_code=201)
def create_user(user: UserCreate, service: UserService = Depends()):
    return service.create_user(user)
```

> **Rule:** Routers orchestrate — services do the work.

## 3. Schemas (Pydantic): Be Explicit & Consistent

Use Pydantic models for:

- Input DTOs
- Output DTOs
- Internal validation
- Avoiding leaking DB models into HTTP responses

Keep input and output models separate:

```python
class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
```

**Never return ORM models directly.**

## 4. Services: Logic Belongs Here

Services contain:

- Business logic
- Validation
- Workflow steps
- Integration boundaries

```python
class UserService:

    def __init__(self, repo: UserRepository = Depends()):
        self.repo = repo

    def create_user(self, user: UserCreate):
        if self.repo.exists(user.email):
            raise EmailAlreadyExists()

        hashed = hash_password(user.password)

        return self.repo.create(
            email=user.email,
            password=hashed
        )
```

Clean, testable, isolated.

## 5. Repositories: Encapsulate Persistence

Repositories transform "database operations" into clean methods.

```python
class UserRepository:

    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def create(self, **kwargs):
        user = User(**kwargs)
        self.session.add(user)
        self.session.commit()
        return user

    def exists(self, email: str) -> bool:
        return self.session.query(User).filter_by(email=email).first() is not None
```

## 6. Dependencies: Powerful but Overused

Avoid injecting too much into routers directly.

**Bad:**

```python
@router.post("/items")
def add_item(item: Item, repo=Depends(UserRepository), config=Depends(get_config)):
```

**Good — inject the service only:**

```python
@router.post("/items")
def add_item(item: Item, service: ItemService = Depends()):
```

The service can internally use repositories, configs, external APIs, and security utilities.

## 7. Clean Naming in FastAPI

- Endpoints use resource names (plural): `/users`, `/orders`, `/payments/{payment_id}`
- Avoid noise words: `❌ /getUsers` → `✅ /users`
- Use descriptive function names:

```python
def create_user(...)
def list_users(...)
def update_user(...)
def deactivate_user(...)
```

## 8. Clean Error Handling

Define custom exceptions:

```python
class EmailAlreadyExists(Exception):
    pass
```

Use FastAPI exception handlers:

```python
@app.exception_handler(EmailAlreadyExists)
def email_exists_handler(request, exc):
    return JSONResponse(
        status_code=409,
        content={"detail": "Email already exists"}
    )
```

Avoid returning error messages manually.

## 9. Clean Validation

Prefer Pydantic validation to manual validation.

**Bad:**

```python
if not email or "@" not in email:
    raise HTTPException(400, "Invalid email")
```

**Good:**

```python
class UserCreate(BaseModel):
    email: EmailStr
```

## 10. Avoid Fat Models (The "Django Problem")

Models should represent data only, not behavior.

**Bad:**

```python
class User(Base):
    def send_welcome_email(self):
        ...
```

**Good — business logic in services:**

```python
class NotificationService:
    def send_welcome_email(self, user):
        ...
```

## 11. Avoid Common FastAPI Code Smells

- **Logic inside router** → move to services.
- **Returning ORM models** → use Pydantic response models.
- **Too many dependencies in endpoints** → inject the service only.
- **Big monolithic project** → use a modular structure.

## 12. Middleware: Keep It Simple

Middleware should only handle:

- Logging
- Authentication
- CORS
- Performance monitoring

Not business logic.

## 13. Configuration & Environment Variables

Use Pydantic Settings:

```python
class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

settings = Settings()
```

Avoid hard-coded values anywhere.

## 14. Response Models: Always Use Them

They prevent overexposing fields, leaking internals, and inconsistent responses.

```python
@router.get("/users/{id}", response_model=UserResponse)
```

## 15. Version Your API Cleanly

```text
app/api/v1/users.py
app/api/v2/users.py
```

Do not version by query params: `❌ /users?version=2`

## 16. Testing: Clean, Structured, Fast

Use `pytest` + `httpx` `TestClient` and the Arrange–Act–Assert pattern:

```python
def test_create_user(client):
    # Arrange
    payload = {"email": "a@b.com", "password": "1234"}

    # Act
    response = client.post("/v1/users", json=payload)

    # Assert
    assert response.status_code == 201
```

Test services separately, not only endpoints.

## 17. Performance & Clean Code Balance

Don't prematurely optimize. Write clean code → measure → optimize bottlenecks in:

- DB queries
- Serialization
- Overusing dependencies
- Duplicate queries

## 18. Async Clean Code Rules

- Use `async` when IO-bound: DB, HTTP calls, file operations.
- Avoid mixing sync and async freely.

**Bad:**

```python
async def foo():
    time.sleep(1)
```

**Good:**

```python
async def foo():
    await asyncio.sleep(1)
```

## 19. Dependency Over-Injection Anti-Pattern

Avoid injecting 5+ dependencies into each endpoint — consolidate them into Services.

## 20. Clean Architecture in FastAPI (Expert Level)

Use layered architecture:

```text
domain/         <-- business logic (pure Python)
use_cases/
adapters/
repositories/   <-- databases
api/            <-- FastAPI
```

Or "Hexagonal / Ports & Adapters": ports are interfaces (service contracts), adapters are the actual implementations (DB, API, etc.). This makes tests extremely easy.

## 21. Security: Clean, Secure, Production-Ready FastAPI

Writing clean code is not enough — it must also be secure code. FastAPI makes security features easy, but production-grade systems require a deeper approach across multiple layers: API, application, authentication, authorization, database, network, container, secrets, environment, and deployment pipelines.

### 21.1 API-Level Security

Use OAuth2 / JWT with FastAPI's built-in security:

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt(token)
    return payload["user_id"]
```

Avoid rolling your own crypto.

**Rate limiting** — FastAPI doesn't include it; use SlowAPI, an API Gateway (Traefik, NGINX, Kong, AWS API Gateway), or Cloudflare / edge WAF:

```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)
```

**Validate all input with Pydantic** — never trust incoming data:

```python
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
```

**Enforce HTTPS** — redirect all HTTP traffic to HTTPS at the load balancer or reverse proxy level.

**Sanitize outputs** — never expose ORM objects directly. Always use Pydantic response models to avoid leaking internal IDs, passwords, keys, or debug fields.

### 21.2 Authentication & Authorization

Use industry-standard protocols: OAuth2, JWT, OPA, Keycloak or Auth0, AWS Cognito.

Split the two concerns:

- **Authentication:** "Who are you?"
- **Authorization:** "What can you do?"

Role-based access control (RBAC):

```python
def require_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403, "Admins only")
```

Never store plain passwords — hash using bcrypt or argon2:

```python
# ❌ Never:
user.password = plaintext

# ✅ Correct:
user.password = hash_password(plaintext)
```

### 21.3 Application Security

- Avoid leaking stack traces in production: `DEBUG=False`, `RELOAD=False`, configure custom exception handlers.
- Limit large uploads — use `UploadFile` and set limits at the gateway level.
- Disable auto-generated docs in production:

```python
if env.is_production:
    app.docs_url = None
    app.redoc_url = None
```

- Avoid business logic inside JWT — it should contain minimal, non-sensitive claims.

### 21.4 Database Security

- Use least-privilege DB accounts — the API should not connect as a superuser (`❌ postgres/root` → `✅ api_user`).
- Always parameterize queries to avoid SQL injection:

```python
# ❌ Vulnerable:
session.execute(f"SELECT * FROM users WHERE email='{email}'")

# ✅ Safe:
session.execute(select(User).where(User.email == email))
```

- Encrypt data at rest: PostgreSQL TDE, MySQL InnoDB Encryption, MongoDB WiredTiger.
- Encrypt data in transit — always use TLS between API ↔ DB and services ↔ DB.
- Use separate read/write roles — avoid giving writes to read-only services.

### 21.5 Secrets Management

Never hard-code secrets:

```python
# ❌ Wrong:
SECRET_KEY = "my-secret"

# ✅ Correct: environment variables + Pydantic Settings
class Settings(BaseSettings):
    SECRET_KEY: str
```

Use secret managers — HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager — and rotate keys regularly.

### 21.6 Environment Security

- Separate environments: dev / staging / prod. Never mix configs.
- Production should use stricter validation, minimized logging, and disabled debug tools.
- Prevent `.env` files from leaking — add to `.gitignore`:

```text
.env
secrets/
```

- Don't log sensitive data (passwords, tokens, session cookies, PII) — use structured logs with filtering.

### 21.7 Network & Infrastructure Security

- Place FastAPI behind a reverse proxy: NGINX, Traefik, AWS ALB, Cloudflare Zero Trust. This adds rate limiting, TLS termination, caching, and WAF.
- Use a WAF (Web Application Firewall) — Cloudflare, AWS WAF, or Azure WAF — to block SQL injection, XSS, bots, and path traversal.
- Disable unused ports — expose only what's needed (typically 80 & 443 externally).
- Use VPC / private networks for the DB — never expose it publicly.
- Use mTLS for service-to-service communication, especially in microservices.

### 21.8 Container Security (Docker / Kubernetes)

- Use minimal base images:

```dockerfile
# ❌ Heavy and unsafe:
FROM python:3.10

# ✅ Better:
FROM python:3.10-slim
```

- Avoid running as root: `USER appuser`.
- Use multi-stage builds to reduce the attack surface.
- Keep dependencies pinned — lock versions in `requirements.txt`.
- Scan images for vulnerabilities: Trivy, Anchore, Snyk.
- Secure Kubernetes: network policies, limited service-account permissions, PodSecurity, avoid privileged containers.

### 21.9 CI/CD Pipeline Security

- Scan code for vulnerabilities: Bandit (Python), SonarQube, Snyk, Trivy.
- Protect CI secrets — use GitHub Actions encrypted secrets or vaults.
- Require approvals for production deploy — never allow direct commits to main.
- Automated dependency updates with safety checks — Renovate or Dependabot.

### 21.10 Observability & Monitoring Security

- Centralized structured logs — remove sensitive data.
- Audit trails — log login attempts, permission violations, admin actions.
- Alerting — trigger alerts for unusual traffic, high error rates, auth failures.

## Conclusion

Clean FastAPI code is:

- Modular
- Testable
- Scalable
- Consistent
- Business-driven
- Free of leaks between layers

Whether you're building a small microservice or a large enterprise API, these clean code patterns will make your FastAPI project more stable, maintainable, and friendly for new developers.
