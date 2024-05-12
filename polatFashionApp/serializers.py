from django.contrib.auth.models import User, Group
from .models import (
    Product,ProductTopSize,Color,
    Category,Orders,Promotion,UserCart,
    ProductLowerSize,Discount,TopBanner,
    SocialMedialGallery,CustomUser,Message,SocialMediaLink,RelavantInfo,
    CargoPrice,ContractTerms,BottomBanner
    
    )
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"
class ProuductSizeTopSerializer(serializers.ModelSerializer):
     class Meta:
        model=ProductTopSize
        fields="__all__"
class ProductSizeLowerSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductLowerSize
        fields="__all__"
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])  # Şifre PBKDF2_SHA256 ile şifrelenir
        user.save()
        return user

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id',"first_name","last_name",'username', 'email']
class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Orders
        fields="__all__"

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Promotion
        fields="__all__"

class UserCartSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserCart
        fields="__all__"
class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Discount
        fields="__all__"
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"
class TopBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model=TopBanner
        fields="__all__"
class BottomBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model=BottomBanner
        fields="__all__"
class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model=SocialMedialGallery
        fields="__all__"
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Color
        fields="__all__"
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields="__all__"
        # extra_kwargs = {'password': {'write_only': True}}
class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=["id","first_name","last_name","email","date_joined","tel"]
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Message
        fields="__all__"

class SocialMediaInfıLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model=SocialMediaLink
        fields="__all__"
class RelevantInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=RelavantInfo
        fields="__all__"
class CargoPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model=CargoPrice
        fields="__all__"
#["id","firstname","lastname","email","date_joined"]
        
class ContactTermsSerializer(serializers.ModelSerializer):
    class Meta:
        model=ContractTerms
        fields="__all__"
