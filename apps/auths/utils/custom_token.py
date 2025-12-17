from rest_framework_simplejwt.tokens import RefreshToken
class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(self, user):
        refresh_token = super().for_user(user)
        refresh_token.payload["full_name"] = user.full_name
        refresh_token.payload["email"] = user.email
        refresh_token.payload["role"] = user.role

        return refresh_token
