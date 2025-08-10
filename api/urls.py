# Step 8: urls.py (api/urls.py)
from django.urls import include, path


from .views import  RegisterView,ChangePasswordView, RetrieveUser,UpdateUser
from api import views


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', views.me_view, name='me'),
    path('update-profile/<int:pk>/',UpdateUser.as_view(),name='update-profile'),
    path('change-password/',ChangePasswordView.as_view(),name='change_password'),
    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('users/',RetrieveUser.as_view(),name='get_user'),
    path('dashboard/count/',views.GlobalCountListView.as_view(), name='book-detail'),
    path('upload/',views.FileUploadCreateView.as_view(),name='file'),
    # organization and Shop
    path('organizations/', views.OrganizationListCreateView.as_view(),name='organization-list-create'),
    path('organizations/<int:pk>/', views.OrganizationDetailView.as_view(),name='organization-detail'),
    path('shops/',views.ShopListCreateView.as_view(),name='shop-list-create'),
    path('shops/<int:pk>/', views.ShopDetailView.as_view(),name='shop-detail'),
    path('dining-tables/', views.DinningTableCreateListView.as_view(),name="shop_dinning_table_list"),
    path('dining-tables/<int:pk>/', views.DinningTableRetrieveDetailView.as_view(),name="shop name"),
    path('categories/', views.MenuCategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.MenuCategoryDetailView.as_view(),name='category-detail'),
    
    path('menu/', views.MenuListCreateView.as_view(),name='menu-list'),
    path('menu/<int:pk>/',views.MenuDetailView.as_view(),name='menu-detail'),   

    path('client/shops/',views.ShopListRetrive.as_view(),name='client_shop'),
    path('client/categories/<int:pk>/', views.MenuCategoryListRetrive.as_view(),name='client_shop_menu'),
    path('client/menus/<int:pk>/',views.MenuListRetrive.as_view(),name='client_shop_menu'),
   
    path('messages/', views.MessageListView.as_view(),name='message_list'),
    path('chat-rooms/',views.ChatRoomCreateListView.as_view(),name='message_list'),
    
    
]
