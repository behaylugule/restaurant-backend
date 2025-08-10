# Step 6: views.py (api/views.py)
import random
import string
from rest_framework import generics, permissions, status

from utils.enum import USER_ROLE, ORDER_STATUS
from .models import ChatRoom, DinningTable, Menu, MenuCategory, Message , Organization, CustomUser, Organization, Shop
from .serializers import ChatRoomSerializer, DinningTableSerializer, GlobalCountSerializer, MenuCategorySerializer, MenuSerializer, MessageSerializer,  OrganizationSerializer, OrganizationSerializer, PasswardChangeSerializer, RegisterSerializer, ShopSerializer, UploadedFileSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError


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
           if role is not None and role !="":
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
    
    users= User.objects.all()
   
    return Response(serializer.data)
    

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = PasswardChangeSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return User.objects.filter(id=self.request.user.id)
        return User.objects.none() # Return an empty queryset if user is not authenticated

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
     

class MenuCategoryListCreateView(generics.ListCreateAPIView):
      serializer_class = MenuCategorySerializer
      permission_classes = [permissions.IsAuthenticated]     
      queryset = MenuCategory.objects.all().order_by('-create_date')
      search_fields = ['name']

      def get_queryset(self):
          return self.queryset.filter(shop = self.request.user.shop)   
      
      def perform_create(self, serializer):
          serializer.validated_data['shop'] = self.request.user.shop
          serializer.save()

class MenuCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
        serializer_class = MenuCategorySerializer
        queryset = MenuCategory.objects.all().order_by('-create_date')
        permission_classes = [permissions.IsAuthenticated]


class MenuListCreateView(generics.ListCreateAPIView):
      serializer_class = MenuSerializer
      permissions_classes = [permissions.IsAuthenticated]
      queryset = Menu.objects.all().order_by('-create_date')
      search_fields = ["name"]

      def get_queryset(self):
           menu_category = self.request.query_params.get('menu_category')
           self.queryset = self.queryset.filter(shop = self.request.user.shop)
           if menu_category is not None and menu_category !="":
                 self.queryset = self.queryset.filter(menu_category = menu_category)
           return self.queryset
      
      def perform_create(self, serializer):
           serializer.validated_data['shop']=self.request.user.shop
           serializer.save()

class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):
      serializer_class = MenuSerializer
      permissions_classes = [permissions.IsAuthenticated]
      queryset = Menu.objects.all()

      

     
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
      
      

class MenuCategoryListRetrive(generics.ListAPIView):
      serializer_class = MenuCategorySerializer
      permission_classes = [permissions.AllowAny]
      queryset = MenuCategory.objects.all()

      

      def get_queryset(self):
           shop_id = self.kwargs.get('pk')
           if shop_id:
                self.queryset = self.queryset.filter(shop__id = shop_id)
           return self.queryset


class MenuListRetrive(generics.ListAPIView):
      serializer_class = MenuSerializer
      permission_classes = [permissions.AllowAny]
      queryset = Menu.objects.all()
      search_field = ['name','description']

      def get_queryset(self):
           shop_id = self.kwargs.get('pk')
           category_id = self.request.query_params.get('category_id')
           
           if category_id:
                self.queryset = self.queryset.filter(menu_category__id = category_id)

           if shop_id:
                self.queryset = self.queryset.filter(shop__id = shop_id)

            
     
           return self.queryset


class ChatRoomCreateListView(generics.ListCreateAPIView):
      serializer_class = ChatRoomSerializer
      permission_classes = [permissions.IsAuthenticated]
      queryset = ChatRoom.objects.all()

      def get_queryset(self):
           if self.request.user.role == USER_ROLE.USER:
                self.queryset = self.queryset.filter(client = self.request.user)
                shop_id = self.request.query_params.get('shop_id')
                if shop_id is not None:
                     self.queryset = self.queryset.filter(shop=shop_id)
                     if self.queryset.count() == 0:
                         shop = Shop.objects.filter(id=shop_id).first()
                         chatroom =   ChatRoom.objects.create(
                             client = self.request.user,
                             shop = shop                      
                                 ) 
                         chatroom.save()
                         self.queryset.filter(shop=shop_id,client=self.request.user) 
           elif self.request.user.role == USER_ROLE.SHOP_ADMIN:
                self.queryset = self.queryset.filter(shop=self.request.user.shop)
           return self.queryset
             

class MessageListView(generics.ListAPIView):
      serializer_class = MessageSerializer
      permission_classes = [permissions.IsAuthenticated]
      queryset = Message.objects.all().order_by('-create_date')


      def get_queryset(self):
           
           
           room_id = self.request.query_params.get('room_id')
           if room_id is not None:
                self.queryset = self.queryset.filter(room=room_id)
           return self.queryset
      


    