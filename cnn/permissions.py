from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"
    

class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "author"

#Author can edit only their post  and admin can edit any post. note: obj = the post
class IsAuthorOrAdmin(BasePermission):

    def has_permission(self, request, view):

        if request.user.role in ["admin", "author"]:
            return True

        return False
    
#class IsAuthorOrAdmin(BasePermission):
 #   def has_object_permission(self, request, view, obj):
  #      if request.user.role == "admin":
   #         return True
    #    #Author can only modify own post. note: obj = the post
     #   return obj.author == request.user


class IsReader(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "reader"




