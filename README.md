# TMS Authentication (Login + JWT)

This is the login half of the TMS authentication task. It has a FastAPI backend
that checks credentials and issues a JWT, and a Streamlit frontend with a sign in
page and a protected dashboard.

Registration and the real dashboard are being built by the other team member, so
this repo has small placeholder versions of both that are easy to swap out later.

---

## 1. What you need installed

| Thing | Why |
|---|---|
| Python 3.10 or newer | Runs both halves of the project |
| The packages in `requirements.txt` | FastAPI, Uvicorn, PyJWT, Requests, Streamlit |

Everything else (the JSON user store, the password hashing) uses the Python
standard library, so there is nothing else to install or configure.

---

## 2. How to run it

You need **two terminals**, both opened in the project root (`E:\TMS`). One runs
the API, the other runs the UI. The UI cannot log anybody in if the API is not
running, because the UI never checks passwords itself.

### First time only

```bash
python -m venv myvenv
myvenv\Scripts\activate
pip install -r requirements.txt
python -m backend.repository.seed_users
```

That last line creates `backend/repository/users.json` with the three test
accounts. It is already done in this repo, but run it again any time you want to
reset the users or add one.

### Terminal 1, the backend

```bash
myvenv\Scripts\activate
uvicorn backend.mehar_main:app --reload
```

It starts on http://127.0.0.1:8000. Open http://127.0.0.1:8000/docs to see the
interactive API page, which is handy when you want to show the team lead the
endpoints without going through the UI.

`--reload` restarts the server whenever you save a file. Use it while developing,
drop it on a real server.

### Terminal 2, the frontend

```bash
myvenv\Scripts\activate
streamlit run frontend/login.py
```

It opens http://localhost:8501 in your browser.

### Test accounts

| Email | Password |
|---|---|
| mehr12@gmail.com | mehr12 |
| mehr22@gmail.com | mehr22 |
| mehr33@hotmail.com | mehr33 |

Any other email gets "Invalid email or password!", which is intentional and
explained in section 7.

---

## 3. Folder structure

```
TMS/
├── backend/
│   ├── mehar_main.py            FastAPI app, this is what uvicorn starts
│   ├── api/
│   │   └── client.py            HTTP calls the Streamlit pages make to the API
│   ├── repository/
│   │   ├── repo.py              Reads users out of storage
│   │   ├── seed_users.py        Creates users.json with hashed passwords
│   │   └── users.json           The three test users (passwords are hashed)
│   ├── routes/
│   │   └── mehar_routes.py      POST /auth/login and GET /auth/me
│   └── services/
│       └── auth.py              Password hashing, password checking, JWT
├── frontend/
│   ├── login.py                 Sign in page, also the app entry point
│   ├── dashboard.py             Protected page (placeholder)
│   ├── register.py              Registration placeholder
│   ├── config.py                Where the teammate's registration link goes
│   └── logo.png
├── myvenv/                      Virtual environment
├── requirements.txt
└── .env.example                 Template for the real secret key
```

The backend is split into four layers on purpose. Each layer only talks to the
one below it:

**routes → services → repository**, and `api/client.py` sits off to the side as
the thing the UI uses to reach the routes.

Why bother: if we move users from a JSON file to PostgreSQL, only `repo.py`
changes. If we switch password hashing, only `auth.py` changes. The routes and
the UI do not notice either time.

---

## 4. What each file does

### `backend/mehar_main.py`
Creates the FastAPI app, sets the title and version that show up on `/docs`, and
plugs in the router from `mehar_routes.py`. It also has a `GET /` health check so
you can confirm the server is alive.

This is the file uvicorn points at: `uvicorn backend.mehar_main:app`, which reads
as "in the module `backend.mehar_main`, use the variable called `app`".

### `backend/routes/mehar_routes.py`
The HTTP layer. It holds:

- **`LoginRequest`** and the other Pydantic models. These describe the exact shape
  of the request and the response. If the body does not match, FastAPI rejects it
  with 422 before our code runs.
- **`get_current_user`**, a dependency. Any route that adds
  `Depends(get_current_user)` becomes a protected route: it reads the
  `Authorization` header, verifies the token, and either hands back the user or
  raises 401.
- **`POST /auth/login`**, which calls the service and turns the answer into
  either 200 with a token or 401.
- **`GET /auth/me`**, the protected route the dashboard calls to prove the token
  is real.

### `backend/services/auth.py`
The brain. Nothing in here knows about HTTP or about Streamlit, which is why it
can be tested on its own.

- `hash_password` turns a plain password into a salted PBKDF2 hash.
- `verify_password` checks a typed password against a stored hash.
- `create_access_token` builds and signs the JWT.
- `decode_access_token` verifies a JWT and reads it back.
- `authenticate_user` is the actual login rule: find the user, check the
  password, return the user or `None`.

The secret key, the algorithm and the token lifetime are the three settings at
the top of this file. They read from environment variables with a development
fallback.

