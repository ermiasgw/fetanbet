from django.urls import path,include
from rest_framework import routers
from . import views
from knox import views as knox_views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

app_name="users"
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('signup/', views.SignUp().as_view()),
    path('confirm-email/<str:token>/', views.ConfirmEmail().as_view()),
    path('login/', views.LoginView().as_view()),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),

]