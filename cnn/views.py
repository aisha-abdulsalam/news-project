from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import ChangePasswordSerializer, RegisterSerializer, CustomTokenObtainPairSerializer #, ChangePasswordSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer
from rest_framework_simplejwt.tokens import RefreshToken #helps you turn refresh token string into object so you can: blacklist it, check it, ispect it. without it django won't understand or be able to manipulate(blacklist) it.
from rest_framework_simplejwt.views import TokenObtainPairView
#from level 2
from django.contrib.auth  import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str

from django.shortcuts import get_object_or_404
from .models import Bookmark, Post, Comment
from .permissions import IsAdmin, IsAuthor, IsAuthorOrAdmin, IsReader #we import the custom permissions we created in permissions.py to use them in our views. These permissions will help us control access to certain views based on the user's role (admin, author, reader) and ownership of posts. For example, we can use IsAuthorOrAdmin to allow only the author of a post or an admin to edit or delete that post, while other users (readers) will not have permission to perform those actions.
from .serializers import PostSerializer, CommentSerializer

from rest_framework.throttling import UserRateThrottle
from rest_framework.filters import SearchFilter #used in PostListView to enable searching posts by title and content using query parameters in the URL (e.g., /posts/?search=keyword). It allows users to filter the list of posts based on specific search criteria, making it easier to find relevant posts.

from rest_framework.generics import RetrieveAPIView #used for retrieving a single object based on a lookup field (e.g., slug). It provides a get method handler that retrieves the object specified by the lookup field and returns it serialized using the specified serializer class. In this case, PostDetailView will retrieve a single Post object based on its slug and return its details serialized using the PostSerializer. The lookup_field attribute specifies that the slug field should be used to look up the post in the database when a request is made to this view (e.g., /posts/my-first-post/ where "my-first-post" is the slug of the post).
from rest_framework.response import Response #used to return HTTP responses from the view methods. It allows us to send data back to the client in a structured format (e.g., JSON) along with an appropriate HTTP status code. For example, we can use Response({"message": "Post liked"}, status=status.HTTP_200_OK) to return a success message when a post is liked, or Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) to return validation errors when a request fails validation.

from .models import Like, Bookmark #we import the Like and Bookmark models to use them in our views for handling post likes and bookmarks. This allows us to create, delete, and manage likes and bookmarks for posts based on user interactions with the API endpoints related to liking and unliking posts, as well as bookmarking posts. For example, in the LikePostView, we can create a new Like instance when a user likes a post, and in the UnlikePostView, we can delete the corresponding Like instance when a user unlikes a post.
from rest_framework.generics import ListAPIView #used for listing objects. It provides a get method handler that returns a list of objects based on the queryset and serializer_class defined in the view. In this case, PostListView will return a list of all Post objects serialized using the PostSerializer. The filter_backends and search_fields attributes allow for searching posts by title and content using query parameters in the URL (e.g., /posts/?search=keyword).

from django_filters.rest_framework import DjangoFilterBackend #used in PostListView to enable filtering posts based on specific fields (e.g., author, category, status) using query parameters in the URL (e.g., /posts/?author=1&category=tech). It allows users to filter the list of posts based on specific criteria, making it easier to find relevant posts. By adding DjangoFilterBackend to the filter_backends and specifying filterset_fields, we can easily filter posts by those fields without having to implement custom filtering logic in the view.
from rest_framework.filters import SearchFilter

from django.contrib.auth.tokens import default_token_generator

#def home(request):
 #   return HttpResponse("<h1>Welcome to CNN!</h1>")

 #goal: Accept POST request, Validate serializer, Create user, Return success response

