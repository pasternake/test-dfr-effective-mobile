from rest_framework import serializers
from .models import Role, Resource, Action, Permission
from django.contrib.auth import get_user_model

User = get_user_model()

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    resource_code = serializers.CharField(source='resource.code', read_only=True)
    action_code = serializers.CharField(source='action.code', read_only=True)

    class Meta:
        model = Permission
        fields = ('id', 'resource', 'action', 'resource_code', 'action_code')

class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    permission_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = Role
        fields = ('id', 'name', 'permissions', 'permission_ids')

    def create(self, validated_data):
        permission_ids = validated_data.pop('permission_ids', [])
        role = Role.objects.create(**validated_data)
        role.permissions.set(permission_ids)
        return role

    def update(self, instance, validated_data):
        permission_ids = validated_data.pop('permission_ids', None)
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        if permission_ids is not None:
            instance.permissions.set(permission_ids)
        return instance

class AssignRoleSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    role_ids = serializers.ListField(child=serializers.IntegerField())

    def validate_user_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exist.")
        return value

    def validate_role_ids(self, value):
        if not Role.objects.filter(id__in=value).count() == len(set(value)):
             raise serializers.ValidationError("One or more roles do not exist.")
        return value
