from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# CustomUser modelini admin paneline eklemek için, UserAdmin'den türetilmiş bir sınıf oluşturun
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_farmer','adress','password','profile_image')

# admin.site.register() kullanarak CustomUser modelini kaydedin
admin.site.register(CustomUser, CustomUserAdmin)
  
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'farmer','image','quantity')
    class Meta:
        ordering = ['name', '-created_at']

admin.site.register(Product, ProductAdmin)

admin.site.register(Comment)

admin.site.register(Iletisim)

admin.site.register(ReservedProduct)