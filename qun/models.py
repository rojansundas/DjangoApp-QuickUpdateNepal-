from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

# Create your models here.


class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    slug=models.SlugField(max_length=100,unique=True)



    def __str__(self):
        return self.name
    
class News(models.Model):
    category=models.ForeignKey(Category,on_delete=models.PROTECT)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title= models.CharField(max_length=100)
    slug=models.SlugField(max_length=100,unique=True)
    description=models.TextField()
    image=models.ImageField(upload_to='new_images/',null=True,blank=True)
    published_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural='News'

class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=20)
    subject=models.CharField(max_length=200)
    message=models.CharField(max_length=200)
    create_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name





def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # 🔴 Validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        # Optional: check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        # ✅ Create user
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'register.html')


class Comment(models.Model):
    news = models.ForeignKey('News', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.news.title}"

        