from datetime import datetime
from ninja import Schema


class HelloResponse(Schema):
    message: str
    server_time: datetime
    version: str


class HealthResponse(Schema):
    status: str
    uptime_hint: str
