from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, ResourceViewSet, AssignRoleView

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'resources', ResourceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('assign/', AssignRoleView.as_view(), name='assign-role'),
]
