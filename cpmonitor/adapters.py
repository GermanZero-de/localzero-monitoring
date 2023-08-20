from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.signals import user_signed_up
from django.contrib import messages
from invitations.app_settings import app_settings

from .models import AccessRight, City, Invitation
from .utils import get_invitation


class AllauthInvitationsAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        if get_invitation(request):
            return True
        elif app_settings.INVITATION_ONLY is True:
            # Site is ONLY open for invites
            return False
        else:
            # Site is open to signup
            return True

    def get_user_signed_up_signal(self):
        return user_signed_up

    def save_user(self, request, user, form, commit=True):
        "Check there is an invitation and set the appropriate access rights. Swallow the user object, if not."
        invitation = get_invitation(request)
        print("Got invitation: " + str(invitation))
        if not invitation:
            self.add_error(
                None,
                "Die Registrierung ist nur möglich über einen gültigen Einladungslink.1",
            )
            messages.error(
                request,
                "Die Registrierung ist nur möglich über einen gültigen Einladungslink.2",
            )
            return

        user.is_staff = True
        user = super().save_user(request, user, form, commit)

        city: City = invitation.city
        if invitation.access_right == AccessRight.CITY_EDITOR:
            city.city_editors.add(user)
            city.save()
        elif invitation.access_right == AccessRight.CITY_ADMIN:
            city.city_admins.add(user)
            city.save()

        return user
