from rest_framework import serializers

from orders.models import MenuRate, Order, OrderItem



class OrderSerializer(serializers.ModelSerializer):
       username = serializers.CharField(source='user.username',read_only=True)
       shop_name = serializers.CharField(source='shop.name',read_only=True)
       table_number_no = serializers.CharField(source='table_number.table_number',read_only=True)
       table_number_name = serializers.CharField(source='table_number.name',read_only=True)
       class Meta:
            model = Order
            fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
       
       menu_name = serializers.CharField(source='menu.name', read_only=True)
       shop_name = serializers.CharField(source='shop.name', read_only=True)
       menu_url = serializers.CharField(source='menu.image.file', read_only=True)

       class Meta:
             model = OrderItem
             fields = '__all__'

class MenuRateSerializer(serializers.ModelSerializer):
       menu_name = serializers.CharField(source='menu.name', read_only=True)
       shop_name = serializers.CharField(source='shop.name', read_only=True)
       username = serializers.CharField(source='user.username', read_only=True)
       class Meta:
            model = MenuRate
            fields = '__all__'



class KitchenDisplaySerializer(serializers.ModelSerializer):
     order_items = OrderItemSerializer(many=True,read_only=True)
     username = serializers.CharField(source='user.username',read_only=True)
     shop_name = serializers.CharField(source='shop.name',read_only=True)
     table_number_no = serializers.CharField(source='table_number.table_number',read_only=True)
     table_number_name = serializers.CharField(source='table_number.name',read_only=True)
     class Meta:
          model = Order
          fields = '__all__'