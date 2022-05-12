from django.contrib import admin
from .models import *

# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = ImageGallery
    extra = 5



class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','category','price']
    list_filter = ['time']
    #readonly_fields = ['slug']
    inlines = [ProductImageInline]



admin.site.register(Item,ProductAdmin)
admin.site.register(OrderItem)
admin.site.register(Order)

admin.site.register(WishlistItem)
admin.site.register(Wishlisted)

admin.site.register(ImageGallery)

admin.site.register(BillingAddress)

admin.site.register(Author)

@admin.register(Reviews)
class Reviewadmin(admin.ModelAdmin):
    list_display = ['id','user','product','rate','time']
    readonly_fields = ['time']


@admin.register(BlogPost)
class Reviewadmin(admin.ModelAdmin):
    list_display = ['id','author','title','time']
    readonly_fields = ['time']
