import bcrypt

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save

from .models.darkflame.dynamic.dynamic import Accounts, ActivityLog

class DarkflameAuthenticationBackend(BaseBackend):
    def __init__(self) -> None:
        super().__init__()

        user_logged_in.disconnect(dispatch_uid="update_last_login")
        user_logged_in.connect(self.update_last_login, dispatch_uid="update_last_login")
    
    def update_last_login(self, sender, request, user, **kwargs):
        ActivityLog.objects.create( # I am cheating here, character id is user id, this is a NEEDS to change
            character_id=user.id,
            activity=2,
            timestamp=int(request.session.get("last_activity", 0)),
            map_id=0,
        )

    def authenticate(self, request, username=None, password=None):
        try:
            user = Accounts.objects.get(name=username)
            if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                if not ActivityLog.objects.filter(character_id=user.id, activity=2).exists():
                    post_save.send(sender=Accounts, instance=user, created=True)
                return self.complete_user_model(user)
        except Accounts.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = Accounts.objects.get(pk=user_id)
            return self.complete_user_model(user)
        except Accounts.DoesNotExist:
            return None
        
    def complete_user_model(self, user):
        user.configure_abstrated_information()
        return user
        