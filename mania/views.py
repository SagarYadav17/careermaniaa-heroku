import reverse_geocoder as rg
from django.db.models import Q
from datetime import datetime
from django.shortcuts import render, redirect
import os
import razorpay

from django.views.decorators.csrf import csrf_exempt

from mania.models import *
from merchant_app.models import *

from django.db import IntegrityError

from django.http import HttpResponse, JsonResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from mania.utils import generate_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.views import View

from django.contrib.auth.decorators import login_required

from dotenv import load_dotenv
load_dotenv()


def send_confirmation_email(request, user):
    current_site = get_current_site(request)

    message = render_to_string('confirmation/activate.html',
                               {
                                   'user': user,
                                   'domain': current_site.domain,
                                   'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                   'token': generate_token.make_token(user)
                               })

    email_message = EmailMessage(
        'Activate Your Account',
        message,
        os.environ['SENDGRID_FROM_EMAIL'],
        [user.email],
    )

    email_message.send(fail_silently=False)


def add_forms_mail(request, user):
    current_site = get_current_site(request)
    email_subject = 'Fill the Information'
    message = render_to_string('merchant/forms.html',
                               {
                                   'user': user,
                                   'domain': current_site.domain,
                               })

    email_message = EmailMessage(
        email_subject,
        message,
        os.environ['SENDGRID_FROM_EMAIL'],
        [user.email],
    )

    email_message.send()


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except:
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_verified = True
            user.save()
            messages.add_message(request, messages.INFO,
                                 'Account Activated Successfully.')
            if user.is_merchant:
                return redirect('merchant/login')
            return redirect('login_user')
        return render(request, 'confirmation/activate_failed.html', status=401)


def index(request):
    try:
        city = request.session['loc']
    except:
        city = None
    if request.method == "POST" and city == None:
        lat = request.POST.get("lati", "21.1458")
        lng = request.POST.get("lngi", "79.0882")
        coordinates = lat, lng
        city = reverseGeocode(coordinates)
        request.session['loc'] = city
    courses = Course.objects.all()
    science_courses = Course.objects.filter(stream="Science")
    context = {'courses': courses,
               'science_courses': science_courses, 'loc': city}
    return render(request, 'user/index.html', context)


def user_profile(request):
    return render(request, 'user/profile.html')


def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.create_student(email, username, password)
            user.save()

            send_confirmation_email(request, user)

            return redirect('index')

        except IntegrityError as e:
            if str(e) == 'UNIQUE constraint failed: mania_user.username':
                messages.info(request, 'username is already taken')
            if str(e) == 'UNIQUE constraint failed: mania_user.email':
                messages.info(request, 'email is already taken')
            else:
                messages.info(request, 'Something went wrong')

    return render(request, 'user/sign-up.html')


def login_user(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)

        if user:
            if user.is_student and user.is_verified:
                login(request, user)
                return redirect('index')

            elif user.is_verified != True:
                return render(request, 'user/login.html', {'error': 'Account not verified yet. Please check your e-mail'})
        if user is None:
            return render(request, 'user/login.html', {'error': 'Your email and password didn\'t match. Please try again.'})

        else:
            return render(request, 'user/login.html', {'error': 'Account doesn\'t found. Try signup'})

    return render(request, 'user/login.html')


@login_required(login_url='merchant/login')
def logout_user(request):
    logout(request)
    return redirect('login_user')


def reverifyAccount(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            if not user.is_verified:
                send_confirmation_email(request, user)
                return JsonResponse({'message': 'Check your mail'})
            if user.is_verified:
                return JsonResponse({'message': 'Account is already verified'})
        except:
            redirect('reverify')

    return render(request, 'confirmation/reverify.html')


def reverseGeocode(coordinates):
    result = rg.search(coordinates)
    city = result[0]["name"]
    return city


def products(request):
    if request.method == "POST":
        lat = request.POST.get("lat", "21.1458")
        lng = request.POST.get("lng", "79.0882")
        coordinates = lat, lng
        city = reverseGeocode(coordinates)
        courses = list(Course.objects.all())
        courses = [course for course in courses if Address.objects.get(
            user=course.coaching.merchant).city == city]
        if courses == []:
            context = {'msg': 'No Near By Coachings'}
        else:
            context = {'courses': courses, 'msg': 'Near You'}
        return render(request, 'user/products.html', context)
    courses = Course.objects.all()
    context = {'courses': courses, 'msg': 'All Courses'}
    return render(request, 'user/products.html', context)


def filters(request):
    if request.method == "POST":
        science = request.POST.get('science', None)
        arts = request.POST.get('arts', None)
        commerce = request.POST.get('commerce', None)
        music = request.POST.get('music', None)
        dance = request.POST.get('dance', None)
        sports = request.POST.get('sports', None)
        Streams = [science, arts, commerce, music, dance, sports]
        Streams = [stream for stream in Streams if stream != None]
        courses = Course.objects.all()
        result = []
        for course in courses:
            if course.stream in Streams:
                result.append(course)
        context = {'courses': result, 'msg': 'Based On Filters'}
        return render(request, 'user/products.html', context)
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'user/products.html', context)


def science_coachings(request):
    courses = Course.objects.filter(stream="Science")
    context = {'courses': courses, 'msg': 'Science Coachings'}
    return render(request, 'user/products.html', context)


