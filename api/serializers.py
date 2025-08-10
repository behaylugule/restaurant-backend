from rest_framework import serializers
from .models import  ChatRoom, DinningTable, Menu, MenuCategory,  Organization, Shop, UploadedFile,Message
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    org_name = serializers.CharField(source='organization.name',read_only=True)
    shop_name = serializers.CharField(source='shop.name', read_only=True)

    class Meta:
        model = User
        fields = ('id','username','first_name','middle_name','last_name','contact_number', 'email','role', 'password','organization','shop','org_name','shop_name')
        extra_kwargs = {
            'password': {'write_only': True}, # This is good practice for passwords
            'role': {'required': False} # Role might be optional during registration
        }


    def create(self, validated_data):
        # Extract password and role explicitly, providing a default for role
        username = validated_data.pop('username') # <-- POP USERNAME
        email = validated_data.pop('email')       # <-- POP EMAIL
        password = validated_data.pop('password')
        role = validated_data.pop('role', 'user') # Pop role, with a default
        request = self.context.get('request')  # Access the request
        organization = None
        if request and request.user.is_authenticated:
            if request.user['organization']:
                organization = request.user.organization 



        # Create the user, using the popped values as keyword arguments
        user = User.objects.create_user(
            username=username, # Use the popped username
            email=email,       # Use the popped email
            password=password,
            role=role,
           
            **validated_data   
        )

        if organization:
            user.organization = organization
            user.save()
        return user
    
class PasswardChangeSerializer(serializers.Serializer):
       old_password = serializers.CharField(required=True)
       new_password = serializers.CharField(required=True)


class UploadedFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = UploadedFile
        fields = ['id', 'title', 'file', 'file_url']  # include file_url

    def get_file_url(self, obj):
        request = self.context.get('request')
        if hasattr(obj, 'file'):
            return request.build_absolute_uri(obj.file.url)
        return None




    
class OrganizationSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Organization
        fields = '__all__'
        
class ShopSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    logo_url = serializers.CharField(source='shop_logo.file',read_only=True)
    

    class Meta:
        model = Shop
        fields = '__all__'

class DinningTableSerializer(serializers.ModelSerializer):
     shop_name = serializers.CharField(source='shop.name', read_only=True)


     class Meta:
          model = DinningTable
          fields = '__all__'

class GlobalCountSerializer(serializers.Serializer):
       total_organizations = serializers.IntegerField()
       total_shops = serializers.IntegerField()
       total_users = serializers.IntegerField() 
     



class MenuCategorySerializer(serializers.ModelSerializer):
     image_url = serializers.CharField(source='image.file',read_only=True)
     shop_name = serializers.CharField(source='shop.name', read_only=True)
     class Meta:
         model = MenuCategory
         fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(source='image.file',read_only=True)
    shop_name = serializers.CharField(source='shop.name',read_only =True)
    category_name = serializers.CharField(source='menu_category.name',read_only = True)

    class Meta:
         model = Menu
         fields = '__all__'


class ChatRoomSerializer(serializers.ModelSerializer):
     shop_name = serializers.CharField(source = "shop.name")
     client_name = serializers.CharField(source='client.username')

     class Meta:
          model = ChatRoom
          fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
        room_name = serializers.CharField(source='room.shop__name',read_only=True)
        username = serializers.CharField(source='user.username', read_only=True)

        class Meta:
             model = Message
             fields = '__all__'
