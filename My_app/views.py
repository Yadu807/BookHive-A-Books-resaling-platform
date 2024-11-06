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
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache

import datetime
from django.db.models import Avg



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
        # Clear any existing messages by iterating over them
        storage = messages.get_messages(request)
        storage.used = True

        username = request.POST.get('mail')
        pwd = request.POST.get('Password')

        # Check if the user exists with the provided username and password
        ob = login_table.objects.filter(username=username, password=pwd)
        if ob.exists():
            ob1 = ob.first()

            # Check if the user is blocked
            try:
                block_status = ob1.blockstatus
                if block_status.status == "Blocked":
                    messages.error(request, "Your account is blocked.")
                    return render(request, 'loginindex.html')  # Redirect back to login page with message
            except BlockStatus.DoesNotExist:
                # If BlockStatus record does not exist, assume the user is active
                pass

            # If the user is not blocked, proceed to check their role and redirect accordingly
            request.session['lid'] = ob1.id
            if ob1.type == 'admin':
                return HttpResponse('''<script>window.location='/adminhome'</script>''')
            elif ob1.type == 'user':
                return HttpResponse('''<script>window.location='userhome'</script>''')
            else:
                return HttpResponse('''<script>window.location='/'</script>''')
        else:
            # Display error messages based on existence of the username
            if not login_table.objects.filter(username=username).exists():
                messages.error(request, "Username does not exist.")
            else:
                messages.error(request, "Incorrect password.")
            return render(request, 'loginindex.html')  # Redirect to login page with error message

    return render(request, 'loginindex.html')


def adminhome(request):
    ob=user_table.objects.all()
    ob1 = book_table.objects.all()
    ob3 = book_table.objects.filter(status='Available')
    ob2 = Order.objects.filter(Status='paid')
    # ob2=[]

    return render(request, "admin/adminindex.html",{"tu":len(ob),"tu1":len(ob1),"tu2":len(ob3),"tu3":len(ob2)})


def userhome(request):
    ob2 = category_table.objects.all()
    ob=book_table.objects.exclude(user_id__LOGIN__id=request.session['lid'])
    for i in ob:
        ob1=favorites_table.objects.filter(user__LOGIN__id=request.session['lid'],book__id=i.id)
        if len(ob1)>0:
            i.s=True
        else:
            i.s=False

    return render(request, "user/userindex.html",{"val":ob,"c":ob2})

from django.db.models import Q, Case, When, Value, IntegerField

def userhomesearch(request):
    s = request.POST.get('s', '').strip()
    cat = request.POST.get('cat', '0')
    ob1 = category_table.objects.all()  # Fetch categories correctly

    # Store search keyword if not empty
    if s:
        SearchKeyword.objects.create(user=user_table.objects.get(LOGIN__id=request.session['lid']), keyword=s)

    base_query = book_table.objects.exclude(user_id__LOGIN__id=request.session['lid'])

    # Filter by category if selected
    if cat != "0":
        base_query = base_query.filter(category__id=cat)

    # If search term is empty, return all books in selected category
    if not s:
        ob = base_query
        return render(request, "user/userindex.html", {"val": ob, "c": ob1, "cat": cat, "s": s})

    # Apply search filters
    search_filters = Q(
        Q(Tittle__icontains=s) |
        Q(Author__icontains=s) |
        Q(genre__icontains=s) |
        Q(language__icontains=s)
    )

    # Handle price-related search filters
    if s.isdigit():
        price_search = int(s)
        min_price = price_search * 0.75
        max_price = price_search * 1.25
        search_filters |= Q(price__gte=min_price, price__lte=max_price)
    elif 'under' in s.lower():
        try:
            price_limit = int(s.split()[-1])
            search_filters |= Q(price__lt=price_limit)
        except ValueError:
            pass

    # Match by condition and status
    search_filters |= Q(condition__iexact=s) | Q(status__iexact=s)

    # Add description filter if search string is 4+ characters
    if len(s) >= 4:
        search_filters |= Q(description__icontains=s)

    ob = base_query.filter(search_filters)

    # Apply relevance ranking
    relevance_conditions = [
        When(Tittle__iexact=s, then=Value(4)),
        When(Author__iexact=s, then=Value(3)),
        When(condition__iexact=s, then=Value(2)),
        When(status__iexact=s, then=Value(2)),
        When(genre__iexact=s, then=Value(1)),
    ]

    # Add price relevance if applicable
    if s.isdigit():
        relevance_conditions.append(When(price__exact=price_search, then=Value(4)))
        ob = ob.annotate(price_proximity=Abs(F('price') - price_search)).order_by('price_proximity')

    ob = ob.annotate(
        relevance=Case(
            *relevance_conditions,
            default=Value(1),
            output_field=IntegerField(),
        )
    ).order_by('-relevance')

    # Update book's favorite status for the user
    for book in ob:
        favorite = favorites_table.objects.filter(user__LOGIN__id=request.session['lid'], book__id=book.id)
        book.s = len(favorite) > 0

    return render(request, "user/userindex.html", {"val": ob, "c": ob1, "cat": cat, "s": s})



