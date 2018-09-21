from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
# from django.contrib.auth.forms import RegistrationForm, UserChangeForm, PasswordChangeForm,
import datetime
from .forms import Edit, RegistrationForm,Post_Con
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.contrib.auth import authenticate
from .forms import RegistrationForm
# from datetime import datetime
from django.contrib.auth import logout,login
from django.contrib import messages
from thanos import settings
from django.shortcuts import render_to_response,render, redirect
from django.template import RequestContext
# from conda.models import Post
# from conda.forms import Doc_form
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
import urllib
import json
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from .token import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .models import UserProfile,Friend,Room, Notification,Post
from django.contrib.auth.models import User
from django.core import serializers
from django.utils import timezone

# from .forms import RegistrationForm, Edit




@login_required
def chat(request):
    return render(request,'chat.html')

@login_required
def notifications(request):
    return render(request, 'not.html')

@login_required(login_url='/')
def change_password(request):
    if request.method=="POST":
        form = PasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request, user)
            messages.success(request,'Your password was successfully updated!')
            return redirect('marvel:login')
        else:
            return render(request,'change.html',{'forms':form})
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'forms':form}
    return render(request,'change.html',args)

@login_required
def friends(request):
    return render(request, 'friend.html')

@login_required
def profile(request):
    user_info = UserProfile.objects.filter(user = request.user)
    post = Post.objects.filter(user=request.user)
    # form = HomeForm()
    # posts = Post.objects.all().order_by('-created')
    # users = User.objects.exclude(id=request.user.id)
    try:            
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()
        
        # 'form': form, 'posts': posts,'users': users,
        args = {
            'friends': friends
        }
        return render(request, 'profile.html',{'user_info':user_info,'friends': friends,'post':post})
    except:
        friends =None
        friend_t = None
        post = None           
        for u in user_info:
            print(u.user_profile)
            print(u.Birthdate)
            print(u.about)
        return render(request, 'profile.html',{'user_info':user_info,'friends': friends,'post':post})


@login_required
def other_profile(request,user):
    print(user)
    use = User.objects.get(username=user)
    user_i = User.objects.filter(username=user)
    print(user_i)
    user_info = UserProfile.objects.filter(user=user_i)
    print(user_info)
    post = Post.objects.filter(user=use)
    print(post)
    # form = HomeForm()
    # posts = Post.objects.all().order_by('-created')
    # users = User.objects.exclude(id=request.user.id)
    try:
        friend_t = Friend.objects.get(current_user=request.user,users=user_i)
        friend = Friend.objects.get(current_user=user_i)
        friends = friend.users.all()
        # 'form': form, 'posts': posts,'users': users,
        args = {
            'friends': friends
        }
        print("hi")
        for u in user_i:
            print(u.first_name)
            print(u.last_name)
        return render(request, 'other_user.html',{'user_i':user_i,'user_info':user_info,'friends': friends,'fr':friend_t,'post':post})
    except:
        try:
            friend = Friend.objects.get(current_user=user_i)
            friends = friend.users.all()
            friend_t = None
            user_i = User.objects.filter(username=user)         
            for u in user_info:
                print(u.user_profile)
                print(u.Birthdate)
                print(u.about)
            for u in user_i:
                print(u.last_name)
            return render(request, 'other_user.html',{'user_info':user_info,'friends': friends,'fr':friend_t,'user_i':user_i,'post':post})
        except:
            friends = None
            friend_t = None
            user_i = User.objects.filter(username=user)         
            for u in user_info:
                print(u.user_profile)
                print(u.Birthdate)
                print(u.about)
            for u in user_i:
                print(u.last_name)
            return render(request, 'other_user.html',{'user_info':user_info,'friends': friends,'fr':friend_t,'user_i':user_i,'post':post})


@login_required
def frprofile(request,frid):
    user_i = User.object.get(pk=frid)
    user_info = UserProfile.objects.filter()
    posts = Post.objects.all().order_by('-created')
    # users = User.objects.exclude(id=request.user.id)
    for u in user_info:
        print(u.user_profile)
        print(u.Birthdate)
        print(u.about)
    return render(request, 'profile.html',{'user_info':user_info,'friends': friends})

