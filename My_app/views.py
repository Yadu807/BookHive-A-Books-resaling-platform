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
from .models import login_table, user_table  # Import your models
from django.shortcuts import render, get_object_or_404
from .models import book_table
from django.db.models import Q
from django.db.models import F
from django.db.models.functions import Abs


from django.http import JsonResponse



# Create your views here.
from My_app.models import *


def home(request):
    return render(request,"index.html")


def login(request):
    return render(request,"loginindex.html")


def terms(request):
    return render(request,"registration/terms.html")


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
    ob1 = category_table.objects.all()
    ob=book_table.objects.exclude(user_id__LOGIN__id=request.session['lid'])
    for i in ob:
        ob1=favorites_table.objects.filter(user__LOGIN__id=request.session['lid'],book__id=i.id)
        if len(ob1)>0:
            i.s=True
        else:
            i.s=False

    return render(request, "user/userindex.html",{"val":ob,"c":ob1})

from django.db.models import Q, Case, When, Value, IntegerField

def userhomesearch(request):
    s = request.POST['s'].strip()  # Remove leading/trailing spaces
    cat = request.POST['cat']
    ob1 = category_table.objects.all()

    # Build the base query to exclude the current user's books
    base_query = book_table.objects.exclude(user_id__LOGIN__id=request.session['lid'])

    # If a category is selected other than "All"
    if cat != "0":
        base_query = base_query.filter(category__id=cat)

    # If the search term is empty, return all books in the selected category
    if not s:
        ob = base_query  # No search filters applied
        return render(request, "user/userindex.html", {"val": ob, "c": ob1, "cat": cat, "s": s})

    # Create a base Q object for partial match fields (no character limit for Tittle, Author, etc.)
    search_filters = Q(
        Q(Tittle__icontains=s) |  # No character limit on title
        Q(Author__icontains=s) |
        Q(genre__icontains=s) |
        Q(language__icontains=s)
    )
    price_search = None  # Initialize price_search as None

    # Handle price search
    if s.isdigit():
        price_search = int(s)
        # Search for books priced approximately around the entered value (e.g., ±25%)
        min_price = price_search * 0.75  # 25% lower than the search value
        max_price = price_search * 1.25  # 25% higher than the search value
        search_filters |= Q(price__gte=min_price, price__lte=max_price)
    elif 'under' in s.lower():  # Handle "under X" queries
        try:
            price_limit = int(s.split()[-1])  # Extract the number from the query
            search_filters |= Q(price__lt=price_limit)
        except ValueError:
            pass  # Ignore if it's not a valid number after 'under'

    # Add case-insensitive exact match for condition and status
    search_filters |= Q(condition__iexact=s) | Q(status__iexact=s)

    # Add description search only if the search string is 4 or more characters
    if len(s) >= 4:
        search_filters |= Q(description__icontains=s)

    # Filter the queryset based on the search filters
    ob = base_query.filter(search_filters)

    # Define the relevance conditions
    relevance_conditions = [
        When(Tittle__iexact=s, then=Value(4)),  # Exact match in title ranks highest
        When(Author__iexact=s, then=Value(3)),  # Exact match in author ranks second
        When(condition__iexact=s, then=Value(2)),  # Exact match in condition
        When(status__iexact=s, then=Value(2)),  # Exact match in status
        When(genre__iexact=s, then=Value(1)),  # Exact match in genre
    ]

    # Add price relevance condition only if price_search is defined
    if price_search is not None:
        relevance_conditions.append(When(price__exact=price_search, then=Value(3)))

        # Add price relevance condition only if price_search is defined
        if price_search is not None:
            # Rank books by how close the price is to the searched value
            ob = ob.annotate(price_proximity=Abs(F('price') - price_search))

            # Add condition to give high relevance to exact price match
            relevance_conditions.append(When(price__exact=price_search, then=Value(4)))

            # Now rank the books based on the proximity of the price
            ob = ob.order_by('price_proximity')  # Closest price first

    # Rank by relevance (Exact matches in Tittle, Author, Price, etc.)
    ob = ob.annotate(
        relevance=Case(
            *relevance_conditions,  # Unpack the list of conditions
            default=Value(1),  # Other matches rank lower
            output_field=IntegerField(),
        )
    ).order_by('-relevance')  # Order by relevance, highest first
    for i in ob:
        ob1=favorites_table.objects.filter(user__LOGIN__id=request.session['lid'],book__id=i.id)
        if len(ob1)>0:
            i.s=True
        else:
            i.s=False
    return render(request, "user/userindex.html", {"val": ob, "c": ob1, "cat": cat, "s": s})


