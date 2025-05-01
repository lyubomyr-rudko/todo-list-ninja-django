from ninja import Router
from django.contrib.auth.models import User
from .schemas import RegisterUser, LoginUser
from django.contrib.auth import logout, authenticate


router = Router()

@router.post("/register")
def register(request, payload: RegisterUser):
    user = User.objects.create_user(**payload.dict())
    return {"success": True, "user": user.username}

@router.post("/login")
def login(request, payload: LoginUser):
    user = User.objects.filter(username=payload.username).first()
    if user and user.check_password(payload.password):
        # Authenticate the user
        user = authenticate(request, username=payload.username, password=payload.password)
        if user:
            # Log the user in
            request.user = user
            return {"success": True, "user": user.username}
    return {"success": False, "error": "Invalid credentials"}

@router.get("/me")
def me(request):
    user = request.user
    if user.is_authenticated:
        return {"username": user.username, "email": user.email}
    return {"error": "User not authenticated"}

@router.post("/logout")
def logout(request):
    if request.user.is_authenticated:
        logout(request)
        return {"success": True}
    return {"error": "User not authenticated"}
