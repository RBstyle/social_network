from typing import List, Optional
from fastapi import Request


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get(
            "email"
        )  # since outh works on username field we are considering email as username
        self.password = form.get("password")

    async def is_valid(self):
        if not self.username or not (self.username.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False


class SignupForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.first_name: Optional[str] = None
        self.last_name: Optional[str] = None
        self.password1: Optional[str] = None
        self.password2: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.password1 = form.get("password1")
        self.password2 = form.get("password2")
        self.first_name = form.get("first_name")
        self.last_name = form.get("last_name")

    async def is_valid(self):
        if not self.username or not (self.username.__contains__("@")):
            self.errors.append("Email is required")
        if not self.first_name:
            self.errors.append("First name is required")
        if (
            self.password1
            and self.password2
            and self.password1 != self.password2
            or not len(self.password1) >= 4
        ):
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False
