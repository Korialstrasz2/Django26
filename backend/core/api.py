from datetime import datetime, timezone
from pathlib import Path
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from ninja import NinjaAPI
from ninja.errors import HttpError
from core.models import PlayerProfile, UserSettings
from core.schemas import (
    AuthMessageResponse,
    AuthUserResponse,
    CacheClearResponse,
    HealthResponse,
    HelloResponse,
    LoginRequest,
    SignupRequest,
    UserSettingsResponse,
    UserSettingsUpdateRequest,
)

api = NinjaAPI(title='LAN Game API', version=settings.APP_VERSION)

STYLE_BACKGROUND_FILES = {
    'diario': 'BGDiario.jpg',
    'menu': 'BGMenu.jpg',
    'dadi': 'BGDadi.jpg',
}


def _styles_base_dir() -> Path:
    return Path(settings.MEDIA_ROOT) / 'Immagini' / 'backgrounds' / 'stili'


def _get_available_style_folders() -> list[str]:
    base_dir = _styles_base_dir()
    if not base_dir.exists() or not base_dir.is_dir():
        return []

    return sorted([item.name for item in base_dir.iterdir() if item.is_dir()])


def _build_style_background_urls(style_folder: str) -> dict[str, str]:
    urls: dict[str, str] = {}
    if not style_folder:
        return urls

    for section, filename in STYLE_BACKGROUND_FILES.items():
        urls[section] = (
            f"{settings.MEDIA_URL}Immagini/backgrounds/stili/{style_folder}/{filename}"
        )
    return urls


def _auth_user_response(user) -> AuthUserResponse:
    if not user.is_authenticated:
        return AuthUserResponse(username='', isAuthenticated=False, isMaster=False)

    profile = PlayerProfile.objects.filter(user=user).first()
    return AuthUserResponse(
        username=user.username,
        isAuthenticated=True,
        isMaster=bool(profile and profile.is_master),
    )


def _require_authenticated_user(request) -> User:
    if not request.user.is_authenticated:
        raise HttpError(401, 'autenticazione_richiesta')
    return request.user


def _user_settings_response_for(user: User) -> UserSettingsResponse:
    settings_obj, _ = UserSettings.objects.get_or_create(user=user)
    available = _get_available_style_folders()

    if settings_obj.selected_style_folder not in available:
        settings_obj.selected_style_folder = available[0] if available else ''
        settings_obj.save(update_fields=['selected_style_folder'])

    return UserSettingsResponse(
        selectedStyleFolder=settings_obj.selected_style_folder,
        availableStyleFolders=available,
        backgrounds=_build_style_background_urls(settings_obj.selected_style_folder),
    )


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


@api.get('/settings', response=UserSettingsResponse)
def get_settings(request):
    user = _require_authenticated_user(request)
    return _user_settings_response_for(user)


@api.post('/settings', response=UserSettingsResponse)
def update_settings(request, payload: UserSettingsUpdateRequest):
    user = _require_authenticated_user(request)
    available = _get_available_style_folders()
    if payload.selectedStyleFolder not in available:
        raise HttpError(400, 'stile_non_valido')

    settings_obj, _ = UserSettings.objects.get_or_create(user=user)
    settings_obj.selected_style_folder = payload.selectedStyleFolder
    settings_obj.save(update_fields=['selected_style_folder'])
    return _user_settings_response_for(user)


@api.post('/settings/cache/clear', response=CacheClearResponse)
def clear_client_cache_hint(request):
    _require_authenticated_user(request)
    return CacheClearResponse(message='clear_client_cache_requested')


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
