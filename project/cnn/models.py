from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify # slugify converts a string into a URL-friendly format. Example: "Hello World!" → "hello-world"
from django.core.exceptions import ValidationError #for file size for adding images


def validate_image_size(image):

    max_size = 2 * 1024 * 1024  # 2MB

    if image.size > max_size:
        raise ValidationError("Image must be smaller than 2MB")


#If different user types share 90% of the same data → use ONE table.(i.e for author, admin, reader)
#in a case where we need to stor that 10% that they don't share → use multi-table inheritance (i.e. create a table for each user type and link them to the main user table using a one-to-one relationship)[e.g. only authors have a bio field(Authorprofile), only readers have a subscription field, only admins have a AdminProfile etc.]
# AbstractUser gives us:
# username
# email
# password
# first_name
# last_name
# is_active
# date_joined
# permissions system
class User(AbstractUser):

    # ROLE_CHOICES restrict what values can be saved in the database, This prevents random strings from being stored as roles
    ROLE_CHOICES = (
        ('admin', 'Admin'), #(field_value, display_label) where field value is what is stored in the database and display_label is what is shown in the admin panel and other parts of the application
        ('author', 'Author'),
        ('reader', 'Reader'),
        )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='reader') # role determines what actions a user can perform.default='reader' because most registered users are readers.
    is_author_requested = models.BooleanField(default=False) # for admin to authorise/permit other users to become admin
    #
    is_verified = models.BooleanField(default=False) #This field can be used to track whether a user's email address has been verified. When a user registers, you can set is_verified to False and send them a verification email with a link. When they click the link, you can set is_verified to True, allowing them to access certain features of the application that require email verification.

    #__str__ controls how the user appears in:- Django admin  - Django shell  - Anywhere the obj    - Anywhere the object is printed
    def __str__(self):
        return self.username



# OneToOneField is used to create a one-to-one relationship between the Authorprofile and User models. Meaning that each Authorprofile is linked to exactly one User(/role -> ('author', 'Author')), and each User can have at most one Authorprofile. The related_name='author_profile' allows us to access the Authorprofile from the User model using user.author_profile.
#in simpler terms, the model below adds fields(bio, phone number, profile picture) that are specific to authors alone, that where not already defined by the User model or the AbstractUser model.
class AuthorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author_profile')#on_delete=models.CASCADE here means if a user is deleted then the corresponding Authorprofile will also be deleted. This ensures that we don't have orphaned Authorprofile records in the database when a user is removed.
    bio = models.TextField(blank=True) #Author biography (optional field beacuase blank=True). blank=True allows it to be empty in forms.
    phone_number = models.CharField(max_length=15, blank=True)#
    profile_picture = models.ImageField(upload_to= 'author_profiles', blank=True, null=True) #blank=True and null=True make this field optional, we need both because ImageField is a file field and it needs to be able to store a null value in the database when no image is uploaded, and blank=True allows the form to be submitted without an image. so in a case were we only need text/string input (like the bio, phone number...) we can just use blank=True to make it optional, but for file fields we need both blank=True and null=True to make them optional.
    # Controls how profile appears in admin panel.
    def __str__(self):
        return f"{self.user.username}'s Profile" #This will display the username of the user associated with the Authorprofile in the admin panel, making it easier to identify which profile belongs to which user. For example, if the user's username is "john_doe", it will display "john_doe's Profile" in the admin panel.