def sellerhome(request):
    ob1=category_table.objects.all()
    ob = book_table.objects.filter(user_id__LOGIN__id=request.session['lid'])

    obreq=Order.objects.filter(BookID__user_id__LOGIN__id=request.session['lid'],Status='Requested',NStatus='pending')
    request.session['ps']=""
    if len(obreq)>0:
        request.session['ps'] = "("+str(len(obreq))+")"
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
    ob1 = favorites_table.objects.filter(user__LOGIN__id=request.session['lid'], book__id=book_id)
    if len(ob1) > 0:
        book.s = True
    else:
        book.s = False
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




def profile_view(request):
    login_id = request.session.get('lid')
    if login_id:
        user_details = user_table.objects.get(LOGIN_id=login_id)
        # Retrieve all feedbacks given to the user
        feedbacks = Feedback.objects.filter(seller=user_details)
        # Calculate the average rating
        avg_rating = feedbacks.aggregate(Avg('rating'))['rating__avg'] or 0  # Default to 0 if no rating

        return render(request, 'user/profile.html', {
            'user_details': user_details,
            'feedbacks': feedbacks,
            'avg_rating': round(avg_rating, 1)  # Rounded to 1 decimal place
        })
    else:
        return redirect('login')


@csrf_exempt
def update_profile_view(request):
    if request.method == 'POST':
        login_id = request.session.get('lid')
        if login_id:
            user_details = get_object_or_404(user_table, LOGIN_id=login_id)
            user_details.name = request.POST['name']
            user_details.place = request.POST['place']
            user_details.phone = request.POST['phone']
            user_details.email = request.POST['email']

            # If a new photo is uploaded
            if 'photo' in request.FILES:
                user_details.photo = request.FILES['photo']

            # # Password update
            # if request.POST.get('password'):
            #     user_details.LOGIN.password = make_password(request.POST['password'])  # Hash before saving

            # Username update
            user_details.LOGIN.username = request.POST['username']

            user_details.save()  # Save the updated user details
            user_details.LOGIN.save()  # Save the updated login details

            response_data = {
                'success': True,
                'name': user_details.name,
                'username': user_details.LOGIN.username,
                'place': user_details.place,
                'phone': user_details.phone,
                'email': user_details.email,
                'photo_url': user_details.photo.url if user_details.photo else None,
            }
            return JsonResponse(response_data)
        return JsonResponse({'success': False})
    return JsonResponse({'success': False})



def get_previous_keywords(request):
    keywords = SearchKeyword.objects.filter(user=user_table.objects.get(LOGIN__id=request.session['lid'])).order_by('-created_at')[:5].values_list('keyword', flat=True)
    return JsonResponse({'keywords': list(keywords)})

@never_cache
def logout_view(request):
    logout(request)
    return redirect('home')

def buynow(request):
    amt=request.POST['amt']
    bob=book_table.objects.get(id=request.session['book_id'])

    ob=Order()
    ob.BookID = bob
    ob.BuyerID = user_table.objects.get(LOGIN__id=request.session['lid'])
    ob.OrderDate=datetime.datetime.now().date()
    ob.Amount = amt
    ob.save()

    return redirect("/Request")



def request_view(request):
    ob=Order.objects.filter(BuyerID__LOGIN__id=request.session['lid'])
    print(ob)
    return render(request,"user/Request.html",{"val":ob})


import  razorpay

