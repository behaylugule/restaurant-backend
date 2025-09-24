# Step 8: urls.py (api/urls.py)
from django.urls import include, path



from api import views


urlpatterns = [

    path('dashboard/count/',views.GlobalCountListView.as_view(), name='book-detail'),
    path('upload/',views.FileUploadCreateView.as_view(),name='file'),
    # organization and Shop
    path('organizations/', views.OrganizationListCreateView.as_view(),name='organization-list-create'),
    path('organizations/<int:pk>/', views.OrganizationDetailView.as_view(),name='organization-detail'),
    path('shops/',views.ShopListCreateView.as_view(),name='shop-list-create'),
    path('shops/<int:pk>/', views.ShopDetailView.as_view(),name='shop-detail'),
    path('dining-tables/', views.DinningTableCreateListView.as_view(),name="shop_dinning_table_list"),
    path('dining-tables/<int:pk>/', views.DinningTableRetrieveDetailView.as_view(),name="shop name"),
    path('client/shops/',views.ShopListRetrive.as_view(),name='client_shop'),
]
