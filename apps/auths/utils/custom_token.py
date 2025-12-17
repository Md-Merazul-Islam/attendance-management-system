from rest_framework_simplejwt.tokens import RefreshToken

class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        refresh = cls()
        refresh["user_id"] = str(user.uid) 
        refresh["full_name"] = user.full_name
        refresh["email"] = user.email
        refresh["role"] = user.role.role_name if user.role else None
        
        return refresh