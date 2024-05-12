"""
URL configuration for polatProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from polatFashionApp import views
from rest_framework import routers
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'product', views.ProductView)
# router.register(r'productSize', views.ProductSizeTopView)
# router.register(r'login', views.LoginViewSet, basename='login')
# router.register(r'users',views.UserGetView.as_view({"get":"get"}),basename="user")
router.register(r'category',views.CategoryView,basename="category")
router.register(r'banner',views.BannerView,basename="TopBanner")
router.register(r'bottom_banner',views.BottomBannerView,basename="bottomBanner")
router.register(r'special-product',views.SpacialProduct,basename="SpacialProduct")
router.register(r'sosyal-medial',views.SocialMedialView,basename="sosyal-medial-gallery")
router.register(r'color-product',views.ColorView,basename="color")
router.register(r"social_info_link",views.FooterSocialMediaInfoLink,basename="mediaInfoLink")
router.register(r"relevant",views.FooterRelevantInfo,basename="relavant")
router.register(r"cargo-price",views.CargoPriceView,basename="kargo fiyatı")
router.register(r"contract-terms/",views.ContractTermsView,basename="contract-terms")
# router.register(r'order',views.UserOrderHistory,basename="order")
# router.register(r'promotion',views.PromotionView,basename="promotion")
# router.register(r'cart',views.UserCartView,basename="cart")

# router.register(r'groups', views.GroupViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('polatFashionApp.urls')),
    path('api/', include(router.urls)),
    # path('api/accounts/', include('authemail.urls')),
    path('api/accounts/signup/', views.AccountCreateView.as_view({"post":"register"}),name="register"),
    path('api/accounts/register-verify/', views.AccountCreateView.as_view({"post":"register_verify"}),name="register_verify"),
    path('api/accounts/send_verification_code/', views.AccountCreateView.as_view({"post":"send_verification_code"}),name="send_verification_code"),
    path('api/accounts/login/', views.AccountCreateView.as_view({"post":"login"}),name="login"),
    path('api/accounts/password_reset/', views.AccountCreateView.as_view({"post":"reset_password"}),name="password_reset"),
    path('api/accounts/password_reset_verify/', views.AccountCreateView.as_view({"post":"reset_password_verify"}),name="reset_password_verify"),
    path('api/accounts/delete_verify/',views.AccountCreateView.as_view({"post","delete_verification_code"}),name="delete_code"),
    path('api/accounts/password_update/',views.UserUpdate.as_view({"post":"password_user_update"}),name="password_user_update"),
    path('api/accounts/logout/',views.AcountLogoutView.as_view({"post":"logout"}),name="user_logout"),
    path('api/users/<int:pk>/', views.UserGetView.as_view({"get":"get"}), name='user'),
    path('api/send_message/',views.MessageView.as_view({"post":"post"}),name="send_message"),
    path('api/send_message/to_admin/',views.SendMessageAdmin.as_view({"post":"user_message_to_admin"}),name="user_message_to_admin"),
    path('api/get_message/<int:user>/',views.MessageView.as_view({"get":"get"}),name="get_message"),
    path('api/accounts/user_update/',views.UserUpdate.as_view({"put":"update"}),name="update"),
    path('api/cart/delete/<int:pk>/', views.UserCartView.as_view({'delete': 'cart_item_delete'}), name='custom_cart_delete'),
    path('api/cart/lenght/<int:pk>/', views.UserCartView.as_view({'get': 'cart_lenght'}), name='cart_lenght'),
    path('api/promotion/<int:pk>/', views.PromotionView.as_view({'get':"get"}), name='promotion'),
    path('api/promotion/state/', views.PromotionView.as_view({'put':"promotion_state"}), name='promotion'),
    # path('api/promotion/<int:pk>/', views.PromotionView.as_view({'delete': 'delete_promotion'}), name='ptomotion_delete'),
    path('api/cart/', views.UserCartView.as_view({'post': 'cart_item_create'}), name='custom_cart'),
    path('api/product-top-size/<int:pk>/', views.ProductSizeTopView.as_view({'get': 'get_product_top_size'}), name='product_Size'),
    path('api/product-lower-size/<int:pk>/', views.ProductSizeLowerView.as_view({'get': 'get_product_lower_size'}), name='product_Lower_Size'),
    path("api/discount/<str:code>/",views.DiscountCode.as_view({"get":"discount_get"}),name="discount"),
    path('api/cart/get/<int:user>/', views.UserCartView.as_view({'get': 'get_cart_all'}), name='get_cart'),
    path('api/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('api/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('api/order/',views.UserOrderHistory.as_view({'post':"create"}),name="user_order_post"),
    path('api/order/update/',views.UserOrderHistory.as_view({'put':"update"}),name="user_order_update"),
    path('api/product/search/<str:q>/<str:value>/',views.ProductSeach.as_view({'get':"get"}),name="productSearch"),
    path('api/product/gender/<str:g>/',views.GenderedProducts.as_view({"get":"getGenderProduct"}),name="getGenderProduct"),

    
    # path('register/', views.RegisterView.as_view(), name='register'),
    # path('login/', views.LoginView.as_view(), name='login'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)