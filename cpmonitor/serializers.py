from cpmonitor.models import (
    City,
    LocalGroup,
    CapChecklist,
    AdministrationChecklist,
    EnergyPlanChecklist,
    Task,
)
from rest_framework import serializers

#
# REST API serializers which are used in views.py by CityList, CityDetail etc.
#


class LocalGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalGroup
        fields = [
            "id",
            "name",
            "website",
            "teaser",
            "description",
            "logo",
            "featured_image",
        ]


def checklistToRepresentation(instance):
    checkbox_items = [
        field
        for field in instance._meta.fields
        if field.attname not in ["city_id", "id"] and "_rationale" not in field.attname
    ]

    return [
        {
            "id": idx,
            "question": checkbox_item.verbose_name,
            "is_checked": getattr(instance, checkbox_item.attname),
            "help_text": checkbox_item.help_text,
            "rationale": getattr(instance, checkbox_item.attname + "_rationale"),
        }
        for idx, checkbox_item in enumerate(checkbox_items)
    ]


class CapChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapChecklist
        fields = "__all__"

    def to_representation(self, instance):
        super().to_representation(instance)
        return checklistToRepresentation(instance)


class AdministrationChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrationChecklist
        fields = "__all__"

    def to_representation(self, instance):
        super().to_representation(instance)
        return checklistToRepresentation(instance)


class EnergyPlanChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyPlanChecklist
        fields = "__all__"

    def to_representation(self, instance):
        super().to_representation(instance)
        return checklistToRepresentation(instance)


class CitySerializer(serializers.ModelSerializer):
    local_group = LocalGroupSerializer(read_only=True)
    cap_checklist = CapChecklistSerializer(read_only=True)
    administration_checklist = AdministrationChecklistSerializer(read_only=True)
    energy_plan_checklist = EnergyPlanChecklistSerializer(read_only=True)

    class Meta:
        model = City
        fields = [
            "id",
            "draft_mode",
            "name",
            "municipality_key",
            "url",
            "resolution_date",
            "target_year",
            "teaser",
            "description",
            "assessment_status",
            "contact_name",
            "contact_email",
            "supporting_ngos",
            "slug",
            "local_group",
            "cap_checklist",
            "administration_checklist",
            "energy_plan_checklist",
            "assessment_action_plan",
            "assessment_administration",
        ]


class TaskSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "draft_mode",
            "title",
            "city",
            "teaser",
            "description",
            "planned_start",
            "planned_completion",
            "responsible_organ",
            "responsible_organ_explanation",
            "plan_assessment",
            "execution_status",
            "execution_justification",
            "supporting_ngos",
            "execution_completion",
            "actual_start",
            "actual_completion",
            "internal_information",
            "slugs",
            "numchild",
            "children",
            "source",
            "frontpage",
        ]

    def get_children(self, obj):
        children = obj.get_children()
        serializer = TaskSerializer(children, many=True)
        return serializer.data


class TaskWithoutDraftModeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "draft_mode",
            "title",
            "city",
            "teaser",
            "description",
            "planned_start",
            "planned_completion",
            "responsible_organ",
            "responsible_organ_explanation",
            "plan_assessment",
            "execution_status",
            "execution_justification",
            "supporting_ngos",
            "execution_completion",
            "actual_start",
            "actual_completion",
            "internal_information",
            "slugs",
            "numchild",
            "children",
        ]

    def get_children(self, obj):
        children = obj.get_children().exclude(draft_mode=True)
        serializer = TaskSerializer(children, many=True)
        return serializer.data
