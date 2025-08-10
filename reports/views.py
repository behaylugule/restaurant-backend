from django.shortcuts import render
from rest_framework import generics, permissions


from api.models import Shop
from api.serializers import MenuSerializer, OrganizationSerializer, ShopSerializer
from orders.models import Order
from orders.serializers import KitchenDisplaySerializer, OrderSerializer
from .tasks import menu_generate_report, order_detail_generate_report, order_generate_report, organization_generate_report, shop_generate_report, users_generate_report
from rest_framework.response import Response
# Create your views here.

class UserReportViews(generics.ListAPIView):
     permission_classes = [permissions.IsAuthenticated]

     def patch(self, request):
         search = request.data.get('search')
         role = request.data.get('role')
         users_generate_report(request.user.id,role, search)
         return Response({'message':'User List report has been Processing'})

class OrganizationReportViews(generics.ListAPIView):
   
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request):
        search = request.data.get('search')
        organization_generate_report(request.user.id, search)
        return Response({'message':'Organizations List report has been processing'})

class ShopReportViews(generics.ListAPIView):
    serializer_class  = ShopSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Shop.objects.all()
    search_fields = ['name']
    def patch(self, request):
        search = request.data.get('search')
        shop_generate_report.delay(request.user.id, search)
        return Response({'message':'Shop List report has been processing'})

class MenuReportViews(generics.ListAPIView):
      serializer_class = MenuSerializer
      permission_classes = [permissions.IsAuthenticated]
      queryset = Order.objects.all()
      search_fields = ['name']

      def patch(self, request):
          menu_category = None
          if self.request.data.get('menu_category') is not None:
              menu_category = self.request.data.get('menu_category')
          menu_generate_report.delay(request.user.id,menu_category)
          return Response({'message':'Menu report has been processing'})


class OrderReportViews(generics.ListAPIView):
      serializer_class = OrderSerializer 
      permission_classes = [permissions.IsAuthenticated]
      queryset = Order.objects.all()
     

      def patch(self, request):
        
        order_date = None
        status = None

        if self.request.data.get('order_date') is not None:
            order_date = self.request.data.get('order_date')

        if self.request.data.get('status') is not None:
            status = self.request.data.get('status')

        order_generate_report.delay(request.user.id, order_date, status)
        return Response({'message':'Order report has been processing '})

class OrderDetailReportViews(generics.RetrieveAPIView):
     serializer_class = KitchenDisplaySerializer
     permission_classes = [permissions.IsAuthenticated]
     queryset = Order.objects.all()

     def get(self,request,*args,**kwags):
         
         order_detail_generate_report.delay(self.request.user.id,kwags.get('pk'))
         return Response({'message':'Order Report has been proccessing'})
     
