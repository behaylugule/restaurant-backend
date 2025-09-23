from rest_framework import serializers
from .models import MenuCategory, Menu


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