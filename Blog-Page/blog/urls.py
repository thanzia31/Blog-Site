"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from ckeditor_uploader import views as ckeditor_views
from blogapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.index,name='index'),
    path("post/",views.postblog,name='poost'),
    path("allblog/",views.all_posts,name='all_posts'),
    path("accounts/",include('django.contrib.auth.urls')),
    path("register/",views.register_request),
    path("post/<slug:slug>",views.post_by_category),
    path("search/",views.search,name="search_bar"),
    path("author/",views.author,name='author_regis'),
    path("authordis/<slug:slug>",views.author_display),
    path("delpost/<slug:slug>",views.delpost),
    path("updatepost/<slug:slug>",views.updatepost,),
    path("accounts/login/index1/",views.index1,name='index1'),
    path("userinfo/",views.userinfo),
    path("userpost/",views.userpost),
    path("like/<int:pk>",views.likeview,name="like_post"),
    path("liked_post/",views.liked_post),
    path("regiscat/",views.registercategory),
    path('ckeditor/upload',login_required(ckeditor_views.upload),name='ckeditor_upload'),
    path('ckeditor/browse/',never_cache(login_required(ckeditor_views.browse)),name='ckeditor_browse'),
    path('verifyotp/',views.verify_otp,name="verifyotp"),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='blogapp/password_reset.html'),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='blogapp/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='blogapp/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='blogapp/password_reset_complete.html'),name='password_reset_complete'),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)