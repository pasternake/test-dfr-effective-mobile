from rest_framework import views
from rest_framework.response import Response
from permissions.permissions import HasResourcePermission

class DocumentListView(views.APIView):
    permission_classes = [HasResourcePermission]
    resource_name = 'document'

    def get(self, request):
        # Requires 'document.read'
        return Response([
            {"id": 1, "title": "Confidential Report"},
            {"id": 2, "title": "Project Plan"}
        ])

    def post(self, request):
        # Requires 'document.create'
        return Response({"message": "Document created successfully."})
