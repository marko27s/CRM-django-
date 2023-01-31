from rest_framework import serializers

from accounts.serializer import AccountSerializer
from cases.models import Case
from common.serializer import OrganizationSerializer, ProfileSerializer
from contacts.serializer import ContactSerializer
from teams.serializer import TeamsSerializer


class CaseSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    contacts = ContactSerializer(read_only=True, many=True)
    assigned_to = ProfileSerializer(read_only=True, many=True)
    created_by = ProfileSerializer(read_only=True)
    teams = TeamsSerializer(read_only=True, many=True)
    org = OrganizationSerializer()

    class Meta:
        model = Case
        fields = (
            "id",
            "name",
            "status",
            "priority",
            "case_type",
            "closed_on",
            "description",
            "created_by",
            "created_on",
            "is_active",
            "account",
            "contacts",
            "teams",
            "assigned_to",
            "org",
            "created_on_arrow",
        )


class CaseCreateSerializer(serializers.ModelSerializer):
    closed_on = serializers.DateField

    def __init__(self, *args, **kwargs):
        request_obj = kwargs.pop("request_obj", None)
        super().__init__(*args, **kwargs)
        self.org = request_obj.org

    def validate_name(self, name):
        if self.instance:
            if (
                Case.objects.filter(name__iexact=name, org=self.org)
                .exclude(id=self.instance.id)
                .exists()
            ):
                raise serializers.ValidationError("Case already exists with this name")

        else:
            if Case.objects.filter(name__iexact=name, org=self.org).exists():
                raise serializers.ValidationError("Case already exists with this name")
        return name

    class Meta:
        model = Case
        fields = (
            "name",
            "status",
            "priority",
            "description",
            "created_by",
            "created_on",
            "is_active",
            "account",
            "org",
            "created_on_arrow",
        )