# The Category model represents a category that can be assigned to posts. It has a name field to store the name of the category. This allows you to organize posts into different categories, making it easier for users to find content related to specific topics. You can create a many-to-many relationship between the Post and Category models if you want to allow posts to belong to multiple categories, but in this simple implementation, we are just defining the Category model without linking it to the Post model.
class Category(models.Model):
    name = models.CharField(max_length=100)

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'), #Not visible to public
        ('published', 'Published'), #visible to public
        ('archived', 'Archived'), #archived posts are not visible to readers but are kept in the database for record-keeping or future reference.
    )

    title = models.CharField(max_length=200) #Title of blog post.CharField is used for short-to-medium length text.
    slug = models.SlugField(unique=True, blank=True) #blank=True allows the slug to be optional when creating a post because we can automatically generate it from the title if not provided. And unique=True ensures that each slug is unique across all posts in the database. This is important for generating unique URLs for each post based on the slug.
    content = models.TextField() #TextField is used for longer text content, such as the body of a blog post.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to="posts/", validators=[validate_image_size], null=True, blank=True) #This field allows you to upload an image associated with the post. The upload_to="posts/" argument specifies that the uploaded images will be stored in a directory named "posts" within your media directory. null=True and blank=True make this field optional, allowing you to create posts without an image if desired.
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft' )
    views_count = models.PositiveIntegerField(default=0) #This counts how many people read a post.
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True) #This field allows you to assign a category to the post. The on_delete=models.CASCADE argument means that if a category is deleted, all posts associated with that category will also be deleted. null=True and blank=True make this field optional, allowing you to create posts without assigning them to a category if desired.
    created_at = models.DateTimeField(auto_now_add=True) #auto_now_add=True means that the created_at field will be automatically set to the current date and time when a new Post instance is created.
    updated_at = models.DateTimeField(auto_now=True)#auto_now=True means that the updated_at field will be automatically set to the current date and time whenever the Post instance is saved, which includes both creation and updates. This allows us to track when a post was last modified.
    

    def save(self, *args, **kwargs):
        if not self.slug:                 # Only create slug if it’s empty
            self.slug = slugify(self.title)  # Convert title to URL-friendly string
        super().save(*args, **kwargs)  # Call the original save() to store in DB


    def __str__(self):
        return self.title#the first onr was to return who posted it, but this will return the title of what was posted.
        #return f"{self.author.username} posted: {self.title}" #This will display the username of the post's author along with the title of the post in the admin panel. For example, if the author's username is "john_doe" and the post title is "Django Models Explained", it will display "john_doe posted: Django Models Explained" in the admin panel. This provides a quick overview of who created the post and what it's about.


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') #a comment can only belong to a post, but a post can have multiple comments. on_delete=models.CASCADE means that if a post is deleted, all comments associated with that post will also be deleted. related_name='comments' allows us to access the comments of a post using post.comments.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')#author of the comment, not the post. calling the User model so all user types(author, reader, admin) should be able to comment. related_name='comments here means that we can access the comments made by a user using user.comments.
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        
        
        
         return f"{self.author.username} commented on {self.post.title} : {self.content[:20]}..." #This will display the username of the comment's author, the title of the post they commented on, and a preview of the comment content (first 20 characters) in the admin panel. For example, if the author's username is "john_doe", the post title is "Django Models Explained", and the comment content is "This is a great post about Django models!", it will display "john_doe commented on Django Models Explained : This is a great..." in the admin panel. This provides a quick overview of who commented, on which post, and what they said while still showing a preview of the comment content.
        #return f"{self.author.username} commented: {self.content[:20]}..." #This will display the username of the comment's author along with the first 20 characters of the comment content in the admin panel. For example, if the author's username is "john_doe" and the comment content is "This is a great post about Django models!", it will display "john_doe commented: This is a great..." in the admin panel. This provides a quick preview of the comment while still showing who made it.
        #return f'Comment by {self.author.username}' #This will display the username of the comment's author in the admin panel. For example, if the author's username is "john_doe", it will display "Comment by john_doe" in the admin panel. This provides a simple and clear way to identify who made the comment without showing any content preview.

# The Like model represents a "like" that a user can give to a post. It has a foreign key relationship to both the User and Post models, indicating which user liked which post. The on_delete=models.CASCADE argument means that if either the user or the post is deleted, the corresponding like will also be deleted from the database. This helps maintain data integrity by ensuring that there are no orphaned like records that reference non-existent users or posts.
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    #Right now users can like a post 1000 times. so the code bellow makes it 1 user = 1 like per post
    class Meta:
        unique_together = ("user", "post")

# The Bookmark model represents a bookmark that a user can create for a post. Similar to the Like model, it has a foreign key relationship to both the User and Post models, indicating which user bookmarked which post. The on_delete=models.CASCADE argument ensures that if either the user or the post is deleted, the corresponding bookmark will also be deleted from the database, preventing orphaned bookmark records.
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) 

    #Right now users can bookmark a post 1000 times. so the code bellow makes it 1 user = 1 bookmark per post
    class Meta:
        unique_together = ("user", "post")














