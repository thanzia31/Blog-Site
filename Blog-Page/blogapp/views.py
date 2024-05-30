from django.shortcuts import render,redirect
from blogapp.models import post,category,authors
from blogapp.forms import Postform,Signup,Authorform,CategoryForm
from django.contrib.auth.decorators import login_required
from django.urls import resolve
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random,concurrent.futures
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from blogapp.post_check import input_model
from blogapp.image_check import input_model_image
# Create your views here.
def index(request):
    
    posts=post.objects.order_by('-timestamp')[0:10]
    cat=category.objects.all()
   
    
    return render(request,'blogapp/index.html',{'post':posts,'cat':cat})
@login_required


def postblog(request):
    cont_flag=True
    img_flag=True
    form=Postform(initial={'author':request.user})
    if authors.objects.filter(username=request.user).exists():
        if request.method=='POST':
            form=Postform(request.POST,request.FILES,initial={'author':request.user})  
            
            if form.is_valid():
                content=form.cleaned_data['content']
                #print(input_model(content))
                predict_cont=input_model(content)
                for i in predict_cont:
                    if i==1 or i==0:
                        cont_flag=False
                        break
                
                
                predict=input_model_image(content)
                print('predict',predict)
                for path,predict_val in predict:
                    if predict_val>0.6:
                        print('Image not  approved ')
                        img_flag=False
                if img_flag and cont_flag:
                    form.save()
                elif img_flag and not cont_flag:
                    print('offensive content')
                    messages.error(request,'Content offensive!!! Modify Your Content To Post Your Blog')
                    return render(request,'blogapp/post.html',{'form':form})
                elif not img_flag and cont_flag:
                    print('offensive images')
                    messages.error(request,'images offensive!!! Remove images as they are explicit')
                    return render(request,'blogapp/post.html',{'form':form})
                else:
                    print('offensive content and images')
                    messages.error(request,'Content and images offensive!!! Modify Your Content and remove or change images To Post Your Blog')
                    return render(request,'blogapp/post.html',{'form':form})

            else:
                print(form.errors)
            return HttpResponseRedirect(reverse(index1))
        return render(request,'blogapp/post.html',{'form':form})
    else:
        return redirect('author_regis')
    
 
def all_posts(request):
    posts=post.objects.all()
    cat=category.objects.all()
    key=str(request.user)
    likes=post.objects.filter(userlikes__icontains=key)
    liked_user=list(likes.values_list('slug'))
    if request.user.is_authenticated:
        loggedin=True
    else:
        loggedin=False
    listt=[i[0] for i in liked_user]
    for i in posts:
        
        if str(i.slug) in listt:
            i.like_field=True
        else:
            i.like_field=False

   
    return render(request,'blogapp/allpost.html',{'post':posts,'cat':cat,'login':loggedin})
@csrf_exempt
def verify_otp(request):
    if request.method=='POST':
        userotp=request.POST.get('otp')
        username=request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        email=request.POST.get('email')
        if password1==password2:
            form=User(first_name=first_name,username=username,last_name=last_name,email=email,password=password1)
            form.save()
            #messages.success("Account Created Successfully!!!Login")
            return redirect("/accounts/login")
    return JsonResponse({'data':'hello'},status=200)
def register_request(request):
    
    if request.method == "POST":
        form = Signup(request.POST)
       
        if form.is_valid():
            otp=random.randint(1000,9999)
            Email=request.POST.get('email')
            username=request.POST.get('username')
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            password1=request.POST.get('password1')
            password2=request.POST.get('password2')
            print(Email)
            send_mail("Blog Corner Verification",f"Verify your account by OTP:{otp}",settings.EMAIL_HOST_USER,[Email],fail_silently=False)
            #user = form.save()
            #login(request, user)
            
            return render(request,'blogapp/verifyOtp.html',{'otp':otp,'email':Email,'username':username,'first_name':first_name,'last_name':last_name,'password1':password1,'password2':password2})
        else:
            user_name=form.data['username']
            first_name=form.data['first_name']
            last_name=form.data['last_name']
            e_mail=form.data['email']
            initial_dict={
                'username':user_name,
                'first_name':first_name,
                'last_name':last_name,
                'email':e_mail
            }
            print(user_name,e_mail,first_name,last_name)
           
            for i in form.errors.values():
                print(i)
                messages.error(request,i)
            
            form=Signup(initial=initial_dict)
            return render (request=request, template_name="blogapp/register.html", context={"form":form})
    form = Signup()
    return render (request=request, template_name="blogapp/register.html", context={"form":form})



def post_by_category(request,slug):
    cate=category.objects.all()[0:10]
    if request.user.is_authenticated:
        loggedin=True
    else:
        loggedin=False
    cat=category.objects.get(slug=slug)
    posts=post.objects.filter(categories=cat)
    return render(request,"blogapp/category_post.html",{'posts':posts,'cat':cate,'login':loggedin})

