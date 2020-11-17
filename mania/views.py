# import reverse_geocoder as rg
from django.shortcuts import render, redirect

from mania.models import User
from merchant_app.models import Merchant_Details

from django.db import IntegrityError

from django.http import HttpResponse

from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from mania.utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.views import View
from datetime import *


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
        settings.EMAIL_HOST_USER,
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
        settings.EMAIL_HOST_USER,
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
                add_forms_mail(request, user)
                return redirect('login_merchant')
            return redirect('login_user')
        return render(request, 'confirmation/activate_failed.html', status=401)


def index(request):
    return render(request, 'user/index.html')


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
                messages.info(request, 'EmailID is already in use')
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
                return HttpResponse("Logged in as " + user.username)

            elif user.is_verified != True:
                return render(request, 'user/login.html', {'error': 'Account not verified yet. Please check your e-mail'})
        else:
            return render(request, 'user/login.html', {'error': 'Account Not Found'})

    return render(request, 'user/login.html')


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
        courses = Course.objects.all()
        result = []
        print(courses)
        for course in courses:
            address = Address.objects.get(branch=course.branch)
            if address.city == city:
                result.append(course)
        if result == []:
            context = {'msg': 'No Near By Coachings'}
        else:
            context = {'courses': result, 'msg': 'Near You'}
        return render(request, 'user/products.html', context)
    courses = Course.objects.all()
    context = {'courses': courses, 'msg': 'All Courses'}
    print(courses)
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
    print(courses)
    return render(request, 'user/products.html', context)


def science_coachings(request):
    merchants = list(Merchant_Details.objects.all())
    merchants = [
        merchant for merchant in merchants if merchant.stream == "Science"]
    coachings = [Coaching.objects.get(
        merchant=merchant.merchant) for merchant in merchants]
    courses = []
    for coaching in coachings:
        courses += Course.objects.filter(coaching=coaching)
    print(merchants)
    context = {'courses': courses, 'msg': 'Science Coachings'}
    return render(request, 'user/products.html', context)


def commerce_coachings(request):
    merchants = list(Merchant_Details.objects.all())
    merchants = [
        merchant for merchant in merchants if merchant.stream == "Commerce"]
    coachings = [Coaching.objects.get(
        merchant=merchant.merchant) for merchant in merchants]
    courses = []
    for coaching in coachings:
        courses += Course.objects.filter(coaching=coaching)
    print(merchants)
    context = {'courses': courses, 'msg': 'Commerce Coachings'}
    return render(request, 'user/products.html', context)


def other_coachings(request):
    merchants = list(Merchant_Details.objects.all())
    merchants = [merchant for merchant in merchants if merchant.stream !=
                 "Science" and merchant.stream != "Commerce"]
    coachings = [Coaching.objects.get(
        merchant=merchant.merchant) for merchant in merchants]
    courses = []
    for coaching in coachings:
        courses += Course.objects.filter(coaching=coaching)
    print(merchants)
    context = {'courses': courses, 'msg': 'Other Coachings'}
    return render(request, 'user/products.html', context)


def add_to_cart(request, id):
    if request.user in list(User.objects.all()):
        course = Course.objects.get(id=id)
        user = request.user
        cart = Cart(user=user, course=course)
        cart.save()
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

import json
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
        msg="Your Cart is Empty."
    else:
        msg = ""
    context = {"courses": carts, "msg":msg, 'loggedIn': loggedIn}
    print(context)
    return render(request, "user/cart.html", context)

def delete_cartitem(request, id):
    if request.user in list(User.objects.all()):
        cart = Cart.objects.get(id=id)
        cart.delete()
    else:
        print("In else")
        courses = request.COOKIES
        print(courses)
        for item in courses.items():
            if item[1] == id:
                cookie_name = item[0]
                break
        print(cookie_name)
        res = HttpResponse("Item Deleted From your Cart.")
        res.delete_cookie(cookie_name)
        return res
    return redirect('cart')

def wishlist(request):
    if request.user in list(User.objects.all()):
        try:
            wishlists = Wishlist.objects.filter(user=request.user)
        except:
            wishlists = None
        if wishlists == None:
            msg="Your Wishlist is Empty."
        else:
            msg = ""
        context = {"courses": wishlists, "msg":msg}
        return render(request, "user/wishlist.html", context)
    else:
        return redirect('login_user')
    


def add_to_wishlist(request, id):
    if request.user in list(User.objects.all()):
        course = Course.objects.get(id=id)
        user = request.user
        wishlist = Wishlist(user=user, course=course)
        wishlist.save()
        return HttpResponse("Item added to wishlist")

def delete_wishlistitem(request, id):
    if request.user in list(User.objects.all()):
        wishlist = Wishlist.objects.get(id=id)
        wishlist.delete()
        return redirect('cart')

def about(request):
    return render(request, 'user/about.html')