from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.sessions.backends.db import SessionStore
from django.http import JsonResponse

from .validate import valid_user, validate_username, validate_password, validate_email
from .models import Profile
from password.pwd import create_db, change_file_password


@api_view(['POST'])
@csrf_exempt
def register_user(request):
    try:
        password = request.data['password1']
        pwd = request.data['password2']
        username = request.data['username']
        email = request.data['email']
        if valid_user(password, pwd, username, email):
            user = User(username=username, email=email, password=password)
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            token = Token.objects.create(user=user)  # type:ignore
            db = create_db(password)
            profile = Profile(user=user, db=db, db_pwd=password)
            profile.save()
            return JsonResponse({"token": token.key}, status=200)
        else:
            return JsonResponse({"error": "Informações incorretas!"}, status=300)
    except KeyError:
        return JsonResponse({"error": "Informações faltando!"}, status=300)


@api_view(['POST'])
@csrf_exempt
def login(request):
    try:
        password = request.data['password']
        username = request.data['username']
        user = authenticate(username=username, password=password)
        if user is not None:
            token = Token.objects.get(user=user)  # type:ignore
            return JsonResponse({"token": token.key}, status=200)
        else:
            return JsonResponse({"error": "Login incorreto!"}, status=300)
    except KeyError:
        return JsonResponse({"error": "Login incorreto!"}, status=404)
