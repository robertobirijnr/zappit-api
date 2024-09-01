
from django.urls import path
from .views import  register, login, AuthenticatedUser, logout, PermissionAPIView, RoleViewSet, UserGenericAPIView, ProfileInfoAPIVIEW, ProfilePasswordAPIVIEW

urlpatterns = [
    path('register', register),
    path('login',login),
    path('logout',logout),
    path('user',AuthenticatedUser.as_view()),
    path('permissions',PermissionAPIView.as_view()),
    path('roles',RoleViewSet.as_view({
        'get':'list',
        'post':'create'
    })),
     path('roles/<str:pk>',RoleViewSet.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy'
    })),
    path('users/info',ProfileInfoAPIVIEW.as_view()),
    path('user/password',ProfilePasswordAPIVIEW.as_view()),
    path('users',UserGenericAPIView.as_view()),
    path('users/<str:pk>',UserGenericAPIView.as_view())
  
]
