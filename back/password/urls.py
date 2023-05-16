from django.urls import path

from .import views


urlpatterns = [
    path('', views.get_pwd_list, name='get_pwd_list'),
    path('new/', views.create_password, name='new_pwd'),
    path('del/', views.del_password, name='delete_pwd'),
    path('edit/', views.edit_password, name='edit_pwd'),
    path('get/', views.download_db, name='download_db'),
]