#the end point to this view is the url that prints to it. NOT THE VIEW itself (i.e POST /register/)
class RegisterView(APIView):
    # We do NOT add permission_classes here
    # That means this view will use the DEFAULT permission.
    # Since we set AllowAny globally,
    # anyone can register (which is correct).
    #This method handles POST requests to the registration endpoint. It takes the incoming request data, validates it using the RegisterSerializer, and if the data is valid, it creates a new user using the serializer's create method. If the user is successfully created, it returns a success response with a message indicating that the registration was successful. If there are validation errors, it returns a response with the errors and a 400 Bad Request status code.
    def post(self, request):
        # request.data contains the incoming JSON body.
        # Example: {
        #   "username": "aisha",
        #   "email": "aisha@gmail.com",
        #   "password": "StrongPass123",
        #   "confirm_password": "StrongPass123"}
        # We pass request.data into our serializer.
        # This does NOT save anything yet.
        # It only prepares for validation.
        serializer = RegisterSerializer(data=request.data) #serializer instance is created with the incoming request data. The data=request.data argument passes the data from the POST request to the serializer for validation and processing. RegisterSerializer is a serializer class that is responsible for validating the incoming data and creating a new user instance based on that data. The serializer will check if the provided data meets the required fields and validation criteria defined in the RegisterSerializer class.
        # serializer.is_valid() does:
        # 1. Check required fields exist
        # 2. Check email format is correct
        # 3. Check password matches confirm_password
        # 4. Run validate_password() for strength
        # 5. Collect errors if any
        if serializer.is_valid():  #is_valid() method is called to validate the incoming data against the rules defined in the RegisterSerializer. If the data is valid, it will return True, and the code inside the if block will be executed. If the data is not valid, it will return False, and the code inside the else block will be executed.
            # serializer.save() triggers:
            # → the create() method inside serializer
            # → which calls User.objects.create_user()
            # → which hashes the password properly
            serializer.save() #save() method is called to create a new user instance based on the validated data. This method will typically call the create() method defined in the RegisterSerializer, which handles the actual creation of the user, including hashing the password and saving the user to the database.
            return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED) #If the user is successfully created, a response with a success message and a 201 Created status code is returned to indicate that the registration was successful.
           
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        ) #If there are validation errors, a response containing the errors and a 400 Bad Request status code is returned to indicate that the registration failed due to invalid

#from django.contrib.auth import authenticate
#class LoginView(APIView):
#    def post(self, request):
#        user = authenticate(
#            username=request.data.get("username"),
#            password=request.data.get("password")
#        )
#        if user is None:
#            return Response({"error": "Invalid credentials"}, status=401)

#        refresh = RefreshToken.for_user(user)

#        return Response({
#            "refresh": str(refresh),
#            "access": str(refresh.access_token)
#        })





#CUSTOM LOGIN VIEW
class CustomLoginView(TokenObtainPairView):
    """
    Custom login view that uses the CustomTokenObtainPairSerializer.
    This ensures JWT token generation works properly with the custom User model.
    Accepts POST requests with 'username' and 'password' fields.
    Returns access and refresh tokens.
    """
    serializer_class = CustomTokenObtainPairSerializer

#no need for login view (thanks to jtw) so we move on to logout
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can logout
    
    def post(self, request):
        try:
            # user sentd POST /logout/ { "refresh: ""fghjkl..."} request.get["request"] below will get the value of the "refresh" field in the JSON body
            refresh_token = request.data["refresh"] #this line will crash if missing cuz it's compulsory but this line: refresh_token = request.data.get("refresh") will return None

            # Convert string token into token object
            token = RefreshToken(refresh_token)

            # Blacklist the token
            token.blacklist()
            
            return Response(
                {"message": "Logout successful"},
                status=status.HTTP_205_RESET_CONTENT
            )
        
        except Exception:
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user #
            old_password = serializer.validated_data["old_password"]
            #
            if not user.check_password(old_password):
                return Response({"error": "Password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
            #get new password
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
        #if validation fails
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


User = get_user_model()

class PasswordResetRequestView(APIView):
    
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            return Response({"message": "if this emailexists, a reset link will be sent"})
    
        uid = urlsafe_base64_encode(force_bytes(user.id))

        token = PasswordResetTokenGenerator().make_token(user)

        reset_link = f"/reset-password/{uid}/{token}/"

        return Response({"reset_link": reset_link})


class PasswordResetConfirmView(APIView):
    def post(self, request, uid, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=user_id)
        except Exception:
            return Response({"error": "invalid reset link"}, status=400)
        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"error": "Token invalid or expired"}, status=400)
        
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=400)
        #set new password (django hases automatically)
        user.set_password(new_password)

        user.save()
        return Response({"message": "Password reset successful"}, status=200)

