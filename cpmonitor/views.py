import json
import os
import re
import requests
import time
import uuid
from datetime import date, datetime

from PIL import Image
from django.conf import settings
from django.contrib import admin
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponseServerError, JsonResponse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView
from invitations import views as invitations_views
from invitations.adapters import get_invitations_adapter
from invitations.app_settings import app_settings as invitations_settings
from invitations.views import accept_invitation
from martor.utils import LazyEncoder
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (
    AccessRight,
    City,
    ExecutionStatus,
    Task,
    CapChecklist,
    AdministrationChecklist,
    EnergyPlanChecklist,
)

from .serializers import CitySerializer
from .serializers import TaskSerializer
from .serializers import TaskTopSerializer
from .serializers import TaskWithoutDraftModeSerializer


STATUS_ORDER = [
    ExecutionStatus.FAILED,
    ExecutionStatus.DELAYED,
    ExecutionStatus.AS_PLANNED,
    ExecutionStatus.COMPLETE,
    ExecutionStatus.UNKNOWN,
]

TO_STATUS = {status.value: status for status in ExecutionStatus}


def _get_task_groups(city):
    children = Task.get_root_nodes().filter(city=city)
    groups = children.filter(depth=1)
    return groups


def _get_cap_checklist(city) -> CapChecklist | None:
    try:
        return city.cap_checklist
    except CapChecklist.DoesNotExist:
        return None


def _get_administration_checklist(city) -> AdministrationChecklist | None:
    try:
        return city.administration_checklist
    except AdministrationChecklist.DoesNotExist:
        return None


def _get_energy_plan_checklist(city) -> EnergyPlanChecklist | None:
    try:
        return city.energy_plan_checklist
    except EnergyPlanChecklist.DoesNotExist:
        return None


@login_required
def markdown_uploader_view(request):
    if request.method != "POST":
        return HttpResponse(_("Invalid request!"))
    if "markdown-image-upload" not in request.FILES:
        return HttpResponse(_("Invalid request!"))

    image = request.FILES["markdown-image-upload"]
    image_types = ["image/png", "image/jpg", "image/jpeg", "image/pjpeg", "image/gif"]
    if image.content_type not in image_types:
        data = json.dumps(
            {
                "status": 415,
                "error": _(
                    "Unsupported image format. Supported formats: "
                    + ", ".join(image_types)
                ),
            },
            cls=LazyEncoder,
        )
        return HttpResponse(data, content_type="application/json", status=415)

    if image.size > settings.MAX_IMAGE_UPLOAD_SIZE:
        to_mb = settings.MAX_IMAGE_UPLOAD_SIZE / (1024 * 1024)
        data = json.dumps(
            {
                "status": 413,
                "error": _("Maximum image file is %(size)s MB.") % {"size": to_mb},
            },
            cls=LazyEncoder,
        )
        return HttpResponse(data, content_type="application/json", status=413)

    img_uuid = "{0}-{1}".format(uuid.uuid4().hex[:10], image.name.replace(" ", "-"))
    tmp_file = os.path.join(
        settings.MARTOR_UPLOAD_PATH, time.strftime("%Y/%m/%d/"), img_uuid
    )
    def_path = default_storage.save(tmp_file, ContentFile(image.read()))

    # restrict size to max 2000 width or height
    img_path = os.path.join(settings.MEDIA_ROOT, def_path)
    img = Image.open(img_path)
    if img.width > 2000 or img.height > 2000:
        img.thumbnail((2000, 2000))
        img.save(img_path)

    img_url = os.path.join(settings.MEDIA_URL, def_path)

    data = json.dumps({"status": 200, "link": img_url, "name": image.name})
    return HttpResponse(data, content_type="application/json")


