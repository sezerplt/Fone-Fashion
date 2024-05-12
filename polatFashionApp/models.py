from django.db import models
from django.contrib.auth.models import AbstractUser,User,BaseUserManager
import random
from django.utils.text import slugify
import os
import datetime
from django.utils import timezone
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from colorfield.fields import ColorField
# from background_task import background

#user e-mail adresini benzersiz yaptık
# User._meta.get_field('email')._unique = True
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
#kullanıcı modelini özelleştirm
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    tel=models.CharField(max_length=12, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=10, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def generate_verification_code(self):
          return ''.join(random.choices('0123456789', k=6))


    def save(self, *args, **kwargs):
        if not self.verification_code:
            self.verification_code = self.generate_verification_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
@receiver(post_save, sender=CustomUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
def upload_to(instance, filename):

    print(instance.uploadValue)
    def to_english(text):
        turkish_chars = "çÇğĞıİöÖşŞüÜ"
        english_chars = "cCgGiIoOsSuU"
        translation=str.maketrans(turkish_chars,english_chars)
        return text.translate(translation)
    
    if instance.uploadValue == "product":
        category_folder = instance.category
        head_folder = slugify(instance.head)
        new_filename = f"{slugify(os.path.splitext(filename)[0])}.{instance.get_file_extension(filename)}"
        imgFile=f"media/product_images/{to_english(category_folder)}/{head_folder}/{new_filename}"
   
        return imgFile
    elif instance.uploadValue == "color":
        return f"media/product_images/color_images/{instance.color}-{filename}"
    elif instance.uploadValue=="top_banner":
        return f"media/banner/top_banner/{instance.id}-{filename}"
    elif instance.uploadValue=="social_medial_gallery":
        return f"media/social/gallery/{instance.id}-{filename}"
    elif instance.uploadValue=="bottom_banner":
        return f"media/social/gallery/{instance.id}-{filename}"
# Create your models here.
#Kategori
class Category(models.Model):
    name=models.CharField(verbose_name="Kategori adı",max_length=100,unique=False)
    class  Meta:
        verbose_name="Kategori"
        verbose_name_plural="Kategori"
    def __str__(self) -> str:
        return self.name
#Bedenlerin boyutu ve stok sayısı
class ProductTopSize(models.Model):
    XS=models.PositiveIntegerField(verbose_name="XS",default=0,blank=True)
    S=models.PositiveIntegerField(verbose_name="S",default=0,blank=True)
    M=models.PositiveIntegerField(verbose_name="M",default=0,blank=True)
    L=models.PositiveIntegerField(verbose_name="L",default=0,blank=True)
    XL=models.PositiveIntegerField(verbose_name="XL",default=0,blank=True)
    
    class  Meta:
        verbose_name="Üst Beden Bilgileri"
        verbose_name_plural="Üst Beden Bilgileri"
       
    def __str__(self) -> str:
        return f"XS: {self.XS}-S: {self.S}-M: {self.M}-L: {self.L}-XL: {self.XL}"

class ProductLowerSize(models.Model):
    size24=models.PositiveIntegerField(verbose_name="24",default=0,blank=True)
    size26=models.PositiveIntegerField(verbose_name="26",default=0,blank=True)
    size28=models.PositiveIntegerField(verbose_name="28",default=0,blank=True)
    size30=models.PositiveIntegerField(verbose_name="30",default=0,blank=True)
    size32=models.PositiveIntegerField(verbose_name="32",default=0,blank=True)
    size34=models.PositiveIntegerField(verbose_name="34",default=0,blank=True)
    size36=models.PositiveIntegerField(verbose_name="36",default=0,blank=True)
    size38=models.PositiveIntegerField(verbose_name="38",default=0,blank=True)
    size40=models.PositiveIntegerField(verbose_name="40",default=0,blank=True)
    size42=models.PositiveIntegerField(verbose_name="42",default=0,blank=True)
    class Meta:
       
        verbose_name="Alt Beden Bilgileri"
        verbose_name_plural="Alt Beden Bilgileri"
       
    def __str__(self) -> str:
        sizes = [f"{field.verbose_name}: {getattr(self, field.name)}" for field in self._meta.fields if isinstance(field, models.PositiveIntegerField)]
        return ", ".join(sizes)
#Renkler ve stok sayısı    
class Color(models.Model):
    color=ColorField(default='#FF0000')
    colorStock=models.PositiveIntegerField(verbose_name="Renk stoklerı",unique=False)
    image=models.ImageField(default="",verbose_name="Ana ürün resmi",upload_to=upload_to)
    image1=models.ImageField(default="",verbose_name="Ürün resmi",upload_to=upload_to)
    image2=models.ImageField(default="",verbose_name="Ürün resmi",upload_to=upload_to)
    productTopSize=models.ForeignKey(ProductTopSize,verbose_name="Üst Beden",on_delete=models.CASCADE,blank=True,null=True)
    productLowerSize=models.ForeignKey(ProductLowerSize,verbose_name="Alt Beden",on_delete=models.CASCADE,blank=True,null=True)
    uploadValue="color"
    class  Meta:
        verbose_name="Ürün Renk Bilgileri"
        verbose_name_plural="Ürün Renk Bilgileri"
    
    def __str__(self) -> str:
        return f"{self.color} - {self.colorStock}"
    
#Ürün bilgileri
class Product(models.Model):
    GENDER_CHOICES = [
        ('M', 'man'),
        ('K', 'woman'),
        ('U', 'unisex'),
    ]
  
    head=models.CharField(verbose_name="Ürün başlığı",max_length=500)
    explanation=models.TextField(verbose_name="Ürün açıklması")
    productColor=ColorField(default='#FF0000')
    price=models.DecimalField(verbose_name="Fiyat",max_digits=10, decimal_places=2)
    totalStock=models.PositiveIntegerField(verbose_name="Toplam Stok")
    image=models.ImageField(default="",verbose_name="Ana ürün resmi",upload_to=upload_to)
    image1=models.ImageField(default="",verbose_name="Ürün resmi",upload_to=upload_to)
    image2=models.ImageField(default="",verbose_name="Ürün resmi",upload_to=upload_to)
    category=models.CharField(verbose_name="Category",max_length=300, blank=True, null=True)
    gender=models.CharField(verbose_name="Cinsiyet",choices=GENDER_CHOICES,max_length=300, blank=True, null=True)
    color=models.ManyToManyField(Color,verbose_name="Ürün renkleri",unique=False,blank=True)
    productTopSize=models.ForeignKey(ProductTopSize,verbose_name="Üst Beden",on_delete=models.CASCADE,blank=True,null=True)
    productLowerSize=models.ForeignKey(ProductLowerSize,verbose_name="Alt Beden",on_delete=models.CASCADE,blank=True,null=True)
    pattern_info=models.CharField(verbose_name="Kalıp bilgisi",max_length=300,blank=True,null=True)
    material = models.CharField(verbose_name="Materyal",max_length=300, blank=True, null=True)
    model_size=models.CharField("Manken ölçüsü",max_length=300, blank=True, null=True)
    body_size=models.CharField("Model bedeni",max_length=300, blank=True, null=True)
    special=models.BooleanField(verbose_name="Özel koleksiyon",blank=True, null=True,default=False)

    uploadValue="product"
    class  Meta:
        verbose_name="Ürün Bilgileri"
        verbose_name_plural="Ürün Bilgileri"
    def get_file_extension(self, filename):
        # Dosyanın uzantısını alır
        return os.path.splitext(filename)[1]
    def __str__(self) -> str:
        return self.head


#Sipariş
class Orders(models.Model):
    product=models.ForeignKey(Product, verbose_name="Ürün",on_delete=models.CASCADE,blank=False,default=1)
    #sipariş numarası oluşturmak
    # orderNumber=models.CharField(verbose_name="sipariş numarası",default=random.choices())
    amount=models.PositiveIntegerField(verbose_name="Ürün miktarı")
    user=models.ForeignKey(CustomUser,models.CASCADE,verbose_name="Kullanıcı",default="")
    orderDate=models.DateTimeField(auto_now_add=True,verbose_name="Sipariş tarihi")
    state=models.CharField(verbose_name="Durum",max_length=50)
    price = models.PositiveIntegerField(verbose_name="Sepetteki ürün tutarı", default=1, blank=True,unique=False)
    size=models.CharField(verbose_name="Sipariş Bedeni",max_length=10,blank=True,unique=False)
    change=models.CharField(verbose_name="İade/Değişim",max_length=200,blank=True,unique=False)
    statement=models.TextField(verbose_name="Açıklama",blank=True,unique=False)
    change_state=models.CharField(verbose_name="Değişim Durumu",max_length=500,blank=True,unique=False,default="Değerlendiriliyor")
    class  Meta:
       verbose_name="Sipariş Bilgileri"
       verbose_name_plural="Sipariş Bilgileri"
    def __str__(self) -> str:
        return f"{self.user.username} - {self.product}"
#kullanıcının sepeti    
class UserCart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, verbose_name="Ürün",on_delete=models.CASCADE,blank=False,default=1)
    count = models.PositiveIntegerField(verbose_name="Sipariş sayısı", default=1, blank=True,unique=False)
    price = models.PositiveIntegerField(verbose_name="Sepetteki ürün tutarı", default=1, blank=True,unique=False)
    size=models.CharField(verbose_name="Sipariş Bedeni",max_length=10,blank=True,unique=False)
    class Meta:
        verbose_name = "Kullanıcı Sepeti"
        verbose_name_plural = "Kullanıcı Sepetleri"

    # def __str__(self) -> str:
    #     return f"{self.user.username} - {self.products}"

#Ödeme
class Payment(models.Model):
    order=models.OneToOneField(Orders,on_delete=models.CASCADE,verbose_name="Sipariş")
    payDate=models.DateTimeField(auto_now_add=True,verbose_name="Ödeme tarihi")
    amount=models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Ödeme miktarı")
    class  Meta:
        verbose_name="Ödeme Alanı"
        verbose_name_plural="Ödeme Alanı"
#Kargo bilgisi
class Cargo(models.Model):
    order=models.OneToOneField(Orders,on_delete=models.CASCADE,verbose_name="Sipariş")
    tracking_number=models.CharField(max_length=100,verbose_name="Takip numarası")
    delivery_date=models.DateTimeField(verbose_name="Teslimat numarası")
    class Meta:
        verbose_name="Kargo Bilgileri"
        verbose_name_plural="Kargo Bilgileri"
#promosyon tanımlama
class Promotion(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name="Promasyon")
    promotion=models.PositiveIntegerField(verbose_name="İndirim miktarı")
    explanation=models.CharField(verbose_name="İndirim açıklaması",max_length=500,blank=True,null=True)
    state=models.BooleanField(verbose_name="Durumu",default=False)
    class Meta:
        verbose_name="İndirim ve Promosyon"
        verbose_name_plural="İndirim ve Promosyon"
#indirim kodu
class Discount(models.Model):
    discount_code=models.CharField(verbose_name="İndirim kodu",max_length=300,default="",blank=True)
    discount_price=models.PositiveIntegerField(verbose_name="indirim tutarı",default=0,blank=True)
    discount_date=models.DateField(verbose_name="Bitiş tarihi",default=timezone.now)
    class Meta:
        verbose_name="İndirim Kodu"
        verbose_name_plural="İndirim Kodu"
    def __str__(self) -> str:
        return f"{self.discount_code} {self.discount_date} {self.discount_price}"
#kullanılan indiirm kodları
class UsedDiscount(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name="Kullanıcı")
    code=models.OneToOneField(Discount,verbose_name="Kullanılan indirim Kod",on_delete=models.CASCADE)
    class Meta:
        verbose_name="Kullanılmış İndirim Kodu"
        verbose_name_plural="Kullanılmış İndirim Kodu"
# İstatistikler ve Raporlar
#Satış verileri
class OrderData(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name="Ürün")
    sales_number = models.PositiveIntegerField(verbose_name="Satış Sayısı")
    date = models.DateField(verbose_name="Satış tarihi",default=timezone.now)
    class Meta:
        verbose_name="Satış Bilgileri"
        verbose_name_plural="Satış Bilgileri"
#Envanter durumu
class InventoryState(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE,verbose_name="Ürün")
    now_stock = models.PositiveIntegerField(verbose_name="Mevcut stok")
    class Meta:
       verbose_name="Envanter Durumu"
       verbose_name_plural="Envanter Durumu"
#Kullanıcı istatislikleri
class UserStatistics(models.Model):
    user= models.OneToOneField(CustomUser, on_delete=models.CASCADE,verbose_name="Kullanıcı")
    orderNumber= models.PositiveIntegerField(verbose_name="Sipariş sayısı")
    class Meta:
        verbose_name="Kullanıcı İstatistikleri"
        verbose_name_plural="Kullanıcı İstatistikleri"


class TopBanner(models.Model):
    image=models.ImageField(verbose_name="banner resmi",upload_to=upload_to)
    text=models.CharField(max_length=400,verbose_name="Banner yazısı",blank=True,null=True)
    uploadValue="top_banner"
    class Meta:
        verbose_name="Banner"
        verbose_name_plural="Banner"
class BottomBanner(models.Model):
    image=models.ImageField(verbose_name="alt banner resmi",upload_to=upload_to)
    uploadValue="bottom_banner"
    class Meta:
        verbose_name="Alt banner"
        verbose_name_plural="Alt banner"
class SocialMedialGallery(models.Model):
    image=models.ImageField(verbose_name="sosyal medya resmi",upload_to=upload_to)
    uploadValue="social_medial_gallery"
    class Meta:
        verbose_name="Sosyal medya galeri"
        verbose_name_plural="Sosyal medya galeri"
class Message(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,verbose_name="user")
    title = models.CharField(max_length=300,blank=True, null=True,verbose_name="mesaj başlığı")
    send_message=models.TextField(verbose_name="Kullanıcı mesaj içeriği",blank=True)
    get_message=models.TextField(verbose_name="Admin mesaj içeriği",default="Beklemede")
    message_date=models.DateField(auto_now_add=True)
    class Meta:
        verbose_name="Kullanıcı mesajları"
        verbose_name_plural="Kullanıcı mesajları"

class SocialMediaLink(models.Model):
    SOCIAL_PATH_CHOICES=[
        ("instagram","M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.9 3.9 0 0 0-1.417.923A3.9 3.9 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.852.174 1.433.372 1.942.205.526.478.972.923 1.417.444.445.89.719 1.416.923.51.198 1.09.333 1.942.372C5.555 15.99 5.827 16 8 16s2.444-.01 3.298-.048c.851-.04 1.434-.174 1.943-.372a3.9 3.9 0 0 0 1.416-.923c.445-.445.718-.891.923-1.417.197-.509.332-1.09.372-1.942C15.99 10.445 16 10.173 16 8s-.01-2.445-.048-3.299c-.04-.851-.175-1.433-.372-1.941a3.9 3.9 0 0 0-.923-1.417A3.9 3.9 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599s.453.546.598.92c.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.5 2.5 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.5 2.5 0 0 1-.92-.598 2.5 2.5 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233s.008-2.388.046-3.231c.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92s.546-.453.92-.598c.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92m-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217m0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334"),
        ("whatsapp","M13.601 2.326A7.85 7.85 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.9 7.9 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.9 7.9 0 0 0 13.6 2.326zM7.994 14.521a6.6 6.6 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.56 6.56 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592m3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.73.73 0 0 0-.529.247c-.182.198-.691.677-.691 1.654s.71 1.916.81 2.049c.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232",),
        ("facebook","M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951",),
        ("tiktok","M9 0h1.98c.144.715.54 1.617 1.235 2.512C12.895 3.389 13.797 4 15 4v2c-1.753 0-3.07-.814-4-1.829V11a5 5 0 1 1-5-5v2a3 3 0 1 0 3 3z",),
        ("threads","M6.321 6.016c-.27-.18-1.166-.802-1.166-.802.756-1.081 1.753-1.502 3.132-1.502.975 0 1.803.327 2.394.948s.928 1.509 1.005 2.644q.492.207.905.484c1.109.745 1.719 1.86 1.719 3.137 0 2.716-2.226 5.075-6.256 5.075C4.594 16 1 13.987 1 7.994 1 2.034 4.482 0 8.044 0 9.69 0 13.55.243 15 5.036l-1.36.353C12.516 1.974 10.163 1.43 8.006 1.43c-3.565 0-5.582 2.171-5.582 6.79 0 4.143 2.254 6.343 5.63 6.343 2.777 0 4.847-1.443 4.847-3.556 0-1.438-1.208-2.127-1.27-2.127-.236 1.234-.868 3.31-3.644 3.31-1.618 0-3.013-1.118-3.013-2.582 0-2.09 1.984-2.847 3.55-2.847.586 0 1.294.04 1.663.114 0-.637-.54-1.728-1.9-1.728-1.25 0-1.566.405-1.967.868ZM8.716 8.19c-2.04 0-2.304.87-2.304 1.416 0 .878 1.043 1.168 1.6 1.168 1.02 0 2.067-.282 2.232-2.423a6.2 6.2 0 0 0-1.528-.161",)
    ]
    link=models.CharField(verbose_name="link",blank=True,null=True,max_length=300)
    path=models.CharField(verbose_name="sosyal media",blank=True,null=True,max_length=1000, choices=SOCIAL_PATH_CHOICES)
    username=models.CharField(verbose_name="facebook",blank=True,max_length=300)
    
    class Meta:
        verbose_name="Sosyal medya linkleri"
        verbose_name_plural="Sosyal medya linkleri"
class RelavantInfo(models.Model):
    
    contact=models.TextField(verbose_name="iletişim",blank=True,null=True)
    about=models.TextField(verbose_name="hakkımızda",blank=True,null=True)
    conditions=models.TextField(verbose_name="koşullar",blank=True,null=True)
    class Meta:
        verbose_name="İlgili bilgiler"
        verbose_name_plural="ilgili bilgiler"

    
class CargoPrice(models.Model):
    cargo_price=models.DecimalField(verbose_name="Kargo fiyatı",null=True,blank=True,default=0,max_digits=10000,decimal_places=2)
    class Meta:
        verbose_name="Kargo fiyatı"
        verbose_name_plural="Kargo fiyatı"

class ContractTerms(models.Model):
    preInfo=models.TextField(verbose_name="Ön bilgilendirme Şartı",null=True,blank=True)
    distanceSellingAgreement=models.TextField(verbose_name="Mesafeli Satış Sözleşmesi",null=True,blank=True)
    class Meta:
        verbose_name="Sözleşme şartları"
        verbose_name_plural="Sözleşme şartları"