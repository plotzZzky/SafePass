from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse

from .serializer import serialize_password
from .pwd import *


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_pwd_list(request):
    try:
        pwd_db = request.user.profile.db_pwd
        db_path = request.user.profile.db
        db = open_file(db_path, pwd_db)
        if db.entries:
            data = [serialize_password(item) for item in db.entries]
        else:
            data = {"pwd": []}
        return JsonResponse({"pwd": data}, status=200)
    except KeyError or AttributeError:
        return HttpResponse("Password db not found", status=400)
    except FileNotFoundError:
        return HttpResponse("Db file not found", status=404)


@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def create_password(request):
    try:
        pwd_db = request.user.profile.db_pwd
        db_path = request.user.profile.db
        post = request.POST
        title = post['new_title']
        user = post['user']
        pwd = post['pwd']
        password = check_pwd(pwd)
        url = post['url']
        if validate_pwd(title, password):
            add_password(db_path, pwd_db, title, user, password, url)
            return JsonResponse({"Error": "Entrada salva"}, status=200)
        else:
            return JsonResponse({"Error": "Formulario invalido"}, status=300)
    except KeyError:
        return JsonResponse({"Error": "Formulario incorreto"}, status=404)


@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def edit_password(request):
    try:
        pwd_db = request.user.profile.db_pwd
        db_path = request.user.profile.db
        post = request.POST
        title = post['title']
        new_title = post['new_title']
        user = post['user']
        pwd = post['pwd']
        password = check_pwd(pwd)
        url = post['url']
        if validate_pwd(new_title, pwd):
            password_update(db_path, pwd_db, title, new_title, user, password, url)
            return HttpResponse("Entrada editada", status=200)
        else:
            return HttpResponse("Entrada não encontrada", status=300)
    except KeyError:
        return JsonResponse({"Error": "Formulario incorreto"}, status=400)


@api_view(['DELETE'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def del_password(request):
    try:
        pwd_db = request.user.profile.db_pwd
        title = request.POST['title']
        db_path = request.user.profile.db
        delete_password(db_path, pwd_db, title)
        return HttpResponse("Senha deletada", status=200)
    except KeyError or FileNotFoundError:
        return HttpResponse("Banco de dados não encontrados", status=404)
    except AttributeError:
        return HttpResponse("Senha não existe", status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_db(request):
    filename = request.user.profile.db
    response = FileResponse(open(filename, 'rb'))
    return response