def mstr_view(request, municipality_key):
    url = "https://www.marktstammdatenregister.de/MaStR/Einheit/EinheitJson/GetVerkleinerteOeffentlicheEinheitStromerzeugung"
    params = {
        "sort": "EinheitMeldeDatum-desc",
        "page": 1,
        "pageSize": 10000,
        "filter": f"Energieträger~eq~'2495'~and~Gemeindeschlüssel~eq~'{municipality_key}'",
    }
    try:
        r = requests.get(url, params)
    except:
        return HttpResponseServerError()

    data = r.json()["Data"]

    installed_by_year = dict()

    START_YEAR = 2019
    for entry in data:
        if not entry["InbetriebnahmeDatum"]:
            continue

        m = re.match("/Date\((-?\d*)\)/", entry["InbetriebnahmeDatum"])
        install_date = datetime.fromtimestamp(int(m.group(1)) / 1000)
        year = START_YEAR if install_date.year < START_YEAR else install_date.year

        if not year in installed_by_year:
            installed_by_year[year] = 0

        installed_by_year[year] += entry["Bruttoleistung"]

    current_year = date.today().year
    installed_accumulated = 0
    years = []
    installed = []
    for year, installed_in_year in sorted(installed_by_year.items()):
        if year == current_year:
            break
        installed_accumulated += round(installed_in_year)
        years.append(year)
        installed.append(installed_accumulated)

    data = json.dumps({"years": years, "installed": installed})
    return HttpResponse(data, content_type="application/json")


class AcceptInvite(invitations_views.AcceptInvite):
    "Overwrite handling of invitation link."

    def post(self, *args, **kwargs):
        """
        Unfortunately, the whole method had to be copied.
        Identical to base implementation, except where noted.
        """
        self.object = invitation = self.get_object()

        if invitations_settings.GONE_ON_ACCEPT_ERROR and (
            not invitation
            or (invitation and (invitation.accepted or invitation.key_expired()))
        ):
            return HttpResponse(status=410)

        if not invitation:
            get_invitations_adapter().add_message(
                self.request,
                messages.ERROR,
                "invitations/messages/invite_invalid.txt",
            )
            return redirect(invitations_settings.LOGIN_REDIRECT)

        if invitation.accepted:
            get_invitations_adapter().add_message(
                self.request,
                messages.ERROR,
                "invitations/messages/invite_already_accepted.txt",
                {"email": invitation.email},
            )
            return redirect(invitations_settings.LOGIN_REDIRECT)

        if invitation.key_expired():
            get_invitations_adapter().add_message(
                self.request,
                messages.ERROR,
                "invitations/messages/invite_expired.txt",
                {"email": invitation.email},
            )
            return redirect(self.get_signup_redirect())

        if not invitations_settings.ACCEPT_INVITE_AFTER_SIGNUP:
            accept_invitation(
                invitation=invitation,
                request=self.request,
                signal_sender=self.__class__,
            )
            # Difference: Revert accepted to allow reuse of link.
            invitation.accepted = False
            invitation.save()

        user: auth.models.User = self.request.user
        if user.is_authenticated:
            if user.is_active and user.is_staff:
                get_invitations_adapter().add_message(
                    self.request,
                    messages.SUCCESS,
                    "invitations/messages/invite_for_logged_in_user.txt",
                    {
                        "role": invitation.get_access_right_display(),
                        "city": invitation.city.name,
                        "username": user.username,
                    },
                )
                city: City = invitation.city
                if invitation.access_right == AccessRight.CITY_EDITOR:
                    city.city_editors.add(user.pk)
                elif invitation.access_right == AccessRight.CITY_ADMIN:
                    city.city_admins.add(user.pk)
                return redirect(invitations_settings.LOGIN_REDIRECT)
            else:
                get_invitations_adapter().add_message(
                    self.request,
                    messages.ERROR,
                    "invitations/messages/invite_for_logged_in_user_invalid.txt",
                    {"role": str(invitation), "username": user.username},
                )
                auth.logout(self.request)

        # Difference: Saving key and not email.
        self.request.session["invitation_key"] = invitation.key

        return redirect(self.get_signup_redirect())


