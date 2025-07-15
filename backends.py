from django.contrib.auth.backends import ModelBackend,BaseBackend
from django.contrib.auth.models import User



class CustomAuthBackend(BaseBackend):
    
    def authenticate(self, request, username=None, password=None):
        # List of predefined users (you can make this more complex if needed)
        predefined_users = {
            'shelflife':'root',
            'abc123': 'root',
        }

        # Check if the username exists and if the password matches
        if predefined_users.get(username) == password:
            # Return a user object if authentication is successful
            user, created = User.objects.get_or_create(username=username)
            return user
        
        return None  # Authentication failed
