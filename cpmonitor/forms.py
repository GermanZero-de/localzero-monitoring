from allauth.account.forms import SignupForm

from .models import Invitation
from .utils import get_invitation


class InvitationBasedSignupForm(SignupForm):
    def save(self, request):
        invitation = get_invitation(request)

        user = super(InvitationBasedSignupForm, self).save(request)

        # Add your own processing here.

        # You must return the original result.
        return user