#admin view all users
class AllUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "admin":
            return Response({"error": "Only admins allowed"}, status=403)

        users = User.objects.all()

        data = [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "role": u.role
            }
            for u in users #
        ]

        return Response(data)

#CREATE POST
class CreatePostView(APIView):

    permission_classes = [IsAuthenticated, IsAuthorOrAdmin]#we use IsAuthorOrAdmin because both authors and admins can create posts, but readers cannot. This permission class will allow access to the view for users who are either authors or admins, while denying access to readers. By adding this permission class to the CreatePostView, we ensure that only users with the appropriate roles (authors and admins) can create new posts, while readers will not have permission to perform this action.

    def post(self, request):

        serializer = PostSerializer(data=request.data)

        #
        #if validation passes, we save the post with the current user as the author. This is done by passing author=request.user to the save() method of the serializer. This way, when a new post is created, it will be associated with the user who made the request, allowing us to track which user created which post and enforce permissions based on authorship in other views (e.g., only allowing authors to edit or delete their own posts).
        if serializer.is_valid(): 

            serializer.save(author=request.user)#Whoever is logged in becomes the author of this post

            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

#updates title, content, image, status(turn drafts into published posts) 
class UpdatePostView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=404)

        # Only author or admin can edit
        if request.user != post.author and request.user.role != "admin":
            return Response({"error": "Permission denied"}, status=403)

        serializer = PostSerializer(post, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


    
# LIST POSTS
class ListPostsView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):

        if request.user.role == "admin":
            posts = Post.objects.all()

        elif request.user.role == "author":
            posts = Post.objects.filter(author=request.user)

        else:
            posts = Post.objects.filter(status="published")

        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)


# GET SINGLE POST
class GetSinglePostView(APIView):

    def get(self, request, slug):

        post = get_object_or_404(Post, slug=slug, status="published")

        serializer = PostSerializer(post)

        return Response(serializer.data)


# UPDATE POST
class UpdatePostView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, slug):

        post = get_object_or_404(Post, slug=slug)

        if post.author != request.user:
            return Response(
                {"error": "You can only edit your own post"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = PostSerializer(post, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


# DELETE POST
class DeletePostView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, slug):

        post = get_object_or_404(Post, slug=slug)

        if post.author != request.user:
            return Response(
                {"error": "You can only delete your own post"},
                status=status.HTTP_403_FORBIDDEN
            )

        post.delete()

        return Response({"message": "Post deleted"})

class CreateCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):

        try:
            post = Post.objects.get(id=post_id, status="published")
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=404)

        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class UpdateCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"})

        if comment.author != request.user:
            return Response(
                {"error": "You can only edit your own comments"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = CommentSerializer(
            comment,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class DeleteCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"})

        if comment.author != request.user:
            return Response(
                {"error": "You can only delete your own comments"},
                status=status.HTTP_403_FORBIDDEN
            )
        comment.delete()
        return Response({"message": "Comment deleted"})

#views comments 
class PostCommentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id, status="published")
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikePostView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post) #What get_or_create() Does It checks:Does this like already exist? If it does, return it. If it doesn't, create it and return it. This prevents duplicate likes from the same user on the same post, ensuring that each user can only like a post once. If a user tries to like a post they have already liked, get_or_create() will simply return the existing Like instance without creating a new one, thus maintaining data integrity and preventing multiple likes from the same user on the same post.
        #Like.objects.create(user=request.user, post=post) #this one only creates making the system crash cuz it will contradict  class Meta:unique_together = ("user", "post") in models.py which prevents duplicate likes from the same user on the same post. If a user tries to like a post they have already liked, this line will raise an IntegrityError due to the unique_together constraint. To avoid this, we should use get_or_create() instead of create() to ensure that we only create a new Like if it doesn't already exist.
        if created:
            return Response({"message": "Post liked"})
        else:
            return Response({"message": "You already liked this post"})
    
class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, post_id):

        Like.objects.filter(
            user=request.user,
            post_id=post_id
        ).delete()

        return Response({"message": "Like removed"})

