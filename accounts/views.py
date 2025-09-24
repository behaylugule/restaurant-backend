from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from utils.enum import USER_ROLE
from api.models import CustomUser
from .serializers import RegisterSerializer, PasswardChangeSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class RetrieveUser(generics.ListAPIView):
      queryset = CustomUser.objects.all()
      serializer_class = RegisterSerializer
      permission_classes = [permissions.IsAuthenticated]
      search_fields = ['username']

      def get_queryset(self):
           user = self.request.user
           role = self.request.query_params.get('role')
           if user.role == USER_ROLE.ORGANIZATION_ADMIN:
                self.queryset = self.queryset.filter(organization=user.organization)
           if role is not None and role != "":
                 self.queryset = self.queryset.filter(role=role)
           return self.queryset


class UpdateUser(generics.UpdateAPIView):
     queryset = CustomUser.objects.all()
     serializer_class = RegisterSerializer
     permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
def me_view(request):
    user = request.user
    serializer = RegisterSerializer(user)
    return Response(serializer.data)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = PasswardChangeSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return User.objects.filter(id=self.request.user.id)
        return User.objects.none()

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            if not user.check_password(old_password):
                return Response({"error":"Old password is incorrect"})
            user.set_password(new_password)
            user.save()
            return Response({"message":"Password change successfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 