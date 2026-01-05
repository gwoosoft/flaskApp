# JWT Authentication - cURL Examples

## Base URL
Assuming your Flask app runs on `http://localhost` (via nginx on port 80)

---

## 1. Register a Regular User (Public Endpoint)

This endpoint is public and always creates a user with role "user", even if you try to specify "admin".

```bash
curl -X POST http://localhost/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

**Response:**
```json
{
  "status": "ok",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Note:** Even if you try to include `"role": "admin"` in the request, it will be ignored and set to "user" for security.

---

## 2. Login as Regular User

```bash
curl -X POST http://localhost/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

**Response:**
```json
{
  "status": "ok",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

## 3. Get Current User Info (Protected Endpoint)

```bash
# Save the token from login/register response
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

curl -X GET http://localhost/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "status": "ok",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user"
  }
}
```

---

## 4. Setup First Admin User

**IMPORTANT:** Before you can create admin users via the API, you need to set up the first admin user using the setup script.

### Step 4a: Create the first admin user using setup script

Run the setup script inside your Docker container:

```bash
# Option 1: Using default credentials (admin@example.com / admin123)
docker exec -it <flask_container_name> python setup_admin.py

# Option 2: Using custom credentials
docker exec -it <flask_container_name> python setup_admin.py \
  --email admin@example.com \
  --password your_secure_password \
  --name "Admin User"
```

**Example output:**
```
==================================================
Admin User Setup Script
==================================================
Email: admin@example.com
Name: Admin User
==================================================

✅ Admin user created successfully!
   Email: admin@example.com
   Name: Admin User
   Role: admin
   ID: 1

==================================================
✅ Setup complete! You can now login with:
   Email: admin@example.com
   Password: admin123
==================================================
```

### Step 4b: Login as the admin user

```bash
curl -X POST http://localhost/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123"
  }'
```

Save the `access_token` from the response.

---

## 5. Create Additional Admin User (Admin-Only Endpoint)

Now that you have an admin user, you can create more admin users via the API:

### Step 5a: Create a new admin user using admin token

```bash
curl -X POST http://localhost/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123"
  }'
```

Save the `access_token` from the response.

### Step 4b: Create a new admin user using admin token

```bash
# Use the admin token from step 4a
ADMIN_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

curl -X POST http://localhost/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "name": "Admin User",
    "email": "admin2@example.com",
    "password": "admin456",
    "role": "admin"
  }'
```

**Response:**
```json
{
  "status": "ok",
  "user": {
    "id": 2,
    "name": "Admin User",
    "email": "admin2@example.com",
    "role": "admin"
  }
}
```

**Note:** If a regular user tries this, they'll get a 403 Forbidden error:
```json
{
  "error": "Admin access required",
  "code": "forbidden"
}
```

---

## 6. Create Regular User as Admin

Admins can also create regular users:

```bash
ADMIN_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

curl -X POST http://localhost/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com",
    "password": "password456",
    "role": "user"
  }'
```

---

## 7. Get User by ID (Protected Endpoint)

Any authenticated user can view other users:

```bash
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

curl -X GET http://localhost/users/1 \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "status": "ok",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user"
  }
}
```

---

## Error Examples

### Unauthorized (No Token)
```bash
curl -X GET http://localhost/auth/me
```
**Response:** 401 Unauthorized

### Forbidden (Regular User Trying Admin Action)
```bash
# Using a regular user token
REGULAR_USER_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

curl -X POST http://localhost/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $REGULAR_USER_TOKEN" \
  -d '{
    "name": "Test",
    "email": "test@example.com",
    "password": "test123",
    "role": "admin"
  }'
```
**Response:** 403 Forbidden - "Admin access required"

### Invalid Credentials
```bash
curl -X POST http://localhost/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "wrong@example.com",
    "password": "wrongpassword"
  }'
```
**Response:** 401 Unauthorized - "Invalid email or password"

---

## Quick Test Script

Save this as `test_api.sh`:

```bash
#!/bin/bash

BASE_URL="http://localhost"

echo "1. Registering regular user..."
REGISTER_RESPONSE=$(curl -s -X POST $BASE_URL/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "test123"
  }')

echo "$REGISTER_RESPONSE" | jq '.'

# Extract token (requires jq)
TOKEN=$(echo $REGISTER_RESPONSE | jq -r '.access_token')
echo -e "\nToken: $TOKEN\n"

echo "2. Getting current user info..."
curl -s -X GET $BASE_URL/auth/me \
  -H "Authorization: Bearer $TOKEN" | jq '.'
```

Make it executable: `chmod +x test_api.sh`



```
curl -X POST http://127.0.0.1:5000/create \
     -H "Content-Type: application/json" \
     -d '{"name": "Alice", "age": 17}'

# Using data.json

curl -X POST http://127.0.0.1:5000/create \
     -H "Content-Type: application/json" \
     -d @data.json


curl -X POST http://localhost/create \
     -H "Content-Type: application/json" \
     -d @data.json



curl -X POST http://localhost/users      -H "Content-Type: application/json"      -d '{"name": "Alice"}'

```

curl -X GET http://localhost/users/1

