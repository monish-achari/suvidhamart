"""grofer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from products.views import *

handler404 = handler404
handler500 = handler500


urlpatterns = [
    path('test/',test_url),
    path('admin/logout/',logout_page),

    path('admin/', admin.site.urls),
    path('',login_page,name='login'),
    
    path('dashboard/',dashboard_page, name='dashboard'),
    path('user/add',create_user_page, name='adduser'),
    path('user/details/<uid>/',user_details,name='detial_user'),
    
    path('category/create/',add_category,name='categoryadd'),
    path('category/list/',list_category,name='categorylist'),
    
    path('sub-category/create/',add_subcategory,name='subcategoryadd'),
    path('sub-category/list/',list_subcategory,name='subcategorylist'),
    
    path('prodcut/list/',list_product,name='productlist'),
    path('prodcut/add/',add_product,name='productadd'),

    path('offers/list/',list_offers,name='offerslist'),
    path('offer/add/',add_offer,name='offeradd'),

    path('offers3/list/',list_offers_third,name='offerslist3'),
    path('offer3/add/',add_offer_third,name='offeradd3'),

    path('offers4/list/',list_offers_fourth,name='offerslist4'),
    path('offer4/add/',add_offer_fourth,name='offeradd4'),

    path('offers5/list/',list_offers_fifth,name='offerslist5'),
    path('offer5/add/',add_offer_fifth,name='offeradd5'),

    path('offers2/list/',list_offers_second,name='offerslist2'),
    path('offer2/add/',add_offer_second,name='offeradd2'),

    path('delete/<uid>/<key>/<url>/',delete_obj, name='delete'),
    path('<obj>/edit/<uid>/',update_obj_page,name='edit'),


    path('order/<deli_type>/',ordered_history,name='orders_history'),
    path('delivered/<child_key>/<parent_key>/',order_delivered,name='order_confirm'),
    path('cancel/<child_key>/<parent_key>/',order_cancel,name='order_confirm'),

    # path('order/details/<prod_id>/<user_uuid>/',odered_products,name='order_detials'),
    path('order/details/<order_id>/<sub_id>/',odered_products,name='order_detials'),
    path('order/update/<key>/<key_n>/<values>/',update_order,name='order_update'),

    path('active/location/',location_list, name='locations_list'),
    path('location/add/',location_add, name='locations_add'),

    path('cart/list/',list_carts, name='cartlist'),
    path('cart/details/<userid>/<cartid>/',detais_cart, name='cartlist'),


    path('grand-category/list/',list_grand_subcategory, name='grandcategory'),
    path('grand-category/add/',add_grand_subcategory, name='grandcategoryadd'),

    #mail api
    path('send/order-mail/',ordermailapicall),

]