def user_pay_proceed(request,id,amt):
    request.session['rid'] = id
    request.session['pay_amount'] = amt
    client = razorpay.Client(auth=("rzp_test_edrzdb8Gbx5U5M", "XgwjnFvJQNG6cS7Q13aHKDJj"))
    print(client)
    payment = client.order.create({'amount': str(amt)+"00", 'currency': "INR", 'payment_capture': '1'})
    res=user_table.objects.get(LOGIN__id=request.session['lid'])


    ob=Order.objects.get(id=request.session['rid'])
    ob.Status='paid'
    ob.save()
    return render(request,'user/UserPayProceed.html',{'p':payment,'val':res,"lid":request.session['lid'],"id":request.session['rid']})


def on_payment_success(request):
    request.session['rid'] = request.GET['id']
    request.session['lid'] = request.GET['lid']
    # var = auth.authenticate(username='admin', password='admin')
    # if var is not None:
    #     auth.login(request, var)
    # amt = request.session['pay_amount']
    ob = Order.objects.get(id=request.session['rid'])
    ob.Status = 'paid'
    ob.save()


    return HttpResponse('''<script>window.location="/Request"</script>''')


def seller_request_view(request):
    # Fetch books where the logged-in user is the seller
    seller_books = book_table.objects.filter(user_id__LOGIN__id=request.session['lid'])
    # Fetch orders for those books
    sbids=[]
    for i in seller_books:
        sbids.append(i.id)
    orders = Order.objects.filter(BookID__in=sbids)

    return render(request, 'user/sellRequest.html', {'orders': orders})



def accept_request(request, id):
     order=Order.objects.get(id=id)  # Ensure seller is correct
     order.Status = 'Available'
     order.save()
     return redirect('seller_request_view')

def reject_request(request, id):
    order = Order.objects.get(id=id)
    order.Status = 'Rejected'
    order.save()
    return redirect('seller_request_view')

def shipped_request(request, id):
    order = Order.objects.get(id=id)
    order.Status = 'Shipped'
    order.save()
    return redirect('seller_request_view')


def request_view_cancel(request,id):
    order = Order.objects.get(id=id)
    order.delete()
    return redirect('request_view')

def request_view_remove(request,id):
    order = Order.objects.get(id=id)
    order.delete()
    return redirect('request_view')

def request_view_recieved(request,id):
    order = Order.objects.get(id=id)
    order.Status = 'Recieved'
    order.delete()
    return redirect('request_view')

def provide_feedback(request,id):
    request.session['sid']=id
    return render(request, 'user/give_feedback.html')

def sendfeedbackpost(request):
    feed=request.POST['comment']
    rating=request.POST['rating']
    print(rating,"rating")
    ob= Feedback()
    ob.seller=user_table.objects.get(id=request.session['sid'])
    ob.user=user_table.objects.get(LOGIN__id=request.session['lid'])
    ob.rating=float(rating)
    ob.feedback=feed
    ob.save()

    return redirect('/userhome')

def view_profile(request, user_id):
    user_profile = get_object_or_404(user_table, pk=user_id)
    feedbacks = Feedback.objects.filter(seller=user_profile)
    avg_rating = feedbacks.aggregate(Avg('rating'))['rating__avg'] or 0
    return render(request, 'user/profileview.html', {
        'user_details': user_profile,
        'feedbacks': feedbacks,
        'avg_rating': round(avg_rating, 1)
    })

def manage_users(request):
    users = user_table.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        user = user_table.objects.get(id=user_id)
        block_status, created = BlockStatus.objects.get_or_create(LOGIN=user.LOGIN)

        if action == 'block':
            block_status.status = "Blocked"
        elif action == 'unblock':
            block_status.status = "Active"

        block_status.save()
        return redirect('manage-users')  # Redirect to refresh the page

    return render(request, 'admin/manage-users.html', {'users': users})


def admin_book_management(request):
    books = book_table.objects.select_related('user_id__LOGIN').all()  # Include related user and login info

    # Calculate average rating for each user
    for book in books:
        feedback_ratings = Feedback.objects.filter(seller=book.user_id)
        book.user_id.avg_rating = feedback_ratings.aggregate(Avg('rating'))['rating__avg'] or 0

    return render(request, 'admin/admin_book_management.html', {'books': books})

