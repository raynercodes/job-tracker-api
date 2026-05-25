# Job Tracker API

A backend REST API for managing job applications and companies, built with Python and Flask. Features secure JWT authentication, row-level data ownership, dynamic filtering, and application analytics.

---

## Live API

https://job-tracker-api-83da.onrender.com

---

## Features

- JWT authentication with access and refresh tokens
- Refresh token rotation and revocation
- Company management
- Full CRUD for job applications
- Filter applications by status and company
- Application statistics by status
- Row-level ownership enforcement
- Structured logging for debugging and request tracing

---

## Tech Stack

- Python
- Flask
- SQLite
- Docker
- PyJWT
- Werkzeug

---

## Project Structure

```
repos/
routes/
services/
utils/
app.py
database.py
db.py
config.py
Dockerfile
```

---

## How to Run

### With Docker
```bash
docker build -t job-tracker-api .
docker run -p 5001:5000 -e SECRET_KEY=your-secret-key job-tracker-api
```

### Manual Setup
```bash
pip install -r requirements.txt
python database.py
python app.py
```

---

## Authentication

```
POST /register
POST /login
POST /refresh
```

Use the access token from login in all protected route headers:
```
Authorization: Bearer <access_token>
```

---

## Company Endpoints

```
POST /companies
GET  /companies
```

---

## Application Endpoints

```
POST   /applications
GET    /applications
GET    /applications/<id>
PATCH  /applications/<id>
DELETE /applications/<id>
GET    /applications/stats
```

Filter applications by status or company:
```
GET /applications?status=applied
GET /applications?company_id=1
GET /applications?status=interview&company_id=2
```

---

## Example Application

```json
{
  "company_id": 1,
  "position": "Backend Developer",
  "status": "applied",
  "notes": "Applied through LinkedIn"
}
```

---

## Design Decisions

### Layered Architecture
Routes handle incoming requests and responses. Services handle validation and business logic. Repositories handle all SQL database operations. This separation keeps the codebase maintainable and each layer independently testable.

### Access Token Ownership via g.user_id
Protected routes decode the JWT and store the authenticated user ID in `g.user_id`. This prevents trusting user identity from client input and keeps ownership checks tied to the authenticated session.

### Refresh Token Rotation
Refresh tokens are stored in the database and rotated on every use. When a token is used it is revoked by setting `revoked_at` and replaced with a new one, preventing token reuse.

### Row-Level Security
Every protected query filters by `user_id` so users can only access their own data regardless of the resource ID passed in the request.

### Dynamic Filtering
The applications list endpoint supports optional `status` and `company_id` query parameters, making the API flexible and closer to how a real client would consume data.

### Stats Aggregation
The stats endpoint uses a grouped SQL `GROUP BY` query to return application counts by status, adding business insight beyond basic CRUD.

---

## Future Improvements

- Add pagination to list endpoints
- Add update/delete routes for companies
- Add automated tests

---

## Author

Leonardo Rayner