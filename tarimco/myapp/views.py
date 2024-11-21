from django.shortcuts import render,redirect ,get_object_or_404
from django.contrib import messages
from django.views import View
from .models import *
from django.db.models import Q

from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate,logout

from .forms import RegisterForm, LoginForm, ProductForm, IletisimForm, CommentForm
from django.core.exceptions import PermissionDenied

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse


#Kayıt ve Login-Logout
class RegisterView(View):
    initial = {'key': 'value'}
    template_name = 'registration/uyeol.html'
    form_class = RegisterForm  # form_class'ı tanımladık
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()  # GET isteğinde boş form kullanılır
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)  # POST isteğinde dosya verilerini de al
        if form.is_valid():
            user = form.save(commit=False)
            is_farmer = form.cleaned_data.get('is_farmer')
            user.is_farmer = is_farmer  # is_farmer bilgisi kullanıcıya atanıyor
            user.save()
            
            # Kullanıcıyı authenticate et
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
            
            if user is not None:
                login(request, user)  # auth_login yerine login kullanılıyor
                username = form.cleaned_data.get('username')
                if is_farmer:
                    messages.success(request, f"A farmer account created for {username}")
                else:
                    messages.success(request, f"A user account created for {username}")
            
                return redirect('home')  # Başarılı bir şekilde işlendikten sonra yönlendir
            
        return render(request, self.template_name, {'form': form})

class CustomLoginView(LoginView):
    form_class = LoginForm
    
    def form_valid(self,form):
        remember_me = form.cleaned_data.get('remember_me')
        
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        
        return super(CustomLoginView,self).form_valid(form)

def logoutView(request):
    logout(request)
    return render(request , 'registration/logout.html')
#Kayıt login logout bitiş

#Contact only
def iletisim(request):
    if request.method == 'POST':
        form = IletisimForm(request.POST)
        if form.is_valid():
            form.save()  # Bu satır form verilerini veritabanına kaydeder

            # Yönlendirme
            return HttpResponseRedirect(reverse('iletisim'))
    else:
        form = IletisimForm()

    return render(request, 'users/iletisim.html', {'form': form})
#Contact only

#Market işlemleri

def urun_ekle(request):
    if not (request.user.is_farmer or request.user.is_superuser):
        raise PermissionDenied

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user
            product.save()
            return redirect('home')
    else:
        form = ProductForm()
    
    return render(request, 'market/urun_ekle.html', {'form': form})

def urun_detay(request, urun_id):
    urun = get_object_or_404(Product, pk=urun_id)
    
    if request.method == 'POST':
        reserve_amount = int(request.POST.get('reserve_amount', 0))
        if reserve_amount < 50 and reserve_amount != urun.quantity:
            messages.error(request, 'Minimum rezervasyon miktarı 50 kg\'dir.')
        elif reserve_amount > urun.quantity:
            messages.error(request, 'Stok yetersiz. Lütfen mevcut stok miktarını aşmayan bir miktar girin.')
        elif urun.quantity - reserve_amount != 0 and urun.quantity - reserve_amount < 50:
            messages.error(request, 'Rezervasyon sonrası stok miktarı en az 50 kg olmalıdır veya tüm stoku rezerve etmelisiniz.')
        else:
            # Ürün rezervasyonunu oluştur
            ReservedProduct.objects.create(
                reserved_by=request.user,
                product=urun,
                reserved_amount=reserve_amount
            )
            # Ürün miktarını güncelle
            urun.quantity -= reserve_amount
            if urun.quantity == 0:
                urun.visible = False  # Ürün miktarı 0 ise görünürlüğü kapat
                urun.save()
                return redirect('market')  # Market sayfasına yönlendir
            urun.save()
            messages.success(request, f'{reserve_amount} kg {urun.name} başarıyla rezerve edildi!')
            return redirect('market')
        
    return render(request, 'market/urun_detay.html', {'urun': urun})

def market(request):
    visible_products = Product.objects.filter(quantity__gt=0)
    return render(request, 'market/market.html', {'products': visible_products})

def search(request):
    query = request.GET.get('q')
    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) | Q(farmer__username__icontains=query)
        )
    else:
        results = None
    return render(request, 'market/search_results.html', {'results': results, 'query': query})

#Market Bitiş

#Ortak Sayfalar
def home(request):
    return render(request, 'users/home.html')

def user_profile(request, user_id):
    profile_user = get_object_or_404(CustomUser, pk=user_id)
    comments = profile_user.profile_comments.filter(parent__isnull=True)
    likes_count = profile_user.liked_by.count()
    dislikes_count = profile_user.disliked_by.count()
    return render(request, 'users/profile.html', {
        'profile_user': profile_user,
        'comments': comments,
        'likes_count': likes_count,
        'dislikes_count': dislikes_count,
        'comment_form': CommentForm(),
    })
@login_required
def like_user(request, user_id):
    liked_user = get_object_or_404(CustomUser, pk=user_id)
    like, created = Like.objects.get_or_create(user=request.user, liked_user=liked_user)
    if Dislike.objects.filter(user=request.user, disliked_user=liked_user).exists():
        Dislike.objects.filter(user=request.user, disliked_user=liked_user).delete()
        
    if not created:
        like.delete()
    
    return redirect('user_profile', user_id=user_id)

@login_required
def dislike_user(request, user_id):
    disliked_user = get_object_or_404(CustomUser, pk=user_id)
    
    if Like.objects.filter(user=request.user, liked_user=disliked_user).exists():
        Like.objects.filter(user=request.user, liked_user=disliked_user).delete()
        
    dislike, created = Dislike.objects.get_or_create(user=request.user, disliked_user=disliked_user)
    if not created:
        dislike.delete()
    return redirect('user_profile', user_id=user_id)

@login_required
def add_comment(request, user_id, parent_id=None):
    profile_user = get_object_or_404(CustomUser, pk=user_id)
    parent_comment = None
    if parent_id:
        parent_comment = get_object_or_404(Comment, pk=parent_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.profile_user = profile_user
            comment.parent = parent_comment
            comment.save()
            
            return redirect('user_profile', user_id=profile_user.id)
        else:
            # Form hatalarını kullanıcıya göster
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect('user_profile', user_id=profile_user.id)
    else:
        form = CommentForm()

    return redirect('user_profile', user_id=profile_user.id)


#Ortak Sayfalar Bitiş

#diğerleri
def politika(request):
    return render(request, 'others/politikalar.html')
def sozlesme(request):
    return render(request, 'others/sozlesmeler.html')
def sss(request):
    return render(request,'others/sss.html')
#diğerleri bitiş