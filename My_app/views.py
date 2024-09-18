from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import smtplib
from email.mime.text import MIMEText
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import login_table, user_table



# Create your views here.
from My_app.models import *


def home(request):
    return render(request,"index.html")


def login(request):
    return render(request,"loginindex.html")


def forgotpassword(request):
    return render(request,"forgot_password.html")

def forgot_password_post(request):
    un = request.POST['mail']
    try:
        # Fetch the user object
        ob = user_table.objects.get(email=un)

        # Setup email
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            # Use a more secure way of handling credentials like environment variables
            gmail.login('yadu01123@gmail.com', 'cnoa qzrv ejhm hszr')
            print("Email login successful")
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
            return HttpResponseRedirect(reverse('forgot_password'))  # Redirect back to forgot password page on failure

        # Create the email message
        msg = MIMEText("Your password is : " + str(ob.LOGIN.password))

        msg['Subject'] = 'Password Recovery - BookHive'
        msg['To'] = un
        msg['From'] = 'yadu01123@gmail.com'

        # Send the email
        try:
            gmail.send_message(msg)
            gmail.quit()  # Close the connection after sending
            return HttpResponseRedirect(reverse('login'))  # Redirect to login page after sending
        except Exception as e:
            print("Failed to send email: " + str(e))
            return HttpResponseRedirect(reverse('forgot_password'))  # Redirect back to forgot password page

    except login_table.DoesNotExist:
        # User with the provided username doesn't exist
        return HttpResponseRedirect(reverse('forgot_password'))  # Redirect back to forgot password page

def logincode(request):
    if request.method == 'POST':
        username = request.POST.get('mail')
        pwd = request.POST.get('Password')

        ob = login_table.objects.filter(username=username, password=pwd)
        if ob.exists():
            ob1 = login_table.objects.get(username=username, password=pwd)
            request.session['lid'] = ob1.id
            if ob1.type == 'admin':
                return HttpResponse('''<script>window.location='/adminhome'</script>''')
            elif ob1.type == 'user':
                return HttpResponse('''<script>window.location='userhome'</script>''')
            else:
                return HttpResponse('''<script>window.location='/'</script>''')
        else:
            if not login_table.objects.filter(username=username).exists():
                messages.error(request, "Username does not exist.")
            else:
                messages.error(request, "Incorrect password.")
            return render(request, 'loginindex.html')  # Render the login page with the error message
    return render(request, 'loginindex.html')


def adminhome(request):
    ob=user_table.objects.all()
    ob1 = book_table.objects.all()
    ob3 = book_table.objects.filter(status='Available')
    # ob2 = order_table.objects.all()
    ob2=[]

    return render(request, "admin/adminindex.html",{"tu":len(ob),"tu1":len(ob1),"tu2":len(ob3)})


def userhome(request):
    ob=book_table.objects.exclude(user_id__LOGIN__id=request.session['lid'])
    return render(request, "user/userindex.html",{"val":ob})

def sellerhome(request):
    ob = book_table.objects.filter(user_id__LOGIN__id=request.session['lid'])
    return render(request, "user/sellerindex.html",{"val":ob})


def addbook(request):
    ob=category_table.objects.all()
    return render(request, "user/AddBook.html",{"val":ob})


def DeleteBook(request,id):

    ob1=book_table.objects.get(id=id)
    ob1.delete()
    return redirect("/sellerhome")


def UpdateBook(request,id):
    ob=category_table.objects.all()
    request.session['bid']=id
    ob1=book_table.objects.get(id=id)
    return render(request, "user/UpdateBook.html",{"val":ob,"i":ob1})


def add_book(request):
    name=request.POST['title']
    author= request.POST['author']
    condition=request.POST['condition']
    image=request.FILES['image']
    fs=FileSystemStorage()
    fn=fs.save(image.name,image)
    price=request.POST['price']
    genre= request.POST['genre']
    dis= request.POST['dis']
    cat=request.POST['cat']
    lan=request.POST['lang']

    ob=book_table()
    ob.category = category_table.objects.get(id=cat)
    ob.Tittle = name
    ob.Author = author
    ob.genre = genre
    ob.condition = condition
    ob.price = price
    ob.description = dis
    ob.user_id = user_table.objects.get(LOGIN__id=request.session['lid'])
    ob.photo = fn
    ob.status = "Available"
    ob.language=lan
    ob.save()

    return redirect('/sellerhome')

def update_book_post(request):
    name=request.POST['title']
    author= request.POST['author']
    condition=request.POST['condition']


    price=request.POST['price']
    genre= request.POST['genre']
    dis= request.POST['dis']
    cat=request.POST['cat']
    lan=request.POST['lang']
    status=request.POST['status']

    ob=book_table.objects.get(id=request.session['bid'])
    ob.category = category_table.objects.get(id=cat)
    ob.Tittle = name
    ob.Author = author
    ob.genre = genre
    ob.condition = condition
    ob.price = price
    ob.description = dis
    ob.user_id = user_table.objects.get(LOGIN__id=request.session['lid'])
    if 'image' in request:
        image = request.FILES['image']
        fs = FileSystemStorage()
        fn = fs.save(image.name, image)
        ob.photo = fn
    ob.status = status
    ob.language=lan
    ob.save()

    return redirect('/sellerhome')



def registration(request):
    return render(request, "registration/regindex.html")



def reg_code_user(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        pwrd = request.POST['pas']
        name = request.POST['name']
        place = request.POST['place']
        email = request.POST['email']
        phone = request.POST['phone']

        # Check if the username or email already exists
        if login_table.objects.filter(username=uname).exists():
            messages.error(request, "Username is already registered.")
            return redirect('/registration')

        if user_table.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('/registration')

        # If no errors, proceed with registration
        ob = login_table()
        ob.username = uname
        ob.password = pwrd
        ob.type = "user"
        ob.save()

        ob1 = user_table()
        ob1.name = name
        ob1.place = place
        ob1.phone = phone
        ob1.email = email

        # Handle file upload
        if 'file' in request.FILES:
            photo = request.FILES['file']
            fs = FileSystemStorage()
            fn = fs.save(photo.name, photo)
            ob1.photo = fn
        else:
            ob1.photo = "sample.jpg"

        ob1.LOGIN = ob
        ob1.save()

        # Success message
        messages.success(request, "Registration successful.")
        return redirect('/login')

    return render(request, 'registration.html')




