from rest_framework import generics, permissions
from .models import Menu, MenuCategory
from .serializers import MenuCategorySerializer, MenuSerializer
from api.models import Shop


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
           if menu_category is not None and menu_category != "":
                 self.queryset = self.queryset.filter(menu_category = menu_category)
           return self.queryset
      
      def perform_create(self, serializer):
           serializer.validated_data['shop']=self.request.user.shop
           serializer.save()

class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):
      serializer_class = MenuSerializer
      permissions_classes = [permissions.IsAuthenticated]
      queryset = Menu.objects.all()


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