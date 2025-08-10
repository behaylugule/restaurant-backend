from django.shortcuts import render

from api.models import DinningTable, Menu, Shop
from orders.models import MenuRate, Order, OrderItem
from rest_framework import generics, permissions, status

from orders.serializers import KitchenDisplaySerializer, MenuRateSerializer, OrderItemSerializer, OrderSerializer
from utils.enum import USER_ROLE, ORDER_STATUS
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Avg, Sum




# Create your views here.


class OrderListCreateView(generics.ListCreateAPIView):
      serializer_class = OrderSerializer 
      permission_classes = [permissions.IsAuthenticated]
      queryset = Order.objects.all()
      search_fields=['user__username']


      def get_queryset(self):
           user = self.request.user
           if user.role == USER_ROLE.SHOP_ADMIN:
                self.queryset = self.queryset.filter(shop=user.shop).order_by('-create_date')
                status = self.request.query_params.get('status')
                order_date = self.request.query_params.get('order_date')
              
                if status is not None and status !="":
                    self.queryset = self.queryset.filter(status=status)
                if order_date is not None and order_date != "":
                     self.queryset = self.queryset.filter(create_date__date=order_date)

           elif user.role==USER_ROLE.USER:
                self.queryset = self.queryset.filter(user=user).order_by('-create_date')
           else:     
                shop = self.request.query_params.get('shop_id')
                self.queryset = self.queryset.filter(shop=shop)

           return self.queryset
      def perform_create(self, serializer):
           shop = Shop.objects.filter(id=self.request.data['shop']).first()
           diningTable = DinningTable.objects.filter(id=self.request.data['table_number']).first()
           order = Order.objects.create(
                shop=shop,
                user= self.request.user,
                total_price = self.request.data['total_price'],
                table_number = diningTable
           )
           order.save()
           for item in self.request.data['items']:
                menu = Menu.objects.filter(id=item['id']).first()
                orderItem =  OrderItem.objects.create(
                    shop= shop , 
                    order = order, 
                    menu = menu,
                    price = item['price'],
                    quantity=item['quantity']
                 )
                orderItem.save()
            
      
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
      serializer_class = OrderSerializer
      permission_classes = [permissions.IsAuthenticated]
      queryset = Order.objects.all().order_by('-create_date')
      def patch(self, request ,*args, **kwargs):
           instance = self.get_object()
           method = request.query_params.get('method')
          
           if method == 'cancled':
                if instance.status != ORDER_STATUS.PENDING:
                     raise ValidationError("The order status is not pending")
                instance.status = ORDER_STATUS.CANCLED
                instance.save()
                return Response({'data':'order Cancled'})
           if method == ORDER_STATUS.PROCESSING:
                if instance.status !=ORDER_STATUS.PENDING:
                     raise ValidationError('The order status is not pending')
                instance.status = ORDER_STATUS.PROCESSING
                instance.save()
           if method == ORDER_STATUS.READY:
                if instance.status != ORDER_STATUS.PROCESSING:
                    raise ValidationError('The order status is not Processing')
                instance.status = ORDER_STATUS.READY
                instance.save()
           if method == 'completed':
                if instance.status != ORDER_STATUS.READY:
                     raise ValidationError("The order status is not pending")
                instance.status = ORDER_STATUS.COMPLETED
                instance.save()
                return Response({'data':'order Completed'})
           return super().patch(request, *args, **kwargs)


class OrderItemListCreate(generics.ListCreateAPIView):
     serializer_class = OrderItemSerializer
     permission_classes = [permissions.IsAuthenticated]
     queryset = OrderItem.objects.all().order_by('-create_date')

     def get_queryset(self):
          order = self.request.query_params.get('order_id')
          
          if order is not None:
               self.queryset = self.queryset.filter(order=order)
          return self.queryset
     
class OrderItemDetail(generics.RetrieveUpdateDestroyAPIView):
      serializer_class = OrderItemSerializer
      permission_classes = [permissions.IsAuthenticated]
      queryset = OrderItem.objects.all()


class MenuRateListCreateView(generics.ListCreateAPIView):
      serializer_class = MenuRateSerializer
      permission_classes = [permissions.IsAuthenticated]
      queryset = MenuRate.objects.all().order_by('-create_date')


      def get_queryset(self):
           order_id = self.request.query_params.get('order_id')
           menu_id = self.request.query_params.get('menu_id')
           user = self.request.user

           if menu_id is not None:
                self.queryset = self.queryset.filter(menu=menu_id)
           if order_id is not None:
                self.queryset = self.queryset.filter(order=order_id)

           if user.role == USER_ROLE.SHOP_ADMIN:
                self.queryset = self.queryset.filter(shop=user.shop)
           return self.queryset
      
      def patch(self, request, *args, **kwargs):
           method = self.request.query_params.get('method') 
           menu = self.request.data['id']
           if method== 'average_rate':
                average_rate = MenuRate.objects.filter(menu=menu).aggregate(avg_rate=Avg('rate'))['avg_rate']
                total_order = OrderItem.objects.filter(menu=menu).aggregate(total=Sum('quantity'))['total']

                return Response({'average_rate':average_rate,'total_order':total_order})  
           return Response({})
      
      def perform_create(self, serializer):
           if MenuRate.objects.filter(user=self.request.user, menu=serializer.validated_data['menu'],order=serializer.validated_data['order']).exists():
                raise ValidationError("you have already rated this menu")
           serializer.save(user=self.request.user)
           return super().perform_create(serializer)

class MenuRateDetailView(generics.RetrieveUpdateDestroyAPIView):
      serializer_class = MenuRateSerializer
      permission_classes = [permissions.IsAuthenticated]
      queryset = MenuRate.objects.all().order_by('-create_date')

  
class KitchenDisplayListView(generics.ListAPIView):
    serializer_class = KitchenDisplaySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        self.queryset =Order.objects.filter(shop=self.request.user.shop).prefetch_related('order_items')
        status = self.request.query_params.get('status')
        if status is not None:
             self.queryset = self.queryset.filter(status=status)
        return  self.queryset
