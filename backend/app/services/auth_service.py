from typing import Dict

users_db: Dict[str, dict] = {}


class AuthService:
    def signup(self, username, email, password):
        if email in users_db:
            raise ValueError("User already exists")

        users_db[email] = {
            "username": username,
            "email": email,
            "password": password,
        }

        return {"message": "User created"}

    def login(self, email, password):
        user = users_db.get(email)

        if not user or user["password"] != password:
            raise ValueError("Invalid credentials")

        return {"message": "Login successful", "user": user}