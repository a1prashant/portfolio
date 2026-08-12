---
layout: page
---

# Clean Code in Python

*A complete practical guide (beginner → expert) to writing code that is predictable, maintainable, extensible, and easy to reason about.*

Clean code isn't just about making programs work — it's about making them easy to read, maintain, and improve. Whether you're new to Python or an experienced developer, adopting clean coding habits will dramatically improve the quality of your codebase. Below are the essential principles, explained with Python-focused examples.

## 1. Naming: Write Code That Explains Itself

Use intention-revealing names — a variable name should answer *"what is this?"* and *"why does it exist?"*

```python
# ❌ Bad
x = 86400

# ✅ Good
SECONDS_PER_DAY = 86400
```

Avoid mental mapping — names should not require decoding:

```python
# ❌ Bad
def calc(r, t):
    return r * t

# ✅ Good
def calculate_total_price(rate, hours):
    return rate * hours
```

Use one word per concept — be consistent. If you use `get` somewhere, don't use `fetch`, `load`, or `retrieve` for the same purpose:

```python
# ❌ Inconsistent
def get_user(): ...
def fetch_account(): ...

# ✅ Consistent
def get_user(): ...
def get_account(): ...
```

Avoid unnecessary encoding in names — Python already handles types, so don't prefix names with types or contexts:

```python
# ❌ Bad
str_name = "Alice"
i_count = 10

# ✅ Good
name = "Alice"
count = 10
```

Make names pronounceable and searchable:

```python
# ❌ Bad
cln_dt = "2025-01-01"
s += h[j]

# ✅ Good
cleaned_date = "2025-01-01"
total_hours += hours[j]
```

Use domain language (ubiquitous language) — code should reflect the business domain:

```python
def calculate_premium(policy, risk_profile):
    ...
```

## 2. Functions: Small, Focused, Intuitive

A function must do **one thing**, at **one level of abstraction**. If it feels like it's doing "a bit of everything", split it.

```python
# ❌ Bad: too many responsibilities
def process_order(order):
    if not order["paid"]:
        raise ValueError("Not paid")
    update_inventory(order["items"])
    send_email(order["email"], "Order processed")
    log_to_file(order)
```

```python
# ✅ Good: split into clear, testable pieces
def validate_payment(order):
    if not order["paid"]:
        raise ValueError("Not paid")

def finalize_inventory(order):
    update_inventory(order["items"])

def notify_customer(order):
    send_email(order["email"], "Order processed")

def process_order(order):
    validate_payment(order)
    finalize_inventory(order)
    notify_customer(order)
```

Short functions are easier to read, debug, and reuse.

## 3. Fewer Arguments (Prefer 0–2)

Every argument increases cognitive load. Ideal: 0 arguments; good: 1–2; avoid 3+ unless necessary.

```python
# ❌ Bad — too many arguments
def create_user(name, age, email, phone, address):
    ...

# ✅ Good — group related data
def create_user(user_info):
    ...
```

Even better, use a dataclass:

```python
from dataclasses import dataclass

@dataclass
class UserInfo:
    name: str
    age: int
    email: str

def create_user(info: UserInfo):
    ...
```

Avoid boolean parameters — a boolean forces a function to do multiple things depending on its value:

```python
# ❌ Bad
def create_user(name, send_email=False):
    ...

# ✅ Split the responsibilities
def create_user(name):
    ...

def create_user_and_notify(name):
    user = create_user(name)
    notify(user)
```

## 4. Clear, Structured Error Handling

Use exceptions only for exceptional conditions:

```python
# ❌ Overusing exceptions
try:
    user = users[name]
except:
    user = "guest"

# ✅ Proper handling
user = users.get(name, "guest")
```

**Fail fast** — detect problems early, at the boundary of your system:

```python
def parse_age(value):
    if value < 0:
        raise ValueError("Age cannot be negative.")
    return value
```

Use custom exceptions for clarity:

```python
class InvalidOrderError(Exception):
    pass
```

## 5. Classes & Object Design

Keep classes small — a class should represent a single responsibility:

```python
# ❌ God class
class Order:
    def validate(self): ...
    def process_payment(self): ...
    def send_email(self): ...
    def print_invoice(self): ...

# ✅ Split by responsibility
class OrderValidator: ...
class PaymentProcessor: ...
class InvoicePrinter: ...
class OrderNotifier: ...
```

**Tell — don't ask.** Let the object decide instead of reaching into its state:

```python
# ❌ Bad
if user.is_admin:
    grant_access()

# ✅ Let the object decide
class User:
    def can_access(self):
        return self.role == "admin"
```

## 6. Modules & Project Structure

Keep modules cohesive — a module should contain closely related functions or classes.

