from django.urls import path
from users import views

# Be careful setting the name to just /login use userlogin instead!
# SET THE NAMESPACE!
app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
]
