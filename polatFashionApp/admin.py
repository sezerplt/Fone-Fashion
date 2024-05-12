from django.contrib import admin
from .models import (
    Product,ProductTopSize,Category,
    Color,Payment,Cargo,OrderData,
    InventoryState,UserStatistics,Orders,Promotion,UserCart,ProductLowerSize,
    Discount,TopBanner,SocialMedialGallery,User,CustomUser,Message,CargoPrice,ContractTerms,BottomBanner
    )
from django.contrib.auth import get_user_model


admin.AdminSite.site_header="F'One FASHION"

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    pass
    # list_display = ('email', 'username', 'is_staff', 'is_verifield')  # Admin panelinde görünen sütunlar
    # search_fields = ('email', 'username')  # Arama yapılabilen alanlar
    # ordering = ('email',)  # Sıralama için kullanılan alan

@admin.register(Product)
class Product(admin.ModelAdmin):
    pass
@admin.register(ProductTopSize)
class ProductTopSize(admin.ModelAdmin):
    pass
@admin.register(ProductLowerSize)
class ProductTopSize(admin.ModelAdmin):
    pass
@admin.register(Category)
class Category(admin.ModelAdmin):
    pass

@admin.register(Color)
class Color(admin.ModelAdmin):
    pass

@admin.register(Payment)
class Payment(admin.ModelAdmin):
    pass

@admin.register(Cargo)
class Cargo(admin.ModelAdmin):
    pass

@admin.register(OrderData)
class OrderData(admin.ModelAdmin):
    pass

@admin.register(InventoryState)
class InventoryState(admin.ModelAdmin):
    pass

@admin.register(UserStatistics)
class UserStatistics(admin.ModelAdmin):
    pass

@admin.register(Orders)
class Orders(admin.ModelAdmin):
    pass
@admin.register(Promotion)
class Promotion(admin.ModelAdmin):
    pass
@admin.register(UserCart)
class UserCartAdmin(admin.ModelAdmin):
    pass

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass

@admin.register(TopBanner)
class TopBannerAdmin(admin.ModelAdmin):
    pass
@admin.register(SocialMedialGallery)
class SocialMedialGalleryAdmin(admin.ModelAdmin):
    pass 

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass
@admin.register(CargoPrice)
class CargoPriceAdmin(admin.ModelAdmin):
    pass

@admin.register(ContractTerms)
class ContractTermsAdmin(admin.ModelAdmin):
    pass
@admin.register(BottomBanner)
class BottomBannerAdmin(admin.ModelAdmin):
    pass