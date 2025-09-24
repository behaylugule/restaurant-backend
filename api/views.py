# Step 6: views.py (api/views.py)
import random
import string
from rest_framework import generics, permissions, status

from utils.enum import USER_ROLE, ORDER_STATUS
from .models import DinningTable, Organization, CustomUser, Organization, Shop
from .serializers import DinningTableSerializer, GlobalCountSerializer, OrganizationSerializer, OrganizationSerializer, ShopSerializer, UploadedFileSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model


User = get_user_model()


class OrganizationListCreateView(generics.ListCreateAPIView):
        serializer_class = OrganizationSerializer
        permission_classes = [permissions.IsAuthenticated]
        queryset = Organization.objects.all().order_by('-create_date')
        search_fields = ['name','address','code','contact_number','description']

        def get_queryset(self):
            if self.request.user.role=='admin':
                return self.queryset
            else:
                return self.queryset

        def perform_create(self, serializer):
            serializer.save()

class FileUploadCreateView(generics.ListCreateAPIView):
      serializer_class = UploadedFileSerializer

      def get_serializer_context(self):
        return {'request': self.request}

      def perform_create(self, serializer):
            serializer.save()

class OrganizationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset


class ShopListCreateView(generics.ListCreateAPIView):
      queryset = Shop.objects.all()
      serializer_class = ShopSerializer
      permission_classes = [permissions.IsAuthenticated]
      search_fields = ['name','description']

      def get_queryset(self):
           return self.queryset.filter(organization=self.request.user.organization)

      def perform_create(self, serializer):
           organization = serializer.validated_data['organization']
           serializer.validated_data['shop_key'] = self.generateShopKey()
           serializer.validated_data['code'] = self.generateCode(organization)
       
           return super().perform_create(serializer)

      def generateShopKey(self):
            length = 8
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            return random_string
      
      def generateCode(self,organization):
            length = 8
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            random_string = organization.name + '-' + random_string
            return random_string


class ShopDetailView(generics.RetrieveUpdateDestroyAPIView):
      queryset = Shop.objects.all().order_by('-create_date')
      serializer_class = ShopSerializer
      permission_classes = [permissions.IsAuthenticated]
     


class GlobalCountListView(generics.RetrieveAPIView):
      
      serializer_class = GlobalCountSerializer
      permission_classes = [permissions.IsAuthenticated]

      def get(self, request, *args, **kwargs):
           
           users = User.objects.count()
           shops = Shop.objects.count()
           organizations = Organization.objects.count()

           data =  {
                'total_users':users,
                'total_shops':shops,
                'total_organizations':organizations
           }
           
           serializer = GlobalCountSerializer(data=data)
           serializer.is_valid(raise_exception=True) 
        
           return Response(serializer.data, status=status.HTTP_200_OK)

         

class ShopListRetrive(generics.ListAPIView):
      serializer_class = ShopSerializer
      permission_classes =[permissions.AllowAny]
      queryset = Shop.objects.all()


class DinningTableCreateListView(generics.ListCreateAPIView):
      serializer_class = DinningTableSerializer
      permission_classes = [permissions.IsAuthenticated]
      queryset = DinningTable.objects.all()
      search_fields = ['name']

      def perform_create(self, serializer):
            serializer.validated_data['shop']=self.request.user.shop
            serializer.save()

      def get_queryset(self):
           if self.request.user.role == USER_ROLE.SHOP_ADMIN:
                self.queryset = self.queryset.filter(shop=self.request.user.shop)
                return self.queryset
           else:
                shop_id = self.request.query_params.get('shop_id')
                self.queryset= self.queryset.filter(shop=shop_id)
           return self.queryset
class DinningTableRetrieveDetailView(generics.RetrieveUpdateDestroyAPIView):
      serializer_class = DinningTableSerializer
      permission_classes=[permissions.IsAuthenticated]
      queryset = DinningTable.objects.all()

      

     
    