from cpmonitor.models import City
from rest_framework import serializers

#
# REST API serializers which are used in views.py by CityList, CityDetail etc.
#


class CitySerializer(serializers.ModelSerializer):
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
        ]