# Admin
class SelectCityView(ListView):
    model = City
    template_name = "admin/admin-city.html"
    ordering = "name"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["title"] = "Städte"
        return context


class CapEditView(DetailView, admin.ModelAdmin):
    model = City
    template_name = "admin/admin-cap.html"

    def get_context_data(self, **kwargs):
        groups = _get_task_groups(self.object)
        cap_checklist = _get_cap_checklist(self.object)
        administration_checklist = _get_administration_checklist(self.object)
        energy_plan_checklist = _get_energy_plan_checklist(self.object)

        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        context["city_id"] = str(self.object.pk)
        context["cap_checklist_id"] = (
            cap_checklist.pk if cap_checklist != None else None
        )
        context["administration_checklist_id"] = (
            administration_checklist.pk if administration_checklist != None else None
        )
        context["energy_plan_checklist_id"] = (
            energy_plan_checklist.pk if energy_plan_checklist != None else None
        )
        context["groups"] = groups
        return context


def move_task(request, pk):
    new_parent_pk = request.POST.get("new_parent_pk")
    task = Task.objects.get(pk=pk)
    new_parent = Task.objects.get(pk=new_parent_pk)
    position = request.POST.get("position")
    task.move(new_parent, position)
    return JsonResponse({"success": True})


#
# REST API views
#


class CityList(APIView):
    """
    List all cities.
    """

    def get_execution_status_count(self, city, auth):
        # Get task execution status count for the city
        if auth:
            tasks = Task.objects.filter(city=city)
        else:
            tasks = Task.objects.filter(city=city, draft_mode=False)

        status_summary = {
            "complete": tasks.filter(execution_status=ExecutionStatus.COMPLETE).count(),
            "asPlanned": tasks.filter(
                execution_status=ExecutionStatus.AS_PLANNED
            ).count(),
            "delayed": tasks.filter(execution_status=ExecutionStatus.DELAYED).count(),
            "failed": tasks.filter(execution_status=ExecutionStatus.FAILED).count(),
            "unknown": tasks.filter(execution_status=ExecutionStatus.UNKNOWN).count(),
        }
        return status_summary

    def get(self, request):
        if request.user.is_authenticated:
            cities = City.objects.all().order_by("-last_update")
        else:
            cities = City.objects.filter(draft_mode=False).order_by("-last_update")

        execution_status_param = request.query_params.get("executionStatusCount", None)

        serializer = CitySerializer(cities, many=True)
        city_data = serializer.data

        if execution_status_param is not None:
            for city in city_data:
                city_instance = City.objects.get(id=city["id"])
                city["executionStatusCount"] = self.get_execution_status_count(
                    city_instance, request.user.is_authenticated
                )

        return Response(city_data)


class CityDetail(APIView):
    """
    Return a specific city.
    """

    def get(self, request, slug):
        try:
            if request.user.is_authenticated:
                city = City.objects.get(slug=slug)
            else:
                city = City.objects.get(slug=slug, draft_mode=False)
        except City.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CitySerializer(city)
        return Response(serializer.data)


class TasksByCity(APIView):
    """
    List all tasks of a city.
    """

    def get(self, request, slug):
        try:
            city = City.objects.get(slug=slug)
        except City.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        city_id = city.id
        if request.user.is_authenticated:
            children = Task.get_root_nodes().filter(city=city_id)
            serializer = TaskSerializer(children, many=True)
        else:
            children = Task.get_root_nodes().filter(city=city_id, draft_mode=False)
            serializer = TaskWithoutDraftModeSerializer(children, many=True)
        return Response(serializer.data)


class TasksTop(APIView):
    """
    List all top tasks.
    """

    def get(self, request):
        tasks = Task.objects.filter(draft_mode=False, source__gt=0)
        serializer = TaskTopSerializer(tasks, many=True)
        return Response(serializer.data)
