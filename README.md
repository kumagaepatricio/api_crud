# INE Test

Django/DRF Test project for INE

## Notes

- There is already a superuser "ine_admin" with password "ineadminpass" who can obtain a JWT token to create other users
- For this project I'm  using a Sqlite3 database, but in production projects I would use another database like Postgresql
- PATCH action has not been developed
- Auth method is JWT for apps and end users. Auth method between apps has not been developed but I would use OpenID

## Installation

Clone the project:

```bash
git clone https://github.com/kumagaepatricio/ine_test.git
```

Run:
```bash
docker-compose up --build
```




## Usage
To obtain a JWT access token make a POST request to /api/auth/token/ with "ine_admin" credentials (in this case I am running the app on http://127.0.0.1:8000)

```bash
curl -XPOST http://127.0.0.1:8000/api/auth/token/ -H "Content-Type: application/json" -d '{"username":"ine_admin", "password":"ineadminpass"}'
```
It will retrieve access and refresh tokens to use the app

```bash
{"refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1NDYwODc0MSwianRpIjoiMmE5ODY1ODgyZTEwNGZiOGIwNjMyYjkwNTY0NDdkOTEiLCJ1c2VyX2lkIjoxfQ.v1MRVUrYcAdcrjHxD_2WKXBRuzYDMjmjVWYYIxfEDMM","access":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU0NTIyNjQxLCJqdGkiOiJmNmZlMzU2MTI3N2Q0MWQxYmRlOGIyOTA0MjdiZDliOCIsInVzZXJfaWQiOjF9.j4qKruVKXTE911CfNABRwhGi2VnKDc5YC1a4V39cFS8"}
```

To use the app endpoints you will need to add an HTTP Authorization header with the access token received. It must be Bearer type

```bash
curl -XPOST http://127.0.0.1:8000/api/v1/users/ -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU0NTIyOTc4LCJqdGkiOiI5OGQ1MGFhZTM0M2Q0MjE0YWEzMTUxMTA1MGZjNzE1YyIsInVzZXJfaWQiOjF9.RCaj9tf8cbl7UWprqFKh05FggYqfITH1z--dx8XTERA" -d '{
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@ine.test",
    "password": "SuperSecurePasswd",
    "repeat_password": "SuperSecurePasswd",
    "groups": [
        "sales",
        "support",
    ]
}'
```

