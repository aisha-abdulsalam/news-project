from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import (
    CustomLoginView,
    LogoutView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    AllUsersView,
    CreatePostView,
    UpdatePostView,
    CreateCommentView,
    UpdateCommentView,
    DeleteCommentView,
    PostCommentsView,
    PostDetailView,
    RegisterView,
    BookmarkPostView,
    RemoveBookmarkView,
    LikePostView,
    UnlikePostView,
    VerifyEmailView,
    PendingRequestsView,
    PromoteUserView,
    ApproveAuthorView,
    RequestAuthorView,
    ListPostsView,
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    #authentication
    path('login', CustomLoginView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()), #
    path('logout/', LogoutView.as_view()),

    #password reset
    path('password-reset-request/', PasswordResetRequestView.as_view()),
    path('reset-password/<uid>/<token>/', PasswordResetConfirmView.as_view()),

    path('view-all-users/', AllUsersView.as_view()),

    #from draft to published
    path('update-post/<int:pk>/', UpdatePostView.as_view()),
    #athor post an article
    path('create-post/', CreatePostView.as_view()),
    #list all posts
    path('posts/', ListPostsView.as_view()),
    #view 1 post
    # #this URL pattern is used to access the details of a specific post based on its slug. The <slug:slug> part of the URL captures the slug value from the URL and passes it as an argument to the PostDetailView. This allows users to access a post's details by visiting a URL like /posts/my-first-post/, where "my-first-post" is the slug of the post they want to view. The PostDetailView will then use this slug to retrieve and display the corresponding post's details.
    path("posts/<slug:slug>/", PostDetailView.as_view()),

    #comments
    path('posts/<int:post_id>/comments/create/', CreateCommentView.as_view()),
    path('comments/<int:pk>/update/', UpdateCommentView.as_view()),
    path('comments/<int:pk>/delete/', DeleteCommentView.as_view()),
    path('posts/<int:post_id>/comments/', PostCommentsView.as_view()),

    #this URL pattern is used to access the details of a specific post based on its slug. The <slug:slug> part of the URL captures the slug value from the URL and passes it as an argument to the PostDetailView. This allows users to access a post's details by visiting a URL like /posts/my-first-post/, where "my-first-post" is the slug of the post they want to view. The PostDetailView will then use this slug to retrieve and display the corresponding post's details.
    path("posts/<slug:slug>/", PostDetailView.as_view()),
    #
    path("posts/<int:post_id>/like/", LikePostView.as_view()),
    path("posts/<int:post_id>/unlike/", UnlikePostView.as_view()),

    #this URL pattern is used to bookmark a specific post based on its ID. The <int:post_id> part of the URL captures the post ID from the URL and passes it as an argument to the BookmarkPostView. This allows users to bookmark a post by visiting a URL like /posts/123/bookmark/, where "123" is the ID of the post they want to bookmark. The BookmarkPostView will then use this post ID to create a bookmark for the current user, allowing them to easily access the bookmarked post later.
    path("posts/<int:post_id>/bookmark/", BookmarkPostView.as_view()),
    path("posts/<int:post_id>/bookmark/remove/", RemoveBookmarkView.as_view()),

    path("verify-email/<uid>/<token>/", VerifyEmailView.as_view()),
    
    #
    path('request-author/', RequestAuthorView.as_view()),
    
    #
    path('pending-author-requests/', PendingRequestsView.as_view()),

    #Admin approves the request
    path('approve-author/<int:user_id>/', ApproveAuthorView.as_view()),
    
    #
    path('promote/<int:user_id>/', PromoteUserView.as_view()),

    
] 

#Django Admin Panel (how to use it) on chatGPT
#🧪 TEST IT
#GET /api/pending-author-requests/
#Header:
#Authorization: Bearer ADMIN_TOKEN
#✅ Response:
#[
#  {
#    "id": 3,
#    "username": "misimi"
#  }
#]

#approve-author/5/
#restart vscode?????????????/















