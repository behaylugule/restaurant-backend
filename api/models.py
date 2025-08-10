from django.db import models
from utils.commons_model import CommonsModel
from django.contrib.auth.models import AbstractUser
from utils.enum import MESSAGE_SENDER, ORDER_STATUS, USER_ROLE


class CustomUser(AbstractUser):
    # Define choices for user roles
   
    # Add a role field to the user model
    role = models.CharField(max_length=50, choices=USER_ROLE.choices, default=USER_ROLE.USER)
    first_name = models.CharField(max_length=50,null=True, blank=True)
    middle_name = models.CharField(max_length=50,null=True, blank=True)
    last_name = models.CharField(max_length=50,null=True, blank=True)
    contact_number = models.CharField(max_length=50,null=True, blank=True)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, null=True, blank=True)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.username


    groups = None
    user_permissions = None
    def __str__(self):
        return self.username
    

class UploadedFile(CommonsModel):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/')
    
    def __str__(self):
        return self.title

class Organization(CommonsModel):
    name=models.CharField(max_length=200)
    code=models.CharField(max_length=100)
    description=models.TextField()
    address=models.CharField(max_length=200)
    contact_number=models.CharField(max_length=200)
    website=models.URLField(null=True, blank=True)
   
    def __str__(self):
        return self.name
    

class Shop(CommonsModel):
    name=models.CharField(max_length=200)
    code=models.CharField(max_length=100,blank=True)
    shop_key=models.CharField(max_length=100, blank=True)
    description=models.TextField()
    organization=models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='shops')
    shop_logo = models.ForeignKey(UploadedFile, null=True, on_delete=models.SET_NULL,related_name="shop_logo")
    lng = models.FloatField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    address = models.CharField(null=True, blank=True)
    

    def __str__(self):
        return self.name
    

class DinningTable(CommonsModel):
      name = models.CharField(max_length=20, blank=False, null=False)
      table_number = models.CharField(max_length=20, blank=False, null=False)
      shop = models.ForeignKey(Shop, blank=True, null=False, on_delete=models.CASCADE, related_name="dinning_table_shop")
      number_set = models.IntegerField(default=0)

      def __str__(self):
           return self.name



class MenuCategory(CommonsModel):
      name = models.CharField(max_length=100)
      description = models.TextField()
      image = models.ForeignKey(UploadedFile, null=True, on_delete=models.SET_NULL, related_name='category_image')
      shop = models.ForeignKey(Shop, blank=True, on_delete=models.CASCADE, related_name="shop_cate")

      def __str__(self):
          return super().__str__()    
      

class Menu(CommonsModel):
      name  = models.CharField(max_length=100)
      description = models.TextField()
      image = models.ForeignKey(UploadedFile, null=True, on_delete= models.SET_NULL, related_name='menu_image')
      shop = models.ForeignKey(Shop, null=True, on_delete= models.SET_NULL, related_name='shop_menu')
      menu_category = models.ForeignKey(MenuCategory, blank=True, on_delete=models.CASCADE, related_name="menu_category")
      price = models.DecimalField(max_digits=10,decimal_places=2, default=0)
      is_active = models.BooleanField(default=True)
      preparation_time = models.IntegerField(null=False,blank=False)

      def __str__(self):
         return super().__str__()
      


class ChatRoom(CommonsModel):
      client = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE, related_name='client_chat')
      shop = models.ForeignKey(Shop, null=False, blank=False, on_delete=models.CASCADE, related_name='shop_chat')

      def __str__(self):
           return self.client.username + " - " + self.shop.name      

class Message (CommonsModel):
      room = models.ForeignKey(ChatRoom, null=False, blank=False, on_delete=models.CASCADE, related_name='room_message')
      user = models.ForeignKey(CustomUser, null=False, blank=False,  on_delete=models.CASCADE, related_name='sender_message')
      text= models.TextField(blank=True, null=True)
      sender = models.CharField(max_length=20, choices=MESSAGE_SENDER.choices, default=MESSAGE_SENDER.USER)

      def __str__(self):
           return self.sender.username 


      