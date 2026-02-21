from datetime import datetime, timezone
from django.conf import settings
from ninja import NinjaAPI
from ninja.errors import HttpError
from core.schemas import HelloResponse, HealthResponse

api = NinjaAPI(title='LAN Game API', version=settings.APP_VERSION)


@api.get('/hello', response=HelloResponse)
def hello(request):
    return HelloResponse(
        message='Hello LAN Player',
        server_time=datetime.now(tz=timezone.utc),
        version=settings.APP_VERSION,
    )


@api.get('/health', response=HealthResponse)
def health(request):
    return HealthResponse(status='ok', uptime_hint='process_alive')


@api.exception_handler(HttpError)
def on_http_error(request, exc: HttpError):
    return api.create_response(
        request,
        {'error': {'message': exc.message, 'status': exc.status_code}},
        status=exc.status_code,
    )


@api.exception_handler(Exception)
def on_unhandled_error(request, exc: Exception):
    return api.create_response(
        request,
        {'error': {'message': 'internal_server_error', 'detail': str(exc)}},
        status=500,
    )
