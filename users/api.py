from ninja import Router
from django.contrib.auth.models import User
from .schemas import RegisterUser, LoginUser
from django.contrib.auth import logout as auth_logout, authenticate, login as auth_login
from django.middleware.csrf import get_token


router = Router()


@router.get("/set-csrf-token")
def get_csrf_token(request):
    return {"csrftoken": get_token(request)}


@router.post("/register", tags=["User"])
def register(request, payload: RegisterUser):
    user = User.objects.create_user(**payload.dict())
    return {"success": True, "user": user.username}


@router.post("/login", tags=["User"])
def login(request, payload: LoginUser):
    user = User.objects.filter(username=payload.username).first()
    if user and user.check_password(payload.password):
        # Authenticate the user
        user = authenticate(request, username=payload.username,
                            password=payload.password)
        if user:
            auth_login(request, user)
            return {"success": True, "user": user.username}
    return {"success": False, "error": "Invalid credentials"}


@router.get("/me", tags=["User"])
def me(request):
    user = request.user
    if user.is_authenticated:
        return {"username": user.username, "email": user.email}
    return {"error": "User not authenticated"}


@router.post("/logout", tags=["User"])
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return {"success": True}
    return {"error": "User not authenticated"}
