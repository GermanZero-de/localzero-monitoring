from allauth.account.adapter import DefaultAccountAdapter
from invitations.app_settings import app_settings

from .models import AccessRight, City, get_invitation


class AllauthInvitationsAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        """
        Overwrites django-invitations.
        Checks that there exists an invitation instead of email.
        """
        if get_invitation(request):
            return True
        elif app_settings.INVITATION_ONLY:
            return False
        else:
            return True

    def save_user(self, request, user, form, commit=True):
        """
        Overwrites django-allauth.
        Check there is an invitation and set the appropriate access rights.
        Swallow the user object already created, if not.
        Otherwise, set access rights according to invitation.
        """
        invitation = get_invitation(request)
        if not invitation:
            self.add_error(
                None,
                "Die Registrierung ist nur möglich über einen gültigen Einladungslink.",
            )
            return

        user.is_staff = True
        user = super().save_user(request, user, form, commit)

        city: City = invitation.city
        if invitation.access_right == AccessRight.CITY_VIEWER:
            city.city_viewers.add(user)
            city.save()
        elif invitation.access_right == AccessRight.CITY_EDITOR:
            city.city_editors.add(user)
            city.save()
        elif invitation.access_right == AccessRight.CITY_ADMIN:
            city.city_admins.add(user)
            city.save()

        return user
