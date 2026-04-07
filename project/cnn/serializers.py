#serealizer.py is for data validation 
from rest_framework import serializers
from django.contrib.auth import get_user_model #get_user_model() ensures we use YOUR custom User model instead of Django’s default User
from django.contrib.auth.password_validation import validate_password # validate_password is a built-in function provided by Django that checks if a given password meets the defined password validation criteria. It raises a ValidationError if the password does not meet the requirements, such as minimum length, complexity, or common password checks. By using validate_password in your serializer, you can ensure that the passwords provided by users during registration or password change meet the security standards defined in your Django settings.
from .models import Bookmark

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "profile_picture"]

#REGISTRATION SERIALIZER
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators = [validate_password]) # write_only=True means that the password field will only be used for input (when creating or updating a user) and will not be included in the serialized output (when retrieving user data). This is a security measure to prevent the password from being exposed in API responses.
    
    #email = serializers.EmailField(required=True)
    #username = serializers.CharField(required=False)

#Meta class is used to specify the model that the serializer should be based on. In this case, we are specifying that the serializer should be based on the User model. This allows the serializer to automatically generate fields and validation based on the User model's attributes and constraints.
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name'] # fields is a list of the fields that should be included in the serialized output. In this case, we are including the id, username, email, password, first_name, and last_name fields from the User model. This means that when we serialize a User instance using this serializer, only these specified fields will be included in the output.

        
#this method is responsible for creating a new user instance based on the validated data provided by the serializer. It takes the validated data as input and uses it to create a new user using the create_user method provided by the User model. The create_user method is a built-in method that handles the creation of a new user, including hashing the password and saving the user to the database. The create method then returns the newly created user instance.
    def create(self, validated_data):
        #object creation using the create_user method provided by the User model. This method takes care of hashing the password and saving the user to the database.
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'], #
            first_name=validated_data.get('first_name', ''),#this one has an emplty string as a default value, which means that if the first_name field is not provided in the validated_data, it will be set to an empty string ('') instead of raising an error. This allows for optional fields in the registration process, where users can choose to provide their first and last names or leave them blank.
            last_name=validated_data.get('last_name', ''),#get() method is used to retrieve the value of the first_name and last_name fields from the validated_data dictionary. If the fields are not present in the validated_data, it will return an empty string ('') as a default value. This allows for optional fields in the registration process, where users can choose to provide their first and last names or leave them blank.
        )
        return user 
   
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True) # old_password is a required field that will be used to verify the user's current password before allowing them to change it. This is a security measure to ensure that only the rightful owner of the account can change the password.
    new_password = serializers.CharField(required=True, validators=[validate_password]) # new_password is a required field that will be used to set the user's new password. This field will be validated using Django's built-in password validation to ensure that it meets the defined security criteria, such as minimum length and complexity requirements.
    confirm_password = serializers.CharField(required=True) # confirm_password is a required field that will be used to confirm the user's new password. This field will be validated to ensure that it matches the new_password field.

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match"})
        return data

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True) #this line

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match"})
        return data


#
class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField() # token is a required field that will be used to verify the user's identity during the password reset process. This token is typically generated and sent to the user's email address when they initiate a password reset request. The user will then need to provide this token along with their new password to confirm their identity and complete the password reset process. The token helps ensure that only the rightful owner of the account can reset the password, adding an extra layer of security to the password reset mechanism.
    new_password = serializers.CharField() # new_password is a required field that will be used to set the user's new password after they have initiated a password reset. This field will be validated using Django's built-in password validation to ensure that it meets the defined security criteria, such as minimum length and complexity requirements. This serializer will typically be used in conjunction with a token-based password reset mechanism, where the user receives a token via email and uses it to confirm their identity before setting a new password.

#The BookmarkSerializer is a tool that helps us convert Bookmark objects into a format that can be easily sent over the internet (like JSON) and also helps us validate and create Bookmark objects when we receive data from the client. It simplifies the process of working with Bookmark data in our API by providing a structured way to handle serialization and deserialization based on the Bookmark model.
class BookmarkSerializer(serializers.ModelSerializer):
    #The Meta class provides metadata about the serializer. In this case, it specifies that the serializer should be based on the Bookmark model and that all fields of the model should be included in the serialization process. This means that when we use the BookmarkSerializer to serialize a Bookmark instance, it will include all the fields defined in the Bookmark model in the output.
    class Meta:
        model = Bookmark #connection to the specific model in models.py
        fields = "__all__" #fields = "__all__" is a shortcut that tells the serializer to include all fields from the Bookmark model in the serialization process. This means that when we serialize a Bookmark instance using this serializer, it will include all the fields defined in the Bookmark model in the output. This is a convenient way to quickly include all fields without having to list them individually. However, if you want to include only specific fields, you can replace "__all__" with a list of field names that you want to include in the serialization.


from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    #
    class Meta:
        model = Post
        fields = "__all__" #
        read_only_fields = ['author'] #Don’t expect author from request body — I will set it manually


class CommentSerializer(serializers.ModelSerializer):
    #
    class Meta:
        model = Comment
        fields = "__all__" #
        read_only_fields = ['user']  
        read_only_fields = ['author'] #Don’t expect author from request body — I will set it manually


#Why We Use Different Serializer Types
#Type	            Used When
#ModelSerializer	Creating or updating model objects
#Serializer	        Validating simple input that doesn’t directly map to model

#Example:
#Registration → ModelSerializer (creates User)
#Change Password → Serializer (not creating User)






