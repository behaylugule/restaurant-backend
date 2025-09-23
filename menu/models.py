from django.db import models
from utils.commons_model import CommonsModel
from api.models import UploadedFile, Shop


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