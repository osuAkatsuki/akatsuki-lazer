from enum import Enum

class ApiHint(str, Enum):
    USERNAME_OR_PASSWORD_INCORRECT = "The username or password is incorrect."