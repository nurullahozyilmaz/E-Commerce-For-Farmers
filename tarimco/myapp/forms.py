from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm 
from .models import CustomUser, Product, Iletisim, Comment

class RegisterForm(UserCreationForm):
    
    first_name = forms.CharField(max_length=100,
                                  required=True,
                                  widget=forms.TextInput(attrs={'placeholder': 'Adı',
                                                                'class': 'form-control',}))
    last_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Soyadı',
                                                               'class': 'form-control',}))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Kullanıcı adı',
                                                             'class': 'form-control',}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'E-mail',
                                                           'class': 'form-control',}))
    adress = forms.CharField(max_length=250, 
                             required=True,
                             widget= forms.TextInput(attrs={'placeholder':'Adres bilgileri',
                                                            'class':'form-control'}))
    password1 = forms.CharField(max_length=50,
                                 required=True,
                                 widget=forms.PasswordInput(attrs={'placeholder': 'Şifre','class': 'form-control',
                                                                   'data-toggle': 'password',
                                                                   'id': 'password',}))
    password2 = forms.CharField(max_length=50,
                                 required=True,
                                 widget=forms.PasswordInput(attrs={'placeholder': 'Şifre Doğrulama',
                                                                   'class': 'form-control',
                                                                   'data-toggle': 'password','id': 'password',}))
    is_farmer = forms.BooleanField(label="Çiftçi Misin?", required=False)
    profile_image = forms.FileField(required = True,
                                    widget= forms.FileInput(attrs={'class':'form-control-file', 'accept': 'image/*'}))
    
    

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'adress', 'is_farmer','profile_image']
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget= forms.TextInput(attrs={'placeholder':'Kullanıcı Adı',
                                                              'class': 'form-control',
                                                              }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder':'Şifre',
                                                                 'class':'form-control',
                                                                 'id':'password',
                                                                 'data-toggle':'password',
                                                                 'name':'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)
    
    class Meta:
        model = CustomUser
        fields= ['username', 'password', 'remember_me']

class ProductForm(forms.ModelForm):
    name = forms.CharField(
        label='İsim',
        widget=forms.TextInput(attrs=
                               {'class': 'form-control', 
                                'placeholder': 'Ürün adı girin...'}),
        initial=''
    )
    price = forms.IntegerField(
        label='Fiyat',
        widget=forms.NumberInput(attrs=
                                 {'class': 'form-control',
                                  'placeholder': 'Fiyatı girin...'}),
        initial=''
    )
    description = forms.CharField(
        label='Açıklama',
        widget=forms.TextInput(attrs=
                               {'class': 'form-control', 
                                'placeholder': 'Açıklama girin...'}),
        initial=''
    )
    quantity = forms.IntegerField(
        label='Miktar',
        widget=forms.NumberInput(attrs=
                                 {'class': 'form-control', 
                                  'placeholder': 'Miktarı girin...', 'min':'50'}),
        initial=''
    )
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'quantity','image']
    
    widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ürün Adı', 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Fiyat', 'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'description': forms.Textarea(attrs={'placeholder': 'Ürün Açıklaması', 'class': 'form-control', 'rows': 5}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'Miktar', 'class': 'form-control', 'step':'1', 'min':'1'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'})  # Sadece resim dosyalarını kabul et
        }

class IletisimForm(forms.ModelForm):
    i_message = forms.CharField(widget=forms.Textarea(attrs={'maxlength': 300,'placeholder': 'Mesajınız'}) )

    class Meta:
        model = Iletisim
        fields = ['i_name', 'i_email', 'i_message']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Yorumunuzu buraya yazın...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].required = True