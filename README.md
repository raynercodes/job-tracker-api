# Job Tracker API

Summary:
  A backend API for managing and tracking job applications with companies featuring a secure user-owned applications and companies system. The API uses a Secure user authentication, row-level ownership enforcement, filtering, and application analytics.

Features:
- JWT-based authentication
- Refresh token rotation
- Company management
- Full CRUD for applications
- Filter application by status and company
- Application statistics by status
- Row-level ownership enforcement

Tech stack:
- Python
- Flask
- SQLite
- PyJWT
- Werkzeug

How to run:
- Install dependencies
- Run `python database.py`
- Run `python app.py`
- Test endpoints in Postman
- Use `Bearer Token` for protected routes in Postman


Design decisions:
### Service / Repository Separation
Separated business logic from database access by using service and repository layers with Routes to handle incoming requests and responses, services handle validation and Business logic, and repositories handle SQL database operations.

### Access Token Ownership using g.user_id
Protected routes decode the JWT access token and store the authenticated user ID in `g.user_id`. This prevents trusting user identity from client input and keeps ownership checks tied to the authenticated session system.

### Refresh Token Rotation
Refresh tokens are stored in the database and rotated on every refresh request. When a refresh token is used, it is revoked by setting `revoked_at` and replaced with a new one. This preserves token history and prevents reuse of old tokens.

### Ownership Checks In Queries
Every protected query filters by `user_id` so users can only access their own data. This enforces row-level security across the API.

### Filtered Applications Endpoint
The applications list endpoint supports optional query parameters such as `status` and `company_id`. This makes the API more flexible and closer to how a client would consume application data.

### Application Stats Aggregation
The stats endpoint uses grouped SQL aggregation to return counts of applications by status. This adds business insight beyond the basic CRUD operations.

Example endpoints:
 Auth:
   - POST /register
   - POST /login
   - POST /refresh

 Companies:
   - POST /companies
   - GET /companies

 Applications:
   - POST /applications
   - GET /applications
   - GET /applications/<id>
   - PATCH /applications/<id>
   - DELETE /applications/<id>
   - GET /applications/stats

Key Concepts Demonstrated:
- JWT authentication and refresh token rotation
- Layered architecture (routes, services, repositories)
- Row-level ownership enforcement
- Dynamic SQL filtering
- Aggregation queries for analytics
- Structured logging for debugging


Future Improvements:
- Add pagination to list endpoints
- Add update/delete routes for companies
- Move configuration secrets into environment variables
- Expand logging with request duration and status code
- Add automated tests