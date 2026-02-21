from datetime import datetime
from ninja import Schema


class HelloResponse(Schema):
    message: str
    server_time: datetime
    version: str


class HealthResponse(Schema):
    status: str
    uptime_hint: str


class SignupRequest(Schema):
    username: str
    password: str
    isMaster: bool = False


class LoginRequest(Schema):
    username: str
    password: str


class AuthUserResponse(Schema):
    username: str
    isAuthenticated: bool
    isMaster: bool


class AuthMessageResponse(Schema):
    message: str
    user: AuthUserResponse


class UserSettingsResponse(Schema):
    selectedStyleFolder: str
    availableStyleFolders: list[str]
    backgrounds: dict[str, str]


class UserSettingsUpdateRequest(Schema):
    selectedStyleFolder: str


class CacheClearResponse(Schema):
    message: str
