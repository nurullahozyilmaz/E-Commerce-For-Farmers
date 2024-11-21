from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    adress = models.CharField(max_length=250, verbose_name='Adres bilgileri')
    is_farmer = models.BooleanField(default=False, verbose_name='Çiftçi misin?')
    profile_image = models.ImageField(upload_to='media/profile_images/', null=True, blank=True)
    dislikes_received = models.IntegerField(default=0)
    likes_received = models.IntegerField(default=0)


    def __str__(self):
        return self.username
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    farmer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='media/product_images/', null=True, blank=True)

    class Meta:
        ordering = ['name', '-created_at']

    def __str__(self):
        return self.name

    def formatted_created_at(self):
        return self.created_at.strftime("%d %B %Y")

class Iletisim(models.Model):
    i_name = models.CharField(max_length=100)
    i_email = models.EmailField()
    i_message = models.TextField()

    def __str__(self):
        return self.i_name

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    liked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='liked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'liked_user')

class Dislike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='dislikes')
    disliked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='disliked_by')
    created_at = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        unique_together = ('user', 'disliked_user')
        
class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    profile_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='profile_comments')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.profile_user.username}'
    
class ReservedProduct(models.Model):
    reserved_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Rezervasyon yapan kullanıcı
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Rezerve edilen ürün
    reserved_amount = models.PositiveIntegerField()  # Rezerve edilen miktar
    reserved_at = models.DateTimeField(auto_now_add=True)  # Rezervasyon tarihi ve saati

    def __str__(self):
        return f"{self.reserved_amount} kg {self.product.name} - {self.reserved_by.username} {self.reserved_at}"