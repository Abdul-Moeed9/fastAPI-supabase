Secure Auth API

This is a simple authentication API I built using FastAPI and Supabase Auth.

It handles signup, login, logout, and a couple of protected routes that only work if you send a valid access token. Supabase takes care of storing passwords and signing tokens, so my code never touches raw passwords. All I'm doing is sending credentials to Supabase and checking the tokens it gives back.

Setup

Create a .env file in the project folder with the following:
SUPABASE_URL=your_project_url
SUPABASE_KEY=your_anon_key

You can get these from your Supabase project under Project Settings, then API. Use the anon key, not the service_role key.

Install the required packages:
pip install fastapi uvicorn python-dotenv supabase
Run the server:
uvicorn main:app --reload

The server runs at http://localhost:8000. Swagger docs are available at http://localhost:8000/docs, where you can click Authorize and paste a token to test the protected routes directly in the browser.

Endpoints

POST /auth/signup creates a new account. Returns 201 on success, 400 if email or password is missing.
POST /auth/login logs in an existing user and returns an access token and refresh token. Returns 401 if the credentials are wrong.
POST /auth/logout logs the user out. Needs a valid token. Returns 204 on success.
GET /public/info is open to anyone, no auth needed.
GET /protected/profile and GET /protected/dashboard both need a valid bearer token in the Authorization header. Return 401 if the token is missing, wrong, or expired.

All the protected routes use the same token-checking function, so I only wrote that logic once and reused it everywhere it's needed.
