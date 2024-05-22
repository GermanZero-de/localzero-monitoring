from cpmonitor.models import City, LocalGroup
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


class CitySerializer(serializers.ModelSerializer):
    local_group = LocalGroupSerializer(read_only=True)

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
        ]