def search(request):
    queryset = post.objects.all()
    cat=category.objects.all()
    if request.user.is_authenticated:
        loggedin=True
    else:
        loggedin=False
    query = request.GET.get('q')
    key=str(request.user)
    likes=post.objects.filter(userlikes__icontains=key)
    liked_user=list(likes.values_list('slug'))
   
    listt=[i[0] for i in liked_user]
    for i in queryset:
        
        if str(i.slug) in listt:
            i.like_field=True
        else:
            i.like_field=False
    
    if query:

        queryset = queryset.filter(
            Q(title__icontains=query) )
            #or  Q(author_icontains=query))	
    context = {
        'queryset': queryset,
        'login':loggedin,
        'cat':cat
        }
    return render(request, 'blogapp/search_bar.html',context)

def author(request):
    current_user=request.user
    name=current_user.username
    email=current_user.email
    first=current_user.first_name
    last=current_user.last_name
    initial_dict={
        'username':name,
        'email':email,
        'firstname':first,
        'lastname':last}
    form=Authorform(initial=initial_dict)
    
    if request.method=='POST':
        form=Authorform(request.POST,request.FILES,initial=initial_dict)
        if form.is_valid:
            form.save()
        return post(request)
    return render(request,'blogapp/author.html',{'form':form})

def author_display(request,slug):
    posts=post.objects.get(slug=slug)
    auth_name=posts.author_id
    
    post_count=post.objects.filter(author_id=auth_name).count()
  
    aut=authors.objects.get(username=auth_name)
    return render(request,'blogapp/author_display.html',{'aut':aut,'count':post_count})

def delpost(request,slug):
    posts=post.objects.get(slug=slug)
    if (str(request.user)==str(posts.author)):
        
        posts.delete()
        return redirect("/userpost")
    else:
        messages.info(request,'You cannot delete this post!!')
    
def updatepost(request,slug):
    
    posts=post.objects.get(slug=slug)
    form=Postform(instance=posts)
    
    if (str(request.user)==str(posts.author)):
        
        if request.method=='POST':
            
            form=Postform(request.POST,instance=posts)
            if form.is_valid():
                print("valid")
                form.save()
            return redirect("/userpost")
    else:
        return redirect("/userpost")
    return render(request,"blogapp/updatepost.html",{'form':form})


def index1(request):
    posts=post.objects.order_by('-timestamp')[0:10]
    cat=category.objects.all()
    key=str(request.user)
    likes=post.objects.filter(userlikes__icontains=key)
    liked_user=list(likes.values_list('slug'))
    listt=[i[0] for i in liked_user]
    for i in posts:
        
        if str(i.slug) in listt:
            i.like_field=True
        else:
            i.like_field=False
    return render(request,'blogapp/index1.html',{'post':posts,'cat':cat})

def userinfo(request):
    info=User.objects.get(username=request.user)
    return render(request,'blogapp/userinfo.html',{'info':info})

def userpost(request):
    try:
        aut=authors.objects.get(username=request.user)
        name=aut.username
        posts=post.objects.filter(author=name)
        return render(request,'blogapp/userpost.html',{'posts':posts})

    except ObjectDoesNotExist:
        return render(request,'blogapp/userpost.html',{'posts':None})
    
@login_required
def likeview(request,pk):
    post_id=request.POST.get("post_id")
    print(pk)
    posts=post.objects.get(id=pk)
    key=str(request.user)
    if posts.likes.filter(id=request.user.id).exists():
        posts.likes.remove(request.user)
        posts.like_field=False
        posts.userlikes.pop(key)
        
        posts.save()
        
    else:
        posts.likes.add(request.user)
        posts.like_field=True
        posts.userlikes[key]=key
        
        posts.save()
        
    data={
        'value':posts.like_field,
        'likes':posts.likes.all().count()
    }
    return JsonResponse(data,safe=False)
    return render(request,'blogapp/index1.html',{'post':ten_posts,'cat':cat})
    
    

def liked_post(request):
    liked=User.objects.get(username=request.user).blog_posts.all()
    key=str(request.user)
    
    
    likes=post.objects.filter(userlikes__icontains=key)
    liked_user=list(likes.values_list('slug'))
    listt=[i[0] for i in liked_user]
    for i in liked:
        
        if str(i.slug) in listt:
            i.like_field=True
        else:
            i.like_field=False

    return render(request,"blogapp/liked_post.html",{'liked':liked})

def registercategory(request):
    form=CategoryForm()
    err=False
    if request.method == 'POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            err=True
            return render(request,'blogapp/registercat.html',{'form':form,'err':err})

        return redirect ("poost")
    return render(request,'blogapp/registercat.html',{'form':form})

        
  


    


    