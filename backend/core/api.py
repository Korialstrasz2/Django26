from datetime import datetime, timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from ninja import NinjaAPI
from ninja.errors import HttpError
from core.models import PlayerProfile
from core.schemas import (
    AuthMessageResponse,
    AuthUserResponse,
    HealthResponse,
    HelloResponse,
    LoginRequest,
    SignupRequest,
)

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


def _auth_user_response(user) -> AuthUserResponse:
    if not user.is_authenticated:
        return AuthUserResponse(username='', isAuthenticated=False, isMaster=False)

    profile = PlayerProfile.objects.filter(user=user).first()
    return AuthUserResponse(
        username=user.username,
        isAuthenticated=True,
        isMaster=bool(profile and profile.is_master),
    )


@api.get('/auth/me', response=AuthUserResponse)
def auth_me(request):
    return _auth_user_response(request.user)


@api.post('/auth/signup', response=AuthMessageResponse)
def auth_signup(request, payload: SignupRequest):
    if User.objects.filter(username=payload.username).exists():
        raise HttpError(400, 'username_gia_in_uso')

    user = User.objects.create_user(username=payload.username, password=payload.password)
    PlayerProfile.objects.create(user=user, is_master=payload.isMaster)
    login(request, user)
    return AuthMessageResponse(message='account_creato', user=_auth_user_response(user))


@api.post('/auth/login', response=AuthMessageResponse)
def auth_login(request, payload: LoginRequest):
    user = authenticate(request, username=payload.username, password=payload.password)
    if user is None:
        raise HttpError(401, 'credenziali_non_valide')

    login(request, user)
    return AuthMessageResponse(message='login_ok', user=_auth_user_response(user))


@api.post('/auth/logout', response=AuthMessageResponse)
def auth_logout(request):
    logout(request)
    return AuthMessageResponse(
        message='logout_ok',
        user=AuthUserResponse(username='', isAuthenticated=False, isMaster=False),
    )


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