def sellerhome(request):
    ob1=category_table.objects.all()
    ob = book_table.objects.filter(user_id__LOGIN__id=request.session['lid'])
    return render(request, "user/sellerindex.html",{"val":ob,"c":ob1})

from django.http import JsonResponse
from django.db.models import Q, Case, When, Value, IntegerField

def sellerSearch(request):
    # Initialize search term and category from the request
    s = request.POST.get('s', '').strip()  # Remove leading/trailing spaces
    cat = request.POST.get('cat', '0')  # Default to "0" if not present
    ob1 = category_table.objects.all()

    # Build the base query to include only the current user's books
    base_query = book_table.objects.filter(user_id__LOGIN__id=request.session['lid'])

    # If a category is selected other than "All"
    if cat != "0":
        base_query = base_query.filter(category__id=cat)

    # If the search term is empty, return all books in the selected category
    if not s:
        ob = base_query  # No search filters applied
        return render(request, "user/sellerindex.html", {"val": ob, "c": ob1, "cat": cat, "s": s})

    # Create a base Q object for partial match fields (no character limit for Title, etc.)
    search_filters = Q(
        Q(Tittle__icontains=s) |  # Partial match on title
        Q(Author__icontains=s) |
        Q(genre__icontains=s) |
        Q(language__icontains=s)
    )

    # Handle price search
    if s.isdigit():
        price_search = int(s)
        # Search for books priced approximately around the entered value (e.g., ±25%)
        min_price = price_search * 0.75  # 25% lower than the search value
        max_price = price_search * 1.25  # 25% higher than the search value
        search_filters |= Q(price__gte=min_price, price__lte=max_price)
    elif 'under' in s.lower():  # Handle "under X" queries
        try:
            price_limit = int(s.split()[-1])  # Extract the number from the query
            search_filters |= Q(price__lt=price_limit)
        except ValueError:
            pass  # Ignore if it's not a valid number after 'under'

    # Add case-insensitive exact match for condition and status
    search_filters |= Q(condition__iexact=s) | Q(status__iexact=s)

    # Add description search only if the search string is 4 or more characters
    if len(s) >= 4:
        search_filters |= Q(description__icontains=s)

    # Filter the queryset based on the search filters
    ob = base_query.filter(search_filters)

    # Rank by relevance (Exact matches in Title or Author rank higher)
    ob = ob.annotate(
        relevance=Case(
            When(Tittle__iexact=s, then=Value(3)),  # Exact match in title ranks highest
            When(Author__iexact=s, then=Value(2)),  # Exact match in author ranks second
            default=Value(1),                       # Other matches rank lower
            output_field=IntegerField(),
        )
    ).order_by('-relevance')  # Order by relevance, highest first



    # Otherwise, render the full template
    return render(request, "user/sellerindex.html", {"val": ob, "c": ob1, "cat": cat, "s": s})


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

        # Check if the username or email already exists during form submission
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

    # Handle AJAX requests for email and username validation
    if request.method == 'GET':
        uname = request.GET.get('uname', None)
        email = request.GET.get('email', None)

        # Check if the username already exists
        if uname:
            is_taken = login_table.objects.filter(username=uname).exists()
            return JsonResponse({'is_taken': is_taken, 'error_message': "Username is already registered." if is_taken else ""})

        # Check if the email already exists
        if email:
            is_taken = user_table.objects.filter(email=email).exists()
            return JsonResponse({'is_taken': is_taken, 'error_message': "Email is already registered." if is_taken else ""})

    return render(request, 'registration/regindex.html')


def book_detail(request, book_id):
    request.session['book_id']=book_id
    return redirect("/book_detail1")


def book_detail1(request):
    book_id=request.session['book_id']
    book = book_table.objects.get(id=book_id)
    return render(request, 'user/BookViewSell.html', {'book': book})


def book_detail2(request, book_id):
    request.session['book_id']=book_id
    return redirect("/book_detail3")


def book_detail3(request):
    book_id = request.session['book_id']
    book = book_table.objects.get(id=book_id)

    # Fetch related books from the same category (excluding the current book)
    related_books = book_table.objects.filter(category=book.category).exclude(id=book_id).exclude(user_id__LOGIN__id=request.session['lid'])[:6]

    return render(request, 'user/BookViewBuy.html', {'book': book, 'related_books': related_books})


def checkemail(request):
    email=request.GET['email']

    ob=user_table.objects.filter(email=email)
    if len(ob)>0:
        return JsonResponse({"is_taken":True,"error_message":"Email existing"})
    else:
        return JsonResponse({"is_taken": False, "error_message": ""})


