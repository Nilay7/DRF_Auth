from django.urls import include, path
from .views import ListBooksView, LoginView, RegisterUsers
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('books/', ListBooksView.as_view(), name = "books-all"),
    # path('rest-auth/', include('rest_auth.urls')),    
    path('auth/login/', LoginView.as_view(), name = "auth-login"),
    path('auth/register/', RegisterUsers.as_view(), name="auth-register")
]