### `backend/repository/repo.py`
Opens `users.json` and finds a user by email, case insensitively (so
`MEHR12@Gmail.com` and `mehr12@gmail.com` are the same account). This is the only
file in the project that knows where user data physically lives.

### `backend/repository/seed_users.py`
A one off script that writes `users.json`. The `HASH_PASSWORDS` flag at the top
decides whether the passwords go in readable or hashed. Run it with
`python -m backend.repository.seed_users`. See section 7.

### `backend/api/client.py`
The other direction: this is the code the Streamlit pages use to call the API.
`login()` posts the credentials, `get_current_user()` sends the token to
`/auth/me`. Both return the raw response so the page can react to the status code.
The base URL lives here, so when the API gets deployed we change one line.

### `frontend/login.py`
The sign in form, plus a tiny router at the bottom that decides which page to
show based on `st.session_state["page"]`. Streamlit re-runs the whole script on
every interaction, so `session_state` is how the app remembers anything between
those re-runs.

### `frontend/dashboard.py`
The protected page. It does not simply trust that a token is sitting in the
session. On every load it calls `/auth/me` with that token, and shows the
dashboard only if the API answers 200.

### `frontend/register.py` and `frontend/config.py`
Placeholder registration page and the one setting that points at the real one.
See section 8.

---

## 5. How the whole thing connects

```
Browser
   │
   │  types email + password, clicks Sign In
   ▼
frontend/login.py ──────► backend/api/client.py ──► POST /auth/login
   ▲                                                      │
   │                                                      ▼
   │                                          routes/mehar_routes.py
   │                                                      │
   │                                          services/auth.py (check password)
   │                                                      │
   │                                          repository/repo.py (read users.json)
   │                                                      │
   │  { "access_token": "eyJ..." }  ◄────────────────────┘
   ▼
st.session_state["token"] = token
st.session_state["page"] = "dashboard"
   │
   ▼
frontend/dashboard.py ──► client.get_current_user(token) ──► GET /auth/me
                                                              (token verified)
                                                                    │
                          "Welcome to the dashboard, ..."  ◄────────┘
```

Step by step, what happens when someone signs in:

1. The user types an email and password and clicks **Sign In**.
2. `login.py` checks the obvious things first: nothing empty, and the email looks
   like an email. This is only to save a pointless network call. The server checks
   the same things again, because the server never trusts the client.
3. `client.login()` sends `POST /auth/login` with a JSON body.
4. FastAPI validates the body against `LoginRequest`. Bad email format or empty
   password stops here with **422**.
5. The route calls `authenticate_user()`.
6. That looks the email up through `repo.py`. No user, or a password that does
   not match the stored hash, and it returns `None`, which becomes **401**.
7. On a match, `create_access_token()` builds a JWT and the route answers **200**
   with the token.
8. `login.py` stores the token in `st.session_state`, flips the page to
   `"dashboard"` and calls `st.rerun()`.
9. `dashboard.py` takes that token and calls `GET /auth/me` with an
   `Authorization: Bearer <token>` header.
10. The `get_current_user` dependency verifies the signature and the expiry. If
    either fails the user is sent back to the login screen. If it passes, the
    dashboard renders with the email that came back from the API.

The important part for the team lead: **the dashboard is not protected by hiding
a page in the UI. It is protected because the data it needs comes from an
endpoint that refuses to answer without a valid token.**

---

## 6. How JWT works

JWT stands for JSON Web Token. It is a string in three parts separated by dots:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9 . eyJzdWIiOiJtZWhyMTJAZ21haWwuY29tIiwi... . cuBcPqiuTHtgaKnqVtZp3ijy...
        header                                    payload                              signature
