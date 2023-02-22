from django.urls import path
from .views import *

urlpatterns=[
    path('home/', homepg),
    path('index/', index),
    path('shop_register/', shopereg),
    path('shop_login/', shoplogin),
    path('shop_profile/', shopprofile),
    path('pdt_upload/', uploadpdt),
    path('pdt_display/',pdtdisplay),
    path('pdt_delete/<int:id>', pdtdelete),     # we are passing the ID of item throug URL which is to be deleted
    path('pdt_edit/<int:id>', pdtedit),
    path('view_all_pdts/',view_all_shoppdts),
    path('customer_register/', custreg),
    path('customer_login/', user_login),
    path('user_profile/', user_profile),
    path('verify/<auth_token>', verify),   #<auth_token> it's a string, so no need to mention data type. just provide a variable to get that token
    path('user_view_pdt/', user_view_pdt),
    path('add_to_cart/<int:id>',addtocart),
    path('add_to_wishlist/<int:id>', addtowishlist),
    path('wishlist_display/', wishlistdisplay),
    path('cart_display/', cartdisplay),
    path('pdt_removefrom_cart/<int:id>', cartpdtremove),
    path('pdt_removefrom_wishlist/<int:id>', wishlistpdtremove),
    path('cart_pdt_buy/<int:id>', cartpdtbuy),
    path('card_payment/', cardpayment),
    path('shop_notification/',shopnotification)
]