
#Django
from django.shortcuts import render,HttpResponse
from django.contrib.auth.models import  Group,User
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import PasswordResetView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordResetConfirmView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.views import LoginView
from django.db import IntegrityError

from django.views.decorators.csrf import csrf_exempt
from .forms import EmailAuthenticationForm

#rest_framework
from rest_framework.decorators import action
from rest_framework import routers
from rest_framework import viewsets,generics,status
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


from .models import (
    Product,ProductTopSize,Orders,
    Promotion,ProductLowerSize,Discount,
    Category,TopBanner,SocialMedialGallery,
    Color,CustomUser,Message,SocialMediaLink,
    RelavantInfo,CargoPrice,ContractTerms,BottomBanner
    
    )
from .serializers import (
    ProductSerializer,ProuductSizeTopSerializer,OrderHistorySerializer,
    ProductTopSize,PromotionSerializer,UserCartSerializer,UserCart,
    ProductSizeLowerSerializer,DiscountCodeSerializer,CategorySerializer,
    TopBannerSerializer,SocialMediaSerializer,ColorSerializer,UserSerializer,
    UserGetSerializer,MessageSerializer,SocialMediaInfıLinkSerializer,
    RelevantInfoSerializer,CargoPriceSerializer,ContactTermsSerializer,BottomBannerSerializer
    )

import os 
import datetime


env_mail=os.environ.get("EMAIL_HOST_USER")
info_send_mail=os.environ.get("INFO_EMAIL_HOST_USER")# iade değişim gönderimleri

def html_message(message,verification_code=None):
    if verification_code:

        return f"""
            <h1>F'one Fashion</h1>
            <br/>
            <h2>{message}<strong style='border: 1px solid #000000;padding:2px'>
            {verification_code}</strong>
            
            </h2> """
    
    return f"""
            <h1>F'one Fashion</h1>
            <br/>
            <h2>{message}</h2> """



def index(request):
    return render(request, 'base.html')
@csrf_exempt
class EmailLoginView(LoginView):
    form_class = EmailAuthenticationForm

@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'success': True})
#Ürün
class ProductView(viewsets.ModelViewSet):
    serializer_class=ProductSerializer
    queryset = Product.objects.all().order_by()
#anasayfa ürün
class SpacialProduct(viewsets.ModelViewSet):
    serializer_class=ProductSerializer
    queryset = Product.objects.filter(special=True)
#cinsiyete göre ürünler
class GenderedProducts(viewsets.ModelViewSet):
    serializer_class=ProductSerializer
    queryset = Product.objects.all().order_by()
   
    
    @action(detail=False,method=["GET"])
    def getGenderProduct(self,request,g):
        product=Product.objects.filter(gender=g)
        serializer=ProductSerializer(product,many=True)

        return Response({"results":serializer.data},status=status.HTTP_200_OK)

#PAGENATİON GEREK DUYULURSA BU CLASS KULLANILACAK
#############################################################################################
# class SetPagination(PageNumberPagination):
#     page_size = 20
#     page_size_query_param = 'page_size'
#     max_page_size = 1000
    

# class GenderedProducts(viewsets.ModelViewSet):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all().order_by('id')  # Sıralama kriteri eklenmeli
#     pagination_class = PageNumberPagination  # Pagination sınıfı belirtilmeli

#     @action(detail=False, methods=["GET"])
#     def getGenderProduct(self, request,g):
#      # Gender parametresi alınmalı
#         if g is not None:
#             products = Product.objects.filter(gender=g)
#             page = self.paginate_queryset(products)  # Sayfalama yapılmalı
#             if page is not None:
#                 serializer = ProductSerializer(page, many=True)
#                 return self.get_paginated_response(serializer.data)
#             serializer = ProductSerializer(products, many=True)
#             return Response({"results": serializer.data}, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Gender parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
class ProductSeach(viewsets.ModelViewSet):
    @action(detail=False,methods=["GET"])
    
    def get(self,request,q,value):
    
        if value=="kategori":
            productResults=Product.objects.filter(category=q)
            serializer=ProductSerializer(productResults,many=True)
            return Response({"results":serializer.data},status=status.HTTP_200_OK)
        else:
            productFilter=Product.objects.filter(head=q)
            serializer=ProductSerializer(productFilter,many=True)
            return Response({"results":serializer.data},status=status.HTTP_200_OK)

    
#categrory verileri almak
class CategoryView(viewsets.ModelViewSet):
    serializer_class=CategorySerializer
    queryset=Category.objects.all().order_by()
    # @action(detail=False,method=["GET"])
    # def get(self,request):
    #     pass