```

- **Header** says which algorithm signed it. Ours is HS256.
- **Payload** carries the claims. We put in `sub` (the email, "subject" of the
  token), `name`, `iat` (issued at) and `exp` (expires at).
- **Signature** is the header and payload run through HMAC SHA256 with our secret
  key.

### The one thing people get wrong

A JWT is **signed, not encrypted**. The payload is base64, and anyone can paste
the token into jwt.io and read it. So never put a password or anything private in
it. What the signature guarantees is that the contents have not been changed,
because changing even one character of the payload makes the signature stop
matching.

### Why this means we do not need sessions on the server

The server does not store the token anywhere. When a request comes in, it
recalculates the signature using its secret key and compares. If it matches, the
token is genuine and the server can trust what is inside it. That is why the API
can stay stateless: restart it mid session and existing tokens still work.

### Expiry

`exp` is set 30 minutes ahead by default (`ACCESS_TOKEN_EXPIRE_MINUTES` in
`services/auth.py`). PyJWT checks it automatically on decode and raises
`ExpiredSignatureError`, which we turn into a 401 with the message "Session
expired, please sign in again". The dashboard catches that and sends the user back
to sign in.

### Why forged tokens fail

If someone builds their own token with our email in it but signs it with a
different secret, `jwt.decode` raises `InvalidTokenError` and they get a 401. The
whole scheme rests on the secret key staying secret, which is why it belongs in an
environment variable and not in git.

---

## 7. Passwords and error messages

### Two storage formats, on purpose

`verify_password` in `services/auth.py` accepts either of these:

```
mehr12                                      plain, what the demo users use today
pbkdf2_sha256$260000$a3f1...$9c2e...        algorithm, rounds, salt, hash
```

**Right now the demo accounts store the password as typed.** Registration is not
built yet, these three accounts exist only so login can be demonstrated, and short
readable passwords make that quicker for everyone on the team to test.

**The hashing path is already written and already works.** The moment registration
starts writing hashed passwords, login accepts them with no change to any file.
You can see it for yourself: set `HASH_PASSWORDS = True` in `seed_users.py`, re-run
it, and log in with the same passwords.

When a hash is stored, it is PBKDF2 with a random per user salt, so two people
with the same password still get different hashes, and nobody can read a password
back out of the file.

Either way the comparison uses `hmac.compare_digest` rather than `==`. A normal
comparison stops at the first different character, and that tiny timing difference
can leak information. `compare_digest` always takes the same time.

PBKDF2 was picked over bcrypt or Argon2 because it ships with Python, so there is
nothing extra to install on anyone's machine. bcrypt or Argon2 is the usual choice
in production.

**Before this handles a real user, `HASH_PASSWORDS` goes to `True` and stays
there.** Plain passwords are a testing shortcut and nothing more.

> If you paste the long `pbkdf2_sha256$...` string into the login form it will be
> rejected, which is correct. That string is the hash of the password, not the
> password.

### Why wrong password and unknown email give the same message

Both return 401 "Incorrect email or password". If an unknown email returned 404
"User not found", anybody could sit at the login page and work out which emails
are registered with us. That is called user enumeration and it is a real finding
in security reviews. The frontend still has a branch for 404 so it stays safe if
another endpoint ever uses it, but our login never sends one.

### Status codes used

| Code | When | What the user sees |
|---|---|---|
| 200 | Credentials correct | Redirected to the dashboard |
| 401 | Wrong password, unknown email, missing token, bad token, expired token | "Invalid email or password!" or the session expired message |
| 422 | Body failed validation (bad email format, empty password, missing field) | "Invalid request data!" |
| 500 | Something broke server side | "Server error, please try again in a moment." |

FastAPI produces the 422 on its own from the Pydantic model. We only raise the
401s by hand.

---

## 8. Where to paste your teammate's registration link

Open **`frontend/config.py`** and put the URL between the quotes:

```python
REGISTER_URL = "http://localhost:8502"
```

That is the only change needed. The sign in page picks it up and the line under
the form turns into a real link that says "Not registered yet? Register here".

While it is empty, the button opens the local placeholder in `register.py`
instead, so nothing breaks before you have the link.

---

## 9. Swapping in the other team member's pages

Both placeholders were written so their files can replace ours with no edits to
`login.py`.

**Dashboard:** replace `frontend/dashboard.py`. The only contract is a function
called `dashboard()` that takes no arguments. The token is waiting for it at
`st.session_state["token"]`, and it should send that token to the API as
`Authorization: Bearer <token>`, the way `client.get_current_user()` does.

**Register:** either point `REGISTER_URL` at their page, or replace
`frontend/register.py` with theirs keeping a function called `register()`.

If their registration writes users through the backend, it should hash passwords
with `hash_password()` from `services/auth.py` so the two halves agree on the
format. That is the single place our two tasks have to line up.

---

## 10. Before this goes anywhere near production

These are worth mentioning to the team lead so it is clear they were considered,
not missed:

1. **Set `HASH_PASSWORDS = True`.** The readable demo passwords are for testing
   this week only. The code path is already there and tested.
2. **Set a real `TMS_SECRET_KEY`.** The fallback in the code is a development
   value. Copy `.env.example` to `.env` and generate one with
   `python -c "import secrets; print(secrets.token_hex(32))"`.
3. **Move users into a database.** `repo.py` is the only file that changes.
4. **Serve over HTTPS.** A bearer token sent over plain HTTP can be read in
   transit.
5. **Add rate limiting on `/auth/login`** so nobody can sit there guessing
   passwords.
6. **Consider refresh tokens** if 30 minutes turns out to be too short in practice.

---

## 11. Quick troubleshooting

| Problem | Cause |
|---|---|
| "Could not reach the server" on sign in | The backend terminal is not running |
| `ModuleNotFoundError: No module named 'backend'` | You started uvicorn from inside the `backend` folder. Run it from the project root |
| Every login says invalid | `users.json` is missing. Run `python -m backend.repository.seed_users` |
| Logo does not show | `logo.png` was moved out of the `frontend` folder |
| Changes to backend code do nothing | You started uvicorn without `--reload` |
| localhost:8501 refuses to connect | Streamlit is sitting on its first run `Email:` prompt and has not started the server yet. Press Enter in that terminal to skip it. `.streamlit/config.toml` stops it asking again |
