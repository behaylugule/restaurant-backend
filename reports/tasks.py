import datetime
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Q

from api.models import CustomUser, Menu, Organization, Shop
from api.serializers import MenuSerializer, OrganizationSerializer, RegisterSerializer, ShopSerializer
from orders.models import Order
from orders.serializers import KitchenDisplaySerializer, OrderSerializer
from utils.enum import USER_ROLE
from utils.file_utils import render_to_pdf

@shared_task
def users_generate_report(user_id,role,search):
     current_user = CustomUser.objects.get(id=user_id)
     if search is None:
          search = ""
     users = CustomUser.objects.filter(username__icontains=search)
     if current_user.role ==USER_ROLE.ORGANIZATION_ADMIN:
          users = users.filter(Q(role = USER_ROLE.SHOP_ADMIN)&Q(organization=current_user.organization))
     if role is not None and role != "":
          users = users.filter(role=role)
     serialized_data = RegisterSerializer(users, many=True).data
     total = users.count()
     date = datetime.datetime.now()
     template_name = "reports/users-list.html"
     items = {"data":serialized_data, "date":date, "total":total, 'title':f"User List", "print_by":current_user,"shop_name":""}
     pdf_base64 = render_to_pdf(template_name,items)
     channel_layer = get_channel_layer()
     async_to_sync(channel_layer.group_send)(
          f'reports_for_{current_user.id}',
          {
               'type':'send_report',
               'report':{
                    'filename':'order_report.pdf',
                    'file':pdf_base64
               }
          }
     )
@shared_task
def organization_generate_report(user_id,search):
     user = CustomUser.objects.get(id=user_id)
     organizations = Organization.objects.all()
     if search is not None and search !="":
          organizations = organizations.filter(name__icontains=search)
     serialized_data = OrganizationSerializer(organizations, many=True).data
     total = organizations.count()
     date = datetime.datetime.now()
     template_name = "reports/organization-list.html"
     items = {"data":serialized_data, "date":date, "total":total, 'title':f"Organizations List", "print_by":user, "shop_name":""}
     pdf_base64 = render_to_pdf(template_name, items)
     channel_layer = get_channel_layer()
     async_to_sync(channel_layer.group_send)(
          f'reports_for_{user.id}',
          {
               'type':'send_report',
               'report':{
                    'filename':'order_report.pdf',
                    'file':pdf_base64
               }
          }
     )
@shared_task
def shop_generate_report(user_id,search):
     user = CustomUser.objects.get(id=user_id)
     shops = Shop.objects.filter(organization=user.organization)
     
     if search is not None and search!="":
          shops = shops.filter(name__icontains=search)
     serialized_data = ShopSerializer(shops,many=True).data
     total = shops.count()
     date = datetime.datetime.now()
     template_name = "reports/shop-list.html"
     items = {"data":serialized_data, "date":date , "total":total, 'title':f"Shop List", "print_by":user, "shop_name":user.organization.name}
     pdf_base64 = render_to_pdf(template_name, items)
     channel_layer = get_channel_layer()
     async_to_sync(channel_layer.group_send)(
       f'reports_for_{user.id}',
       {
            'type':'send_report',
            'report':{
                 'filename':'order_report.pdf',
                 'file': pdf_base64
            }
       }
     )

@shared_task
def menu_generate_report(user_id, menu_category):
     user = CustomUser.objects.get(id= user_id)
     menus = Menu.objects.filter(shop=user.shop)
     
     if menu_category is not None and menu_category !="":
          menus = menus.filter(menu_category=menu_category)

     serialized_data = MenuSerializer(menus,many=True).data
     total = menus.count()
     date = datetime.datetime.now()
     template_name = "reports/menu-list.html"
     items = {"data":serialized_data, "date":date, 'total':total, "title":f"Menus List  ", "print_by ":user, "shop_name":user.shop.name}
     pdf_base64 = render_to_pdf(template_name, items)
     channel_layer = get_channel_layer()
     async_to_sync(channel_layer.group_send)(
          f'reports_for_{user.id}',
          {
               'type':'send_report',
               'report':{
                    'filename':'order_report.pdf',
                    'file': pdf_base64
               }
          }
     )
@shared_task
def order_generate_report(user_id,order_date,status):
    user = CustomUser.objects.get(id=user_id)
   
    request = None
    orders = Order.objects.filter(shop=user.shop)
    if status is not None and status !="":
        orders = orders.filter(status = status)
    if order_date is not None and order_date !="":
         orders = orders.filter(create_date__date=order_date)
    serialized_data = OrderSerializer(orders, many=True).data
    total = Order.objects.filter(shop=user.shop).count()
    date = datetime.datetime.now()
    template_name = "reports/order-list.html"
    items = {"data": serialized_data,"date" : date , "total":total, "title": f"Order Report ", "print_by": user, "shop_name": user.shop.name}
    pdf_base64 = render_to_pdf(template_name,  items)
    channel_layer = get_channel_layer()
    print('chanel channel layer', channel_layer)
    async_to_sync(channel_layer.group_send)(
        f'reports_for_{user.id}',
        {
            'type': 'send_report',
            'report': {
                'filename': 'order_report.pdf',
                'file': pdf_base64,
            }
        }
    )

@shared_task
def order_detail_generate_report(user_id,order_id):
     user = CustomUser.objects.get(id=user_id)
     order = Order.objects.get(id=order_id)
     serialized_data = KitchenDisplaySerializer(order)
     date = datetime.datetime.now()
     template_name = "reports/order-detail.html"
     items = {"data":serialized_data.data, "date":date,"title": f"Order Detail Report ", "print_by": user, "shop_name": user.shop.name}
     pdf_base64 = render_to_pdf(template_name,items)
     channel_layer = get_channel_layer()
     print('channel layer', channel_layer)
     async_to_sync(channel_layer.group_send)(
          f'reports_for_{user.id}',
          {
               'type':'send_report',
               'report':{
                    'filename':"order_detail_report.pdf",
                    'file':pdf_base64
               }
          }
     )