def checkuname(request):
    uname=request.GET['uname']

    ob=login_table.objects.filter(username=uname)
    if len(ob)>0:
        return JsonResponse({"is_taken":True,"error_message":"Username existing"})
    else:
        return JsonResponse({"is_taken": False, "error_message": ""})

def addfav(request):
    bid=request.GET['bid']
    ob=favorites_table.objects.filter(user__LOGIN__id=request.session['lid'],book__id=bid)
    if len(ob)==0:
        ob = favorites_table()
        ob.user=user_table.objects.get(LOGIN__id=request.session['lid'])
        ob.book=book_table.objects.get(id=bid)
        ob.save()
    else:
        ob[0].delete()

    return JsonResponse({"task": True})


# def owner_chat_to_user(request, id):



def owner_chat_to_user(request, id):
    request.session["userid"] = id
    cid = str(request.session["userid"])
    request.session["new"] = cid
    qry = user_table.objects.get(LOGIN__id=cid)
    print(qry,'login----------')

    return render(request, "user/Chat.html", {'photo': qry.photo.url, 'name': qry.name, 'toid': cid})


def chat_view(request):
    fromid = request.session["lid"]
    toid = request.session["userid"]


    qry = user_table.objects.get(LOGIN_id=request.session["userid"])
    from django.db.models import Q

    res = Chat.objects.filter(Q(FROMID_id=fromid, TOID_id=toid) | Q(FROMID_id=toid, TOID_id=fromid)).order_by("id")
    l = []
    print(qry.name,'userssssssssss')

    for i in res:
        l.append({"id": i.id, "message": i.message, "to": i.TOID_id, "date": i.date, "from": i.FROMID_id,"ct":i.ctype})
        if int(i.TOID_id) ==int(request.session["lid"]):
            ob=Chat.objects.get(id=i.id)
            ob.status='viewed'
            ob.save()


    return JsonResponse({'photo': qry.photo.url, "data": l, 'name': qry.name, 'toid': request.session["userid"]})


def chat_send(request, msg):
    lid = request.session["lid"]
    toid = request.session["userid"]
    message = msg

    import datetime
    d = datetime.datetime.now().date()
    chatobt = Chat()
    chatobt.message = message
    chatobt.TOID_id = toid
    chatobt.FROMID_id = lid
    chatobt.date = d
    chatobt.ctype="text"
    chatobt.status="pending"
    chatobt.save()

    return JsonResponse({"status": "ok"})


def upload_image(request):
    lid = request.session["lid"]
    toid = request.session["userid"]
    print("********++++++++++++++++")
    print(request.FILES)
    fs=FileSystemStorage()
    img=request.FILES['image']
    fn=fs.save(img.name,img)
    message = "/media/"+fn

    import datetime
    d = datetime.datetime.now().date()
    chatobt = Chat()
    chatobt.message = message
    chatobt.TOID_id = toid
    chatobt.FROMID_id = lid
    chatobt.date = d
    chatobt.ctype="image"
    chatobt.status="pending"
    chatobt.save()

    return JsonResponse({"status": "ok"})

def coun_msg(request,id):

    request.session["userid"]=id

    return JsonResponse({"status": "ok"})


def home_chat(request):


    return render(request,"user/fur_chat.html")



def chatview(request):
    lids=[]
    ob = Chat.objects.filter(FROMID__id=request.session['lid'])
    for i in ob:
        lids.append(i.TOID.id)
    ob1 = Chat.objects.filter(TOID__id=request.session['lid'])
    for i in ob1:
        lids.append(i.FROMID.id)
    d=[]
    ob=user_table.objects.filter(LOGIN__id__in=lids)
    for i in ob:
        r={"name":i.name,'photo':i.photo.url,'email':i.email,'loginid':i.LOGIN.id}
        pm=""
        obb=Chat.objects.filter(TOID__id=request.session['lid'],FROMID__id=i.LOGIN.id,status='pending')
        if len(obb)>0:
            pm="("+str(len(obb))+")"
        r['pm']=pm
        d.append(r)
    return JsonResponse(d, safe=False)

def favorites_view(request):
    favorite_books = favorites_table.objects.filter(user__LOGIN_id=request.session['lid'])  # Adjust as needed for your user model
    return render(request, 'user/view_favorite.html', {'favorite_books': favorite_books})


def fav_view(request):
    favorite_books = favorites_table.objects.filter(user__LOGIN_id=request.session['lid'])  # Adjust as needed for your user model
    return render(request, 'user/favourites.html', {'favorite_books': favorite_books})