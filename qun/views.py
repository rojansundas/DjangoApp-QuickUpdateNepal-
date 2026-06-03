from django.shortcuts import render
from .models import*
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login,logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Comment
from rest_framework import viewsets
from .serializer import NewsSerializer
from rest_framework.permissions import IsAuthenticated


class NewsViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=News.objects.all()
    serializer_class=NewsSerializer






def index(request):
    news_list=News.objects.all()
    paginator = Paginator(news_list,6)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number)

    data={
        'newsData':page_obj
    }
    return render(request,'pages/index.html',data)

def newsDetails(request, slug):
    news = News.objects.get(slug=slug)
    catId = news.category.id

    comments = news.comments.all().order_by('-created_at')

   
    if request.method == "POST":
        if request.user.is_authenticated:
            content = request.POST.get('content')

            if content:  # prevent empty comment
                Comment.objects.create(
                    news=news,
                    user=request.user,
                    content=content
                )
            return redirect('news-details', slug=slug)

    data = {
        'news': News.objects.get(slug=slug),
        'relatedNews': News.objects.filter(category_id=catId).exclude(id=news.id)[:10],
        'comments': comments, 
    }

    return render(request, 'pages/news-details.html', data)

def LatestNews(request):
    data={
        'latestNewsData':News.objects.all().order_by('-published_at')[:6]
    }          
    return render(request,'pages/latestnews.html',data)

def category_list(request):
    data={
        'categoryData':Category.objects.all(),
    }
    return render(request,'pages/category.html',data)

def categoryDetails(request,slug):
    data={
        'category':Category.objects.get(slug=slug),
    }
    return render(request,'pages/category-details.html',data)


from django.db.models import Q

def search(request):
    searchKey = request.GET.get('criteria', '')

    if searchKey:
        findData = News.objects.filter(
            Q(title__icontains=searchKey) |
            Q(description__icontains=searchKey) |
            Q(category__name__icontains=searchKey)
        )
    else:
        findData = News.objects.none()

    return render(request, 'pages/search-list.html', {
        'newsData': findData,
        'searchKey': searchKey,
    })

   
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

      
        Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message,
        )

        full_message = f"""
        Name: {name}
        Phone: {phone}
        Email: {email}

        Message:
        {message}
        """

        send_mail(
            subject,
            full_message,
            settings.EMAIL_HOST_USER, 
            ['sundasrojan@gmail.com'],
            fail_silently=False,
        )

        messages.success(request, "Your message is sent!")

    return render(request, 'pages/contact.html')

def login(request):
      if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            messages.error(request,'Invalid credentials')
            return render(request, 'pages/login.html')

      return render(request, 'pages/login.html')



def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

   
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'pages/register.html')


def account_logout(request):
    logout(request)
    return redirect('login')


@login_required()
def profile(request):
    return render(request, 'pages/profile.html')