class PostDetailView(RetrieveAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"
    #every time a post is retrieved through this view, the retrieve() method is overridden to increment the views_count of the post by 1 and save the updated post instance before returning the serialized data in the response. This allows us to track how many times a post has been viewed.
    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()

        post.views_count += 1
        post.save()

        serializer = self.get_serializer(post)
        return Response(serializer.data)

#this class
class PostListView(ListAPIView):
    #queryset = Post.objects.all()
    queryset = Post.objects.filter(status="published")
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ["author", "category", "status"]
    search_fields = ["title", "content"]#


class BookmarkPostView(APIView):
    permission_classes = [IsAuthenticated]
    #This method handles POST requests to bookmark a post. It retrieves the post based on the provided post_id, creates a new Bookmark instance associating the current user with the post, and returns a success message indicating that the post has been bookmarked. This allows users to bookmark posts they are interested in for easy access later.
    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            post=post
        )#read about this in LikePostView.
        if created:
            return Response({"message": "Post bookmarked"})
        else:
            return Response({"message": "You already bookmarked this post"})

class RemoveBookmarkView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, post_id):
        Bookmark.objects.filter(
            user=request.user,
            post_id=post_id
        ).delete()
        return Response({"message": "Bookmark removed"})


class VerifyEmailView(APIView):
    def get(self, request, uid, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=user_id)

            if default_token_generator.check_token(user, token):
                user.is_verified = True
                user.save()

                return Response({"message": "Email verified successfully"})

        except Exception:
            pass

        return Response({"error": "Invalid token"}, status=400)




#for user to make request to admin to promote users to admin. what gets executed when you
class RequestAuthorView(APIView): 
    permission_classes = [IsAuthenticated] 
    def post(self, request): 
        request.user.is_author_requested = True 
        request.user.save() 
        return Response({"message": "Author request submitted"})

#for admin. 
class PromoteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, user_id):
        # Only admin can do this
        if request.user.role != 'admin':
            return Response({"error": "Only admins can promote users"}, status=403)

        try:
            user = User.objects.get(id=user_id)
            user.role = 'admin'
            user.is_staff = True
            user.save()

            return Response({"message": "User promoted to admin"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        


class PendingRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'admin':
            return Response({"error": "Only admins allowed"}, status=403)

        users = User.objects.filter(is_author_requested=True)
        data = [{"id": u.id, "username": u.username} for u in users]

        return Response(data)


#Admin approves the request
#from django.contrib.auth import get_user_model
#User = get_user_model()

class ApproveAuthorView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, user_id):
        # Only admin can approve
        if request.user.role != 'admin':
            return Response({"error": "Only admins allowed"}, status=403)

        try:
            user = User.objects.get(id=user_id)

            if not user.is_author_requested:
                return Response({"error": "User did not request author role"}, status=400)

            user.role = 'author'
            user.is_author_requested = False
            user.save()

            return Response({"message": "User is now an author"})

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

####
from rest_framework.parsers import MultiPartParser, FormParser

class UpdateProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request):
        user = request.user

        image = request.FILES.get("profile_picture")

        if not image:
            return Response({"error": "No image provided"}, status=400)

        user.profile_picture = image
        user.save()

        return Response({
            "message": "Profile picture updated",
            "profile_picture": user.profile_picture.url
        })


#ListAPIView vs APIView:
#ListAPIView is a generic view that provides a built-in implementation for listing objects. It handles