Good module names: `billing.py`, `authentication.py`, `notifications.py`.
Bad module names: `utils.py`, `helpers.py`, `misc.py`.

Follow a consistent structure:

```text
project/
│── app/
│   ├── __init__.py
│   ├── models/
│   ├── services/
│   ├── controllers/
│── tests/
│── config/
│── main.py
```

## 7. Comments: Explain Why, Not What

The code should explain *what*; comments should explain *why*:

```python
# ❌ Bad — obvious
count += 1  # add 1 to count

# ✅ Good — reveals intent
# Retry count increments after transient failure
retry_count += 1
```

Replace comments with clearer code when possible:

```python
# ❌ Bad
# check if user is logged in
if session['user'] != None:

# ✅ Good
def is_logged_in(session):
    return session.get("user") is not None

if is_logged_in(session):
```

If you need a paragraph of comments to explain the logic, the code likely needs refactoring.

## 8. Avoid Code Smells & Repetition (DRY)

Avoid these smells:

- **Duplicate code** — refactor repeated logic into a single place.
- **Long functions** — break into smaller units.
- **Large classes** — split responsibilities.
- **Deeply nested logic** — flatten when possible.

```python
# ❌ Bad — duplicate logic
if user["role"] == "admin" and user["active"]:
    ...
if order["owner_role"] == "admin" and order["active"]:
    ...

# ✅ Good — extract a reusable check
def is_active_admin(entity):
    return entity["role"] == "admin" and entity["active"]

if is_active_admin(user):
    ...
if is_active_admin(order):
    ...
```

## 9. Reduce Complexity

Prefer clarity over cleverness:

```python
# ❌ Clever one-liner
return [x for x in data if x > 10 and x % 2 == 0]

# ✅ More readable
def is_valid(x):
    return x > 10 and x % 2 == 0

return [x for x in data if is_valid(x)]
```

Avoid magic numbers:

```python
# ❌ Bad
if x > 42:

# ✅ Good
MAX_RETRIES = 42
if x > MAX_RETRIES:
    ...
```

Flatten deeply nested logic:

```python
# ❌ Bad
if a:
    if b:
        if c:
            ...

# ✅ Good — early return
if not a or not b or not c:
    return
```

## 10. Immutability Where Possible

Avoid mutating input arguments:

```python
# ❌ Bad — mutates the input
def sanitize(user):
    user["name"] = user["name"].strip()

# ✅ Good — returns a new value
def sanitize(user):
    cleaned = user.copy()
    cleaned["name"] = cleaned["name"].strip()
    return cleaned
```

## 11. Clean Code Patterns (Python-Friendly)

**Strategy pattern using callables:**

```python
def pay_with_card(amount): ...
def pay_with_paypal(amount): ...

payment_methods = {
    "card": pay_with_card,
    "paypal": pay_with_paypal
}

payment_methods[user_choice](amount)
```

**Dataclasses for simple models:**

```python
@dataclass
class Product:
    id: int
    name: str
    price: float
```

**Context managers for resource handling:**

```python
with open("file.txt") as f:
    data = f.read()
```

## 12. Testing as Part of Clean Code

Clean code is easy to test. Use meaningful test names and the Arrange–Act–Assert pattern:

```python
def test_order_fails_when_inventory_is_empty(): ...

def test_discount_applies():
    # Arrange
    product = Product(price=100)

    # Act
    total = apply_discount(product, 0.1)

    # Assert
    assert total == 90
```

## 13. Refactoring Techniques

- **Extract function** — break long functions.
- **Extract class** — split large classes.
- **Inline temporary variables** — when unnecessary.
- **Replace conditionals with polymorphism** — instead of multiple `if` blocks.

## 14. Clean Architecture Principles (Advanced)

**Dependency rule:** inner layers must not depend on outer layers.

```text
domain/       <-- business logic
use_cases/
adapters/     <-- REST, CLI, DB
frameworks/   <-- Django, FastAPI
```

## 15. Consistency & Tooling

Follow a consistent style:

- `snake_case` for variables and functions
- `PascalCase` for classes
- `UPPER_CASE` for constants

```python
PI = 3.14

def calculate_area(radius):
    return PI * radius ** 2

class Circle:
    ...
```

Tools like `black`, `flake8`, or `ruff` maintain consistency automatically.

## Conclusion

Clean code isn't about perfection — it's about a mindset:

- Prefer clarity over cleverness
- Make everything intention-revealing
- Keep functions and classes small
- Reduce complexity
- Avoid repetition
- Make code testable
- Keep modules cohesive

Master these principles and your Python code becomes easier to understand, easier to change, easier to scale, and easier to test.
