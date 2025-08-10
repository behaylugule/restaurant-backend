from django.db import models

from api.models import CustomUser, DinningTable, Menu, Shop
from utils.commons_model import CommonsModel
from utils.enum import ORDER_STATUS

# Create your models here.

class Order(CommonsModel):
      user = models.ForeignKey(CustomUser,null=False,blank=True,on_delete=models.CASCADE, related_name="user_order")
      shop = models.ForeignKey(Shop,null=False, blank=True, on_delete=models.CASCADE, related_name="shop_with_order")
      total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=True)
      status = models.CharField(max_length=30, choices=ORDER_STATUS.choices, default=ORDER_STATUS.PENDING)
      table_number = models.ForeignKey(DinningTable, null=False, blank=False, on_delete=models.CASCADE, related_name="table_number_order")

      def __str__(self):
          return self.user.username
      

class OrderItem(CommonsModel):
      shop = models.ForeignKey(Shop, null=False, blank=True, on_delete=models.CASCADE, related_name="shop_order_item")
      order = models.ForeignKey(Order,null=False, blank=False,on_delete= models.CASCADE, related_name="order_items")
      menu = models.ForeignKey(Menu, null=False, blank=False, on_delete=models.CASCADE, related_name="menu_order_items")
      price= models.DecimalField(max_digits=10,decimal_places=2)
      quantity = models.IntegerField(default=0)


      def __str__(self):
          return self.menu.name

class MenuRate(CommonsModel):
      menu = models.ForeignKey(Menu, null=False, blank=False, on_delete=models.CASCADE, related_name="menu_rate")
      rate = models.IntegerField(default=5)
      user = models.ForeignKey(CustomUser, null=False, blank=True, on_delete=models.CASCADE, related_name='menu_rate_user')
      shop = models.ForeignKey(Shop, null= False, blank=False, on_delete=models.CASCADE, related_name='menu_rate_shop')
      comment = models.TextField(blank=True, null=True)
      order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='menu_rate_order')

      def __str__(self):
           return self.menu.name