def delete_book(request, book_id):
    book = get_object_or_404(book_table, id=book_id)
    book.delete()
    return redirect('admin_book_management')


def manage_categories(request):
    # Fetch all categories
    categories = category_table.objects.all()

    # Handle adding a new category
    if request.method == 'POST' and 'add_category' in request.POST:
        category_name = request.POST.get('category')
        description = request.POST.get('description')
        if category_name and description:
            new_category = category_table(category=category_name, description=description)
            new_category.save()
            messages.success(request, "Category added successfully!")
            return redirect('manage_categories')

    # Handle editing an existing category
    if request.method == 'POST' and 'edit_category' in request.POST:
        category_id = request.POST.get('category_id')
        category_name = request.POST.get('category')
        description = request.POST.get('description')
        category_instance = get_object_or_404(category_table, id=category_id)
        category_instance.category = category_name
        category_instance.description = description
        category_instance.save()
        messages.success(request, "Category updated successfully!")
        return redirect('manage_categories')

    # Handle deleting a category
    if request.method == 'POST' and 'delete_category' in request.POST:
        category_id = request.POST.get('category_id')
        category_instance = get_object_or_404(category_table, id=category_id)
        category_instance.delete()
        messages.success(request, "Category deleted successfully!")
        return redirect('manage_categories')

    return render(request, 'admin/manage_categories.html', {'categories': categories})


def report_book(request, book_id):
    if request.method == 'POST':
        # Get complaint text from the form submission
        complaint_text = request.POST.get('complaint_text')
        book = get_object_or_404(book_table, id=book_id)

        # Check if 'lid' exists in the session to identify the logged-in user
        if 'lid' in request.session:
            try:
                # Fetch the user based on the login ID stored in the session
                user = user_table.objects.get(LOGIN__id=request.session['lid'])

                # Save the report
                Report.objects.create(book=book, user=user, complaint_text=complaint_text)
                # messages.success(request, 'Your complaint has been submitted.')
                return redirect('book_detail2', book_id=book_id)

            except user_table.DoesNotExist:
                # messages.error(request, "User not found. Please log in again.")
                return redirect('login')  # Redirect to login if user lookup fails
        else:
            # messages.error(request, "Session expired. Please log in again.")
            return redirect('login')  # Redirect to login if 'lid' is not in session

    return redirect('book_detail2', book_id=book_id)  # Redirect if request method is not POST


def sales_statistics(request):
    if 'lid' in request.session:
        user_id = request.session['lid']
        total_books_sold = Order.objects.filter(BookID__user_id__LOGIN__id=user_id).count()
        total_sales_amount = Order.objects.filter(BookID__user_id__LOGIN__id=user_id).aggregate(Sum('Amount'))['Amount__sum'] or 0

        most_sold_books = Order.objects.filter(BookID__user_id__LOGIN__id=user_id).values('BookID__title').annotate(total_sales=Count('id')).order_by('-total_sales')[:1]
        most_sold_book = most_sold_books[0] if most_sold_books else None

        context = {
            'total_books_sold': total_books_sold,
            'total_sales_amount': total_sales_amount,
            'most_sold_book': most_sold_book,
        }
        return render(request, 'user/sellerindex.html', context)
    else:
        return redirect('login')




def admin_view_reports(request):
    reports = Report.objects.select_related('book', 'user').all()
    context = {'reports': reports}
    return render(request, 'admin/admin_reports.html', context)

def delete_book(request, book_id):
    book = get_object_or_404(book_table, id=book_id)
    book.delete()
    return redirect('admin_view_reports')


def order_history(request):
    # Check if 'lid' is in session
    if 'lid' not in request.session:
        return redirect('/login/')  # Redirect to login if 'lid' is not in session

    # Retrieve the user from user_table using the session's 'lid'
    user_id = request.session['lid']
    user = user_table.objects.get(LOGIN_id=user_id)

    # Get orders where the user is the buyer
    buy_orders = Order.objects.filter(BuyerID=user).order_by('-OrderDate')

    # Get orders where the user is the seller (books they listed)
    sell_orders = Order.objects.filter(BookID__user_id=user).order_by('-OrderDate')

    context = {
        'buy_orders': buy_orders,
        'sell_orders': sell_orders,
    }
    return render(request, 'user/order_history.html', context)
