from rest_framework import viewsets, views, status
from rest_framework.response import Response
from .models import Role, Resource, Permission
from .serializers import RoleSerializer, ResourceSerializer, AssignRoleSerializer
from .permissions import IsAdminUser
from django.contrib.auth import get_user_model

User = get_user_model()

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminUser]

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [IsAdminUser]

class AssignRoleView(views.APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = AssignRoleSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(id=serializer.validated_data['user_id'])
            roles = Role.objects.filter(id__in=serializer.validated_data['role_ids'])
            user.roles.set(roles)
            return Response({"message": "Roles assigned successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
