"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


#
""""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from cnn.views import LogoutView

from cnn.views import PasswordResetRequestView
from cnn.views import PasswordResetConfirmView

from cnn.views import (
    CreateCommentView,
    UpdateCommentView,
    DeleteCommentView,
    PostCommentsView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    # JWT authentication endpoints
    path('login/', TokenObtainPairView.as_view()), #What happens internally:1. User sends username + password 2. Django checks password hash 3. If correct:- Generates ACCESS token (short life)- Generates REFRESH token (long life) 4. Returns both tokens in response. TokenObtainPairView is a built-in view provided by the Simple JWT library that handles user authentication and token generation. When a user sends a POST request to the /login/ endpoint with their username and password, this view validates the credentials and, if they are correct, returns a JSON response containing an access token and a refresh token. The access token is used for authenticating subsequent requests to protected endpoints, while the refresh token can be used to obtain a new access token when the current one expires.
    path('token/refresh/', TokenRefreshView.as_view()), #TokenRefreshView is another built-in view provided by the Simple JWT library that handles token refreshing. When a user sends a POST request to the /token/refresh/ endpoint with a valid refresh token, this view validates the refresh token and, if it is valid, generates and returns a new access token. This allows users to maintain their authenticated session without having to log in again when their access token expires, as long as they have a valid refresh token.
    
    path('logout/', LogoutView.as_view()), #LogoutView is a custom view that handles user logout by blacklisting the refresh token.
    #password reset
    path('password-reset-request/', PasswordResetRequestView.as_view()),
    path('reset-password/<uid>/<token>', PasswordResetConfirmView.as_view()),

    #comments
    path('comments/create/', CreateCommentView.as_view()),
    path('comments/<int:pk>/update/', UpdateCommentView.as_view()),
    path('comments/<int:pk>/delete/', DeleteCommentView.as_view()),
    path('posts/<int:post_id>/comments/', PostCommentsView.as_view()),

    ]

"""



from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('admin/', admin.site.urls),

    # Send all API requests to the cnn app
    path('api/', include('cnn.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #This line is used to serve media files (such as images) during development. It appends a URL pattern to the urlpatterns list that maps the MEDIA_URL to the MEDIA_ROOT directory. This allows you to access uploaded media files through the specified URL path. Note that this is only suitable for development and should not be used in production, where you should configure your web server to serve media files directly.