def commerce_coachings(request):
    courses = Course.objects.filter(stream="Commerce")
    context = {'courses': courses, 'msg': 'Science Coachings'}
    return render(request, 'user/products.html', context)


def other_coachings(request):
    courses = list(Course.objects.all())
    courses = [course for course in courses if course.stream !=
               "Science" and course.stream != "Commerce"]
    context = {'courses': courses, 'msg': 'Other Coachings'}
    return render(request, 'user/products.html', context)


def add_to_cart(request, id):
    if request.user in list(User.objects.all()):
        course = Course.objects.get(id=id)
        user = request.user
        cart = Cart(user=user, course=course)
        cart.save()
        return redirect('cart')
    else:
        courses = request.COOKIES
        i = str(len(courses) + 2)
        cookiee_name = "course" + i
        cookiee_name = str(cookiee_name)
        for item in courses.items():
            if id == item[1]:
                return redirect("cart")
        res = HttpResponse("Item Added to cart. Go to Cart to checkout")
        res.set_cookie(cookiee_name, id)
        return res
    return HttpResponse("Some Error Occured")


def cart(request):
    if request.user in list(User.objects.all()):
        try:
            carts = Cart.objects.filter(user=request.user)
        except:
            carts = None
        loggedIn = True
    else:
        courses = request.COOKIES
        carts = []
        for item in courses.items():
            if len(item[1]) > 2:
                continue
            else:
                carts.append(Course.objects.get(id=item[1]))
        loggedIn = False
    if carts == None:
        msg = "Your Cart is Empty."
    else:
        msg = ""
    context = {"courses": carts, "msg": msg, 'loggedIn': loggedIn}
    return render(request, "user/cart.html", context)


def delete_cartitem(request, id):
    if request.user in list(User.objects.all()):
        cart = Cart.objects.get(id=id)
        cart.delete()
    else:
        courses = request.COOKIES
        for item in courses.items():
            if item[1] == id:
                cookie_name = item[0]
                break
        res = HttpResponse("Item Deleted From your Cart.")
        res.delete_cookie(cookie_name)
        return res
    return redirect('cart')


def wishlist(request):
    if request.user in User.objects.all():
        try:
            wishlists = Wishlist.objects.filter(user=request.user)
        except:
            wishlists = None
        if wishlists == None:
            msg = "Your Wishlist is Empty."
        else:
            msg = ""
        context = {"courses": wishlists, "msg": msg}
        return render(request, "user/wishlist.html", context)
    else:
        return redirect('login_user')


@login_required(login_url='user/login')
def add_to_wishlist(request, id):
    if request.user in list(User.objects.all()):
        course = Course.objects.get(id=id)
        user = request.user
        wishlist = Wishlist(user=user, course=course)
        wishlist.save()
        return redirect("wishlist")


def delete_wishlistitem(request, id):
    if request.user in list(User.objects.all()):
        wishlist = Wishlist.objects.get(id=id)
        wishlist.delete()
        return redirect('wishlist')
    else:
        return redirect('login_user')


def about(request):
    return render(request, 'user/about.html')


def search(request):
    if request.method == "POST":
        try:
            city = request.POST['city']
        except:
            city = None
        keyword = request.POST['keyword']
        if keyword == "":
            return render(request, 'user/search.html', {'length': 0})
        courses = []
        courses += Course.objects.filter(Q(name__icontains=keyword)
                                         | Q(description__icontains=keyword))
        if city:
            courses = [course for course in courses if Address.objects.get(
                user=course.coaching.merchant).city == city]
        return render(request, 'user/search.html', {'courses': courses, 'keyword': keyword})
    courses = Course.objects.all()
    return render(request, 'user/search.html', {'courses': courses})


def payment(request, id):
    if request.user in User.objects.all():
        user = request.user
        course = Course.objects.get(id=id)
        fees = str(course.fees)
        amount = int(fees)
        registration = Registration(user=user, course=course, fees=str(fees))
        registration.save()
        client = razorpay.Client(
            auth=(os.getenv('razorpaykey'), os.getenv('razorpaysecret')))
        response = client.order.create(
            {'amount': amount, 'currency': 'INR', 'payment_capture': 1})
        print(response)
        context = {'response': response}
        return render(request, "user/payment.html", context)


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        print(request.POST)
        return HttpResponse("Done payment hurrey!")


def bookings(request):
    if request.user in User.objects.all():
        courses = Registration.objects.filter(user=request.user)
        context = {'courses': courses}
        return render(request, 'user/bookings.html', context)
    return redirect('login_user')


def product(request, id):
    try:
        course = Course.objects.get(id=id)
    except:
        course = None
        return redirect('index')
    context = {'course': course}
    return render(request, 'user/product.html', context)


def jobs(request):
    context = {
        'jobs': Job.objects.all()
    }
    return render(request, 'user/jobs.html', context)


def job(request, id):
    context = {
        'job': Job.objects.get(id=id)
    }
    return render(request, 'user/job.html', context)


def job_apply(request, id):
    try:
        JobApplications.objects.create(
            applicant=request.user, job_appication=Job.objects.get(id=id)).save()
    except:
        pass
    return redirect('jobs')