def change_friends(request, operation, pk):
    friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, friend)
    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)
    return redirect('marvel:profile')



@login_required
def edit(request):
    if request.method == 'POST':
        form = Edit(request.POST,request.FILES)
        if form.is_valid():
            print("hi")
            profile = form.save(commit=False)
            profile.user = request.user
            form.save()
            # edit.save()
            return redirect('marvel:profile')
        else:
            return render(request, 'edit.html',{'form':form})
    else:
        form = Edit()
        return render(request, 'edit.html',{'form':form})


@login_required
def tril(request):
    return render(request,'tril.html')

@login_required
def timeline(request):
    now = datetime.datetime.now()
    timef = now.strftime('%H:%M')
    datef = now.strftime('%Y-%m-%d')
    print(datef)
    print(timef)
    posts1 = Post.objects.filter(post_date__lte=datef,post_time__lte=timef).order_by('-post_date').order_by('-post_time')
    for p in posts1:
        p.fetch = True
        p.save()
    if request.method =='POST':
        form = Post_Con(request.POST,request.FILES)
        # posts1 = Post.objects.order_by('-post_time')
        if form.is_valid():
            print("false")
            post_data = form.save(commit=False)
            post_data.user= request.user
            post_data.save()
            return render(request, 'timeline.html', {'form':form,'post_content':posts1})
        else:
            print("HI1")
            print(form.errors)
            context = {
            'form':form,'post_content':posts1
            }
            return render(request, 'timeline.html', context)
    else:
        print("HI2")
        form = Post_Con()
        return render(request, 'timeline.html', {'form':form,'post_content':posts1})
        
    # img1 = request.FILES.get('img')
    # msg1 = request.POST.get('msg')
    # date1 = request.POST.get('date') or None
    # time1 = request.POST.get('time') or None
    # print(img1)
    # print(msg1)
    # print(date1)
    # print(time1)
    # if request.method == "POST":
    #     form = Post(user=request.user,post_msg=msg1,post_img=img1,post_date=date1,post_time=time1)
    #     if img1 and msg1:
    #         form.save()
    #         posts1 = Post.objects.order_by('-post_time')
    #         for p in posts1:
    #             print(p.post_img)
    #         return render(request, 'timeline.html', {'post_content':posts1})
    #     else:
    #         posts1 = Post.objects.order_by('-post_time')
    #         for p in posts1:
    #             print(p.post_img)
    #         return render(request, 'timeline.html', {'post_content':posts1})
    # else:
    #     posts1 = Post.objects.order_by('-post_time')
    #     for p in posts1:
    #         print(p.post_img)
    #     return render(request, 'timeline.html',{'post_content':posts1})


def index(request):
    if request.session.get('user') != '' and request.session.get('user') != None:
        print(request.user.username)
        return redirect('marvel:timeline')
    else:
        # if request.method == "POST":
        #     username = request.POST['username']
        #     password = request.POST['password']
        #     user = authenticate(username=username, password=password)
        #     if user is not None:
        #         login(request, user)
        #         # posts = Post.objects.filter(user=request.user)
        #         return render(request, 'timeline.html',{'error_message':'Sorry!! Not a User'})
        #     else:
        #         # but points here .. doesn't catch the user...
        #         return render(request, 'chat.html', {'error_message': 'Invalid login'})
        return render(request, 'login.html')

def forgot(request):
    return render(request, 'forgot.html')



