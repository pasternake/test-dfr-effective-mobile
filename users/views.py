from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserSerializer, UserUpdateSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            if not user.is_active:
                return Response({"error": "Account is disabled."}, status=status.HTTP_403_FORBIDDEN)
            login(request, user)
            return Response({"message": "Logged in successfully."})
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(views.APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully."})

class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        logout(self.request)