#ÜrünlERİN beden boyutları
class ProductSizeTopView(viewsets.ModelViewSet):
    serializer_class = ProuductSizeTopSerializer
    queryset = ProductTopSize.objects.all().order_by()

    @action(detail=False, method=["GET"])
    def get_product_top_size(self, request, pk=None):
        if pk ==0:
         
            return Response(None)
        product_size = ProductTopSize.objects.get(pk=pk)
      
        serializer = ProuductSizeTopSerializer(product_size)
     
        return Response(serializer.data)
class ProductSizeLowerView(viewsets.ModelViewSet):
    serializer_class=ProductSizeLowerSerializer
    queryset=ProductLowerSize.objects.all().order_by()
    @action(detail=False,method=["GET"])
    def get_product_lower_size(self,request,pk):
        if pk ==0:
            
            return Response(None)
        product_size=ProductLowerSize.objects.get(pk=pk)
        serializer=ProductSizeLowerSerializer(product_size)
        return Response(serializer.data)
    

#Kullanıcı oluşturmak

class AccountCreateView(viewsets.ModelViewSet):
    serializer_class=UserSerializer
    @action(detail=False,method=["post"])
    def register(self,request):
        email=request.data.get("email")
        password=request.data.get("password")
        try:
    
            user = CustomUser.objects.create(email=email,username=email)
            user.set_password(password)
            subject = 'Oturum Doğrulama'
            html=html_message("Doğrulama kodunuz",user.verification_code)
            send_mail(subject,"",env_mail, [email],html_message=html)
            token,credits=Token.objects.get_or_create(user=user)
            serializer=UserSerializer(user)
            return Response({"user":serializer.data,"token":token.key,"user_id":user.pk},status=status.HTTP_201_CREATED)
            # user.delete_verification_code(schedule=timezone.now()+ datetime.timedelta(seconds=60))
          
        
        except IntegrityError as e:
            return Response("Üzgünüz, girdiğiniz e-posta adresi zaten sistemimizde kayıtlı",status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
           
            return Response(f"Kayıt başarısız {str(e)}",status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False,method=["post"])
    def register_verify(self,request):
        email=request.data.get("email")
        code=request.data.get("code")
      
        try:
            user=CustomUser.objects.get(email=email,verification_code=code, is_verified=False)
        
        except CustomUser.DoesNotExist:
            return Response('Geçersiz doğrulama kodu veya kullanıcı zaten doğrulanmış.', 
                            status=status.HTTP_400_BAD_REQUEST)
        user.is_verified = True
        user.save()

        return Response("Kullanıcı doğrulandı")

    @action(detail=False,method=["post"])
    def login(self,request):
        email=request.data.get("email")
        password=request.data.get("password")
       
        try:
            user=CustomUser.objects.get(email=email, is_verified=True)
            if user.check_password(password):
                token,credits=Token.objects.get_or_create(user=user)
                serializer=UserSerializer(user)
                return Response({"user":serializer.data,"token":token.key,"user_id":user.pk},status=status.HTTP_201_CREATED)
            return Response("Geçersiz kimlik bilgisi. Lütfen kullanıcı adı veya şifresini kontrol ediniz",status=status.HTTP_401_UNAUTHORIZED)
        except :
            return Response("Geçersiz kimlik bilgisi. Lütfen kullanıcı adı veya şifresini kontrol ediniz",status=status.HTTP_401_UNAUTHORIZED)
    @action(detail=False,method=["post"])
    def reset_password(self,request):
        email=request.data.get("email")
        code=request.data.get("code")
        new_passsword=request.data.get("newPassword")
        try:
            user=CustomUser.objects.get(email=email,verification_code=code,is_verified=True)
          
        except Exception as e:
           
            return Response("Geçersiz email veya kullanıcı doğrulanmadı",status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_passsword)
        user.verification_code = None
        user.save()
        return Response("Şifreniz başarıyla değiştirildi")   
    @action(detail=False,methods=["post"])
    def reset_password_verify(self,request):
        email=request.data.get("email")
        try:
            user=CustomUser.objects.get(email=email,is_verified=True)
        except Exception:
            return Response({"message":"Kullanıcı doğrulandı"},status=status.HTTP_400_BAD_REQUEST)
        user.verification_code=user.generate_verification_code()
        user.save()
        subject="Şifre yenileme doğrulama kodu"
        
        message="Şifre yenileme onay kodu "
        html=html_message(message,user.verification_code)
        send_mail(subject,"",email,[email],html_message=html)
        return Response({"message":f"Şifre yenileme '{email}' adresine gönderildi "})
    @action(detail=False,method=["post"])
    def send_verification_code(self,request):
        email=request.data.get("email")
        
        try:
            user=CustomUser.objects.get(email=email)
        except Exception as e:
            return Response("Kullanıcı bulunamadı",status=status.HTTP_400_BAD_REQUEST)
        user.verification_code=user.generate_verification_code()
        user.save()
        subject="Doğrulama kodu"
        
        message="İşlemi tamamlamak için kodu kullanın "
        html=html_message(message,user.verification_code)
        send_mail(subject, "",env_mail, [email],html_message=  html)
        return Response({"message":f"Doğrulama kodu '{email}' adresine gönderildi "})
    @action(detail=False,method=["post"])
    def delete_verification_code(self,request):
        email=request.data.get("email")
        try:
            user=CustomUser.objects.get(email=email,is_verified=False)
        except:
             return Response({"message":"Kullanıcı doğrulanamadı"},status=status.HTTP_400_BAD_REQUEST)
        user.verification_code=None
        user.save()
        return Response({"message":"Doğrulama kodu silindi"},status=status.HTTP_200_OK)
class AcountLogoutView(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    @action(detail=False,methods=["POST"])
    def logout(self,request):
        try:
            logout(request)
            return Response("Başarıyla çıkış yapıldı",status=status.HTTP_200_OK)
        except Exception as e:
            return Response("Çıkış yaparken bir hata oluştu", status=status.HTTP_400_BAD_REQUEST)


class UserUpdate(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    action(detail=False,method=["put"])
    def update(self,request):
        user_id=request.data.get("user_id")
        first_name=request.data.get("first_name")
        last_name=request.data.get("last_name")
        tel=request.data.get("tel")
        try:
            user=CustomUser.objects.get(pk=user_id)
        except Exception as e:
            return Response(f"Hata:{e}",status=status.HTTP_400_BAD_REQUEST)
        user.first_name=first_name
        user.last_name=last_name
        user.tel=tel
        user.save()
        return Response("Bilgileriniz başarıyla güncellendi",status=status.HTTP_200_OK)
      
    @action(detail=False,method=["post"])
    def password_user_update(self,request):
        
        email=request.data.get("email")
        password=request.data.get("password")
      
        try:
            user=CustomUser.objects.get(email=email)
            if user.check_password(password):
                subject="Şifre yenileme doğrulama kodu"
        
                message="Şifre yenileme onay kodu "
                user.verification_code=user.generate_verification_code()
                html=html_message(message,user.verification_code)
                send_mail(subject,"",email,[email],html_message=html)
                # user.set_password(newPassword)
                return Response("Şifre değiştirme başarılı",status=status.HTTP_201_CREATED)
            else:
                return Response("Şİfreniz hatalı",status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f"Bir hata ile karşılaşıldı. {e}",status=status.HTTP_404_NOT_FOUND)
        
class UserGetView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # queryset = CustomUser.objects.all()  # Use your custom User model
    # serializer_class =UserGetSerializer
    @action(detail=False,method=["get"])
    def get(self,request,pk):
        users=CustomUser.objects.get(pk=pk)
      
        serializers=UserGetSerializer(users)
        return Response(serializers.data,status=status.HTTP_200_OK)
class MessageView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Message.objects.all()  # Use your custom User model
    serializer_class =MessageSerializer
    def get(self,request,user):
      
        users=CustomUser.objects.get(pk=user)
       
        try:
            message_data=Message.objects.filter(user=users)  # Use filter instead of get
            serializer=MessageSerializer(message_data, many=True)  # Note the many=True parameter
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Hata: {e}",status=status.HTTP_400_BAD_REQUEST)
    def post(self,request):
        user=request.data.get("user_id")
        title=request.data.get("title")
        message=request.data.get("message")

        userId=CustomUser.objects.get(pk=user)
        send_mail(f"{info_send_mail.capitalize()} {title} başlıklı kullanıcıdan, yeni bir mesajınız var",message=message,from_email=userId.email,recipient_list=[info_send_mail])
        add_message=Message.objects.create(user=userId,title=title,send_message=message)
        
        add_message.save()
        return Response("Mesajınız gönderildi",status=status.HTTP_200_OK)
class SendMessageAdmin(viewsets.ModelViewSet):
    def user_message_to_admin(self,request):
        email=request.data.get("email")
        title=request.data.get("title")
        message=request.data.get("message")
        try:
            send_mail(f"{email} {title} başlıklı kullanıcıdan, yeni bir mesajınız var",message=message,from_email=env_mail,recipient_list=[info_send_mail])
        except:
            return Response("Mesajınız gönderirken bir hata oluştu",status=status.HTTP_400_BAD_REQUEST)
        return Response("Mesajınız gönderildi",status=status.HTTP_200_OK)
#Giriş yapmak
class LoginViewSet(viewsets.ViewSet):
    def create(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
       
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'user_id':user.pk,'user': user.username, 'token':token.key})
        else:
            return Response('Geçersiz giriş bilgileri', status=status.HTTP_400_BAD_REQUEST)


#Kullanıcı şifre resetleme
# class CustomPasswordResetView(generics.CreateAPIView):
#     serializer_class=PasswordResetSerializer
#     def create(self,request):
#         email=request.data.get("email")
      
#         user=User.objects.filter(email=email).first()
#         if user is not None:
#             # PasswordResetView.as_view()(request)
#             uidb64 = urlsafe_base64_encode(force_bytes(user.id))
#             token = default_token_generator.make_token(user)
#             reset_link = f"http://127.0.0.1:8000/api/reset/{uidb64}/{token}/"

#             send_mail(
#                 "Şifre Sıfırlama Mesajı",
#                 f"Şifreyi sıfırlamak için linke tıklayın: {reset_link}",
#                 env_mail,
#                 [email]
#             )
#             return Response({'message': 'Şifre sıfırlama e-postası gönderildi.'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'message': 'Bu e-posta adresine sahip bir kullanıcı bulunamadı.'}, status=status.HTTP_404_NOT_FOUND)
# #Kullanıcı verileri almak        
# class UserViewSets(viewsets.ViewSet):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def create(self, request):
#         # The authenticated user can be accessed using request.user
       
#         user=request.data.get("username")
     
#         queryset = User.objects.filter(pk=user)
#         serializer = UserViewSerializer(queryset, many=True)
#         return Response(serializer.data)

    
#Kullanıcı şiparişleri almak
class UserOrderHistory(viewsets.ModelViewSet):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @action(detail=False,method=["post"])
    def create(self,request):
        user=request.data.get("username")
        userId = CustomUser.objects.get(pk=user)

        order_set=Orders.objects.filter(user=userId).all()
        
        serializerOrder=OrderHistorySerializer(order_set,many=True)
    
        
        return Response(serializerOrder.data,status=status.HTTP_200_OK)
    @action(detail=False,method=["put"])
    def update(self,request):
        user=request.data.get("username")
        orderId=request.data.get("orderId")
        change=request.data.get("change")
        statement=request.data.get("statement")
        userId=CustomUser.objects.get(pk=user)
        order=Orders.objects.filter(pk=orderId,user=userId)
      
        if order:
             order.update(change=change,statement=statement)
             html=html_message(statement)
             send_mail(
                f"{change}",
                "",
                env_mail,
                [info_send_mail],
                html_message=html
                
            )
             return Response("Talebiniz iletildi",status=status.HTTP_200_OK)
        else:
            return Response("Talebiniz iletilmedi",status=status.HTTP_400_BAD_REQUEST)
#promosyon ve indirimler
class PromotionView(viewsets.ModelViewSet):
 
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = UserCart.objects.all()
    serializer_class = UserCartSerializer

    @action(detail=False, methods=['get'])
    def get(self, request,pk):
        userId = CustomUser.objects.get(pk=pk)
        try:
            
            promostion_get = Promotion.objects.filter(user=userId)
            
        except:
             return Response("Adınıza ait bir kupun bulunamadı",status=status.HTTP_400_BAD_REQUEST)
        serializer = PromotionSerializer(promostion_get, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def delete_promotion(self, request, pk=None):
        try:
            promotion_instance = Promotion.objects.get(pk=pk)
            
        except Promotion.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        promotion_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    @action(detail=True,method=["put"])
    def promotion_state(self,request):
        user_id=request.data.get("user_id")
        promotion_id=request.data.get("id")
        state=request.data.get("state")
    
        try:
            user = CustomUser.objects.get(pk=user_id)
            # Filter promotions based on user and promotion id
            promotion = Promotion.objects.get(user=user, id=promotion_id)
        except CustomUser.DoesNotExist:
            return Response("User not found", status=status.HTTP_400_BAD_REQUEST)
        except Promotion.DoesNotExist:
            return Response("Promotion not found", status=status.HTTP_400_BAD_REQUEST)
        
        promotion.state=state
        promotion.save()
        return Response("Kupon kullanıldı",status=status.HTTP_200_OK)
#kullanıcı sepeti
class UserCartView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = UserCart.objects.all()
    serializer_class = UserCartSerializer
    @action(detail=True,methods=["post"])
    def cart_item_create(self, request):
        user = request.data.get("user")
        product = request.data.get("products")
        count = request.data.get("count")
        price = request.data.get("price")
        size=request.data.get("size")
        userId = CustomUser.objects.get(pk=user)
      
        productId = Product.objects.get(id=product)
        existing_cart_item = UserCart.objects.filter(user=user, products=product,size=size).first()

        if existing_cart_item:
            
            existing_cart_item.count = count
   
            existing_cart_item.price = price
         
            existing_cart_item.save()
          
            serializer = UserCartSerializer(existing_cart_item)
        
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
  
            # If the product is not in the cart, create a new cart item
            new_cart_item = UserCart.objects.create(
                user=userId,
                products=productId,
                count=count,
                price=price,
                size=size
            )

            # Return a response indicating that the cart item has been created
            serializer = UserCartSerializer(new_cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
    @action(detail=True,methods=["delete"])
    def cart_item_delete(self,request,pk=None):
        user=request.data.get("username")
       
        userId=CustomUser.objects.get(pk=user)
    
        cart_item= UserCart.objects.filter(user=userId, pk=pk).first()

        cart_item.delete()
        
        # cart_item.delete()
        del_serializer=UserCartSerializer(cart_item)
        return Response(del_serializer.data)
    @action(detail=True, methods=["get"])
    def get_cart_all(self, request, user):
        # Get the user
        
        userId = CustomUser.objects.get(pk=user)
        
        # Get the cart data for the user
        cartData = UserCart.objects.filter(user=userId)
     
        # Create a list to store serialized data
        productData = []
        if cartData:
        # Loop through each item in the cart
            for cart_item in cartData:
                # Get the product associated with the cart item
                product = Product.objects.get(id=cart_item.products.pk)

                # Serialize cart item and product separately
                serializerCart = UserCartSerializer(cart_item)
                serializerProduct = ProductSerializer(product)
                data={**serializerProduct.data,**serializerCart.data,}
                # Append the serialized data to the list
                productData.append(data)
             
            # Return the serialized data as JSON response
            return Response(productData)
        else:
            return Response(status=status.HTTP_201_CREATED)
    @action(detail=False,method=["get"])
    def cart_lenght(self,request,pk):
        
        userId = CustomUser.objects.get(pk=pk)
        cartData = UserCart.objects.filter(user=userId)
        total_items = cartData.count()
        return Response({"cart_lenght":total_items})

#indirim kodu 
class DiscountCode(viewsets.ModelViewSet):
  
    serializer_class=DiscountCodeSerializer
    queryset=Discount.objects.all().order_by()
    @action(detail=True,method=["get"])

    def discount_get(self,request,code):
        try:
            discodeCode = Discount.objects.get(discount_code=code)
        
        except Discount.DoesNotExist:
            return Response("Kod tanımlı değil", status=status.HTTP_404_NOT_FOUND)

        if discodeCode.discount_date >= timezone.now().date():
            serializers = DiscountCodeSerializer(discodeCode)
            return Response(serializers.data,status=status.HTTP_200_OK)
        else:
            return Response("İndirim kodunun geçerlilik süresi dolmuştur", status=status.HTTP_400_BAD_REQUEST)
       
class BannerView(viewsets.ModelViewSet):
    serializer_class=TopBannerSerializer
    queryset=TopBanner.objects.all().order_by()
class BottomBannerView(viewsets.ModelViewSet):
    serializer_class=BottomBannerSerializer
    queryset=BottomBanner.objects.all()
class SocialMedialView(viewsets.ModelViewSet):
    serializer_class=SocialMediaSerializer
    queryset=SocialMedialGallery.objects.all().order_by()
class ColorView(viewsets.ModelViewSet):
    serializer_class=ColorSerializer
    queryset=Color.objects.all().order_by()

class FooterSocialMediaInfoLink(viewsets.ModelViewSet):
    serializer_class=SocialMediaInfıLinkSerializer
    queryset=SocialMediaLink.objects.all()
class FooterRelevantInfo(viewsets.ModelViewSet):
    serializer_class=RelevantInfoSerializer
    queryset=RelavantInfo

class CargoPriceView(viewsets.ModelViewSet):
    serializer_class=CargoPriceSerializer
    queryset=CargoPrice.objects.all()

class ContractTermsView(viewsets.ModelViewSet):
    serializer_class=ContactTermsSerializer
    queryset=ContractTerms.objects.all()