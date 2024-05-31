from cpmonitor.models import City, LocalGroup, CapChecklist
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


class CapChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapChecklist
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        checkbox_items = [
            field
            for field in instance._meta.fields
            if field.attname not in ["city_id", "id"]
            and "_rationale" not in field.attname
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


class CitySerializer(serializers.ModelSerializer):
    local_group = LocalGroupSerializer(read_only=True)
    cap_checklist = CapChecklistSerializer(read_only=True)

    class Meta:
        model = City
        fields = [
            "id",
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
            "assessment_action_plan",
        ]
