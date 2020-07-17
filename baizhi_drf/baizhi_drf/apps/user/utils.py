from django.db.models import Q
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.backends import ModelBackend

from user.models import UserInfo


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'username': user.username,
        'user_id': user.id
    }


# def check_user(account):
#     try:
#         user = UserInfo.objects.filter(Q(username=account) | Q(phone=account))[0]
#     except UserInfo.DoesNotExist:
#        return None
#     else:
#        return user

def check_user(account):
    user = UserInfo.objects.filter(Q(username=account) | Q(phone=account))[0]
    if user:
        return user
    return None




class UserAuthModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = check_user(username)
        if user and user.check_password(password) and user.is_authenticated:
            return user
        return None
