from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(shopregmodel)
admin.site.register(pdtupldmodel)
admin.site.register(profile)
admin.site.register(cartmodel)
admin.site.register(wishlistmodel)
admin.site.register(buymodel)
admin.site.register(cardpaydetailsmodel)
admin.site.register(shopnotificationmodel)
admin.site.register(usernotificationmodel)