def register(request):
    if request.session.get('user') != '' and request.session.get('user') != None:
        return redirect('marvel:timeline')
    else:
        if request.method =='POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():            
                userObj = form.cleaned_data
                username = userObj['username']
                email =  userObj['email']
                firstname = userObj['first_name']
                lastname = userObj['last_name']
                password = userObj['password']             
                recaptcha_response = request.POST.get('g-recaptcha-response')
                url = 'https://www.google.com/recaptcha/api/siteverify'
                values = {
                    'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                    'response': recaptcha_response
                }
                data = urllib.parse.urlencode(values).encode()
                req =  urllib.request.Request(url, data=data)
                response = urllib.request.urlopen(req)
                result = json.loads(response.read().decode())
                print(result)
                if result['success'] and data:
                    if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                        userc = User.objects.create_user(username, email,password)
                        userc.is_active=False
                        userc.first_name=firstname
                        userc.last_name=lastname
                        userc.save()
                        current_site = get_current_site(request)
                        mail_subject = 'Activate your ChatMash Account account.'
                        message = render_to_string('acc_active_email.html', {
                            'user': userc,
                            'domain': current_site.domain,
                            'uid':urlsafe_base64_encode(force_bytes(userc.pk)),
                            'token':account_activation_token.make_token(userc),
                        })
                        to_email = form.cleaned_data.get('email')
                        email = EmailMessage(
                                    mail_subject, message, to=[to_email]
                        )
                        email.send()
                        messages.success(request,'Please confirm your email address to complete the registration') 
                        user = authenticate(username = username, password = password)
                        login(request, user)
                        request.session['user'] = username                 
                        return redirect('marvel:edit')
                        
                    else:
                        messages.error(request, 'Look like email id or username already register')
                        return render(request, 'register.html', {'forms':form})
                    # user = authenticate(username=form.username, password=form.password)
                    # if user is not None:
                    #     login(request, user)
                    #     # posts = Post.objects.filter(user=request.user)
                    # return redirect('conda:login_user')
                    # else:
                    #     return HttpResponse("NOT DONE")
                else:
                    print("HI")
                    messages.error(request, 'Invalid reCAPTCHA ')
                    return render(request, 'register.html', {'forms':form})
            else:
                print("HI1")
                print(form.errors)
                context = {
                'forms':form
                }
                return render(request, 'register.html', context)
        else:
            print("HI2")
            form = RegistrationForm()
            return render(request, 'register.html', {'forms':form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
         # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')



def login_user(request):
    if request.session.get('user') != '' and request.session.get('user') != None:
        return redirect('marvel:timeline')
    else:
        if request.method =='POST':
            username = request.POST['username']
            password = request.POST['password']
            print(username)
            print(password)
            user = authenticate(username = username, password = password)
            if user is None:
                messages.error(request,"Please Enter valid Username or Password")
                return render(request, 'login.html')
            else:
                login(request, user)
                request.session['user'] = username                 
                return redirect('marvel:profile')
        else:
            return render(request, 'login.html')
    

@login_required
def logout_view(request):
    logout(request)
    request.session['user']= '' or None
    return redirect('marvel:index')

@login_required
def re_no(request):
    n = Notification.objects.filter(User=str(request.user))
    for nt in n:
        print(nt.viewed)
        nt.viewed=True
        nt.save()
    return JsonResponse({"suc":True})
   


@login_required
def Add_Room(request):
    c_us = request.user
    u = User.objects.all()
    nu = str(request.user)
    # print(Room._meta.get_fields())
    # r5 = Room.objects.exclude(id=0).order_by("title")
    print(request.user)
    try:
        friend = Friend.objects.get(current_user=request.user)
    except:
        try:
            post = Post.objects.filter(user=request.user)
            if post is None:
                friends =None
                friend_t = None
                post = None  
                user_info = UserProfile.objects.filter(user = request.user)         
                for u in user_info:
                    print(u.user_profile)
                    print(u.Birthdate)
                    print(u.about)
                return render(request, 'profile.html',{'user_info':user_info,'friends': friends,'post':post,'m':"You have no Friend yet"})
            else:
                friends =None
                friend_t = None
                user_info = UserProfile.objects.filter(user = request.user)         
                for u in user_info:
                    print(u.user_profile)
                    print(u.Birthdate)
                    print(u.about)
                return render(request, 'profile.html',{'user_info':user_info,'friends': friends,'post':post,'m':"You have no Friend yet"})
        except:
            friends =None
            friend_t = None
            post = None  
            user_info = UserProfile.objects.filter(user = request.user)         
            for u in user_info:
                print(u.user_profile)
                print(u.Birthdate)
                print(u.about)
            return render(request, 'profile.html',{'user_info':user_info,'friends': friends,'post':post,'m':"You have no Friend yet"})

    friends = friend.users.all()
    n = Notification.objects.filter(User=str(request.user),viewed=False)
    for notifi in n:
        print(notifi.User)
        print(notifi.sender)
        print(notifi.message)

        # except:
        #     print("hello")


        # c = str(c_us.id)
        # for uf in uo:
        #     lu = str(uf.id)
        #     fin = c+lu
        #     # print(fin)
        #     f = int(fin)
        #     r = Room.objects.all()

        #     for r1 in r:
        #         # if r1.id:

        #             if r1.id!=f or r1.id == "":
        #                 print(f)
        #                 print(r1.id)
        #              # print(uf.username)
        #                 try:
        #                     fur = Room.objects.create(id=f,title=uf.username,staff_only=True)
        #                     fur.save()
        #                 except:
        #                     print("room already present")
        #         # else:
                #     try:
                #         fur = Room.objects.create(id=f,title=uf.username,staff_only=True)
                #         fur.save()
                #     except:
                #         print("room already present")
                            
    return render(request, "chat.html",{"user": friends,"notification": n,})
   

@login_required
def AROOM(request):
    c_us = request.user
    lu=str(request.POST.get('recv'))
    lu_n=str(request.POST.get('rec_n'))

    r5 = Room.objects.exclude(id=0).order_by("title")
    sende_t = str(c_us.username)
    c = str(c_us.id)
    fin = c+lu
    # print(fin)
    cht_title = sende_t + " and " + lu_n 
    f = int(fin)
    r = Room.objects.all()
    uo = User.objects.get(id = int(lu))
    ntsen = str(request.user)
    ntrec = str(uo.username)
    for r1 in r:
        # if r1.id:
        if r1.id!=f:
            print(f)
            print(r1.id)
            # print(uf.username)
            try:
                fur = Room.objects.create(id=f,title=cht_title,staff_only=False)
                n=Notification()
                n.add_notification(f,ntrec,ntsen)
                fur.save()
                print(f)
                return JsonResponse({'rid':f})
            except:
                print("room already present")
                n=Notification()
                n.add_notification(f,ntrec,ntsen)
                print(f)
                return JsonResponse({'rid':f})                 # else:
                    #     try:
                    #         fur = Room.objects.create(id=f,title=uf.username,staff_only=True)
                    #         fur.save()
                    #     except:
                    #         print("room already present")
                                
    

@login_required
def index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    rooms = Room.objects.order_by("title")
    c_id = request.user
    cus_id = c_id.id
    print(cus_id)
    # Render that in the index template
    return render(request, "index.html", {
        "rooms": rooms,"cus": cus_id,
    })


# @login_required
# def friend_sent_Req(request,receiver):
#     other_user = User.objects.get(pk=receiver)
#     Friend.objects.add_friend(
#     request.user,                               # The sender
#     other_user,                                 # The recipient
#     message='Hi! I would like to add you')      # This message is optional
@login_required
def view_not(request):
    n = Notification.objects.filter(User=str(request.user),viewed=False,fetch=False)    
    cou = 0

    if(n):
        for nt in n:
            nt.fetch=True
            nt.save()
        not_ser = serializers.serialize('json', n)
        cou = len(list(n))
        # print(type(not_ser))
        # notification = list(n)
        return JsonResponse({'n_n':not_ser,'co':cou},safe=False)
    else:
        return JsonResponse({'n_n':"True"})

@login_required
def view_post(request):
    now = datetime.datetime.now()
    timef = now.strftime('%H:%M')
    datef = now.strftime('%Y-%m-%d')
    print(datef)
    print(timef)
    posts1 = Post.objects.filter(post_date__lte=datef,post_time__lte=timef,fetch=False).order_by('-post_date').order_by('-post_time')
    print(posts1)
    if(posts1):
        for nt in posts1:
            nt.fetch=True
            nt.save()
        not_ser = serializers.serialize('json', posts1)
        # print(type(not_ser))
        # notification = list(n)
        return JsonResponse({'post':not_ser},safe=False)
    else:
        return JsonResponse({'post':"True"})

def ser_user(request):
    usename = request.GET.get('username')    
    u = User.objects.filter(first_name__iexact=usename)
    print(u)
    if u:
        not_ser = serializers.serialize('json', u)
        return JsonResponse({'n_n':not_ser},safe=False)
    else:
        return JsonResponse({'n_n':"True"})