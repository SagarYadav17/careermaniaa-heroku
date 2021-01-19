from django.shortcuts import render, redirect
from mania.models import *
from merchant_app.models import Merchant_Details

from django.db import IntegrityError

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from mania.utils import generate_token
from django.core.mail import EmailMessage
from merchant_app.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.contrib import messages
from datetime import *

from urllib.parse import urlparse, urlunparse

from django.contrib.auth.forms import PasswordResetForm

from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from django.conf import settings


def merchant_view(request):
    faqs = FAQ.objects.all()
    context = {'faqs': faqs}
    return render(request, 'merchant/index.html', context)


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
        'sagaryadav.careermaniaa@gmail.com',
        [user.email],
    )

    email_message.send(fail_silently=False)


def register_merchant(request):
    if request.method == "POST":
        print(request.POST['register-type'])
        if request.POST['register-type'] == str('colleges'):
            try:
                user = User.objects.create_merchant(
                    email=request.POST['email'],
                    username=request.POST['username'],
                    password=request.POST['password'],
                    merchant_type=1
                )
                user.save()

                user_id = User.objects.get(email=request.POST['email'])
                college = College.objects.create(
                    user=user_id,
                    registration_no=request.POST['registeration-number'],
                    contact_no=request.POST['phone-number'],
                    college_name=request.POST['name'],
                    university_type=request.POST['uni-type'],
                    institute_type=request.POST['inst-type'],
                    chairman=request.POST['chairman'],
                    college_address=request.POST['address'],
                    country=request.POST['country'],
                    state=request.POST['state'],
                    city=request.POST['city']
                )
                college.save()
                send_confirmation_email(request, user)
                return redirect('merchant/login')

            except IntegrityError as e:
                if str(e) == 'UNIQUE constraint failed: mania_user.username':
                    messages.info(request, 'username is already taken')
                if str(e) == 'UNIQUE constraint failed: mania_user.email':
                    messages.info(request, 'EmailID is already in use')
                else:
                    messages.info(request, 'Something went wrong')

        if request.POST['register-type'] == str('classes'):
            try:
                user = User.objects.create_merchant(
                    email=request.POST['email'],
                    username=request.POST['username'],
                    password=request.POST['password'],
                    merchant_type=2
                )
                user.save()

                user_id = User.objects.get(email=request.POST['email'])
                logo = request.FILES['logo_img']
                coaching = Coaching.objects.create(
                    merchant=user_id,
                    name=request.POST['name'],
                    logo=logo,
                    registration_number=request.POST['registeration-number'],
                    country=request.POST['country'],
                    state=request.POST['state'],
                    address=request.POST['address'],
                    director_name=request.POST['chairman'],
                    phone_number=request.POST['phone-number']
                )

                coaching.save()
                owner_name = request.POST['chairman']
                owner_image = request.FILES['image']
                established = request.POST['established']
                mobile = request.POST['phone-number']
                owner = CoachingMetaData(owner_name=owner_name, owner_image=owner_image, mobile=mobile, established_on=established,
                                         coaching=coaching)
                owner.save()

                return redirect('merchant/login')

            except IntegrityError as e:
                if str(e) == 'UNIQUE constraint failed: mania_user.username':
                    messages.info(request, 'username is already taken')
                if str(e) == 'UNIQUE constraint failed: mania_user.email':
                    messages.info(request, 'EmailID is already in use')
                else:
                    messages.info(request, 'Something went wrong')

        if request.POST['register-type'] == str('jobs'):
            try:
                user = User.objects.create_merchant(
                    email=request.POST['email'],
                    username=request.POST['username'],
                    password=request.POST['password'],
                    merchant_type=3
                )
                user.save()
                send_confirmation_email(request, user)

                user_id = User.objects.get(email=request.POST['email'])
                job = JobRecruiter.objects.create(
                    user=user_id,
                    contact_no=request.POST['phone-number'],
                    company_address=request.POST['address'],
                    company_name=request.POST['name'],
                    registration_no=request.POST['registeration-number'],
                    country=request.POST['country'],
                    state=request.POST['state'],
                    city=request.POST['city'],
                    director_name=request.POST['chairman'],
                    industry_type=request.POST['industry-type']
                )
                job.save()

                return redirect('merchant/login')

            except IntegrityError as e:
                if str(e) == 'UNIQUE constraint failed: mania_user.username':
                    messages.info(request, 'username is already taken')
                if str(e) == 'UNIQUE constraint failed: mania_user.email':
                    messages.info(request, 'EmailID is already in use')
                else:
                    messages.info(request, 'Something went wrong')
    university_types = UniversityType.objects.all()
    class_types = ClassType.objects.all()
    industry_types = IndustryType.objects.all()
    institution_types = InstitutionType.objects.all()
    context = {'university_types': university_types, 'class_types': class_types,
               'industry_types': industry_types, 'institution_types': institution_types}
    return render(request, "merchant/signup.html", context)


def login_merchant(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user:
            if user.is_merchant and user.is_verified:
                login(request, user)
                return redirect('merchant')

            elif user.is_verified != True:
                return render(request, 'merchant/login.html', {"error": "Account is not verified yet. Pleace check your e-mail."})

        if user is None:
            return render(request, 'merchant/login.html', {'error': 'Your email and password didn\'t match. Please try again.'})

        else:
            return render(request, 'merchant/login.html', {'error': 'Account doesn\'t found. Try signup'})

    return render(request, 'merchant/login.html')


def forms_details(request, user):
    user = User.objects.get(username=str(user))
    if user.is_merchant and user.is_verified:
        try:
            coaching = Coaching.objects.get(merchant=user)
        except:
            coaching = None
        try:
            info = CoachingMetaData.objects.get(coaching=coaching)
        except:
            info = None
        if not coaching:
            return redirect('add_coaching', user=user.username)
        if not info:
            return redirect('owner', user=user.username)
        return redirect("index")
    return render(request, 'merchant/login.html')


class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context


class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = 'registration/password_reset_email.html'
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('merchant/password_reset_done')
    template_name = 'merchant/password_reset/forget-password.html'
    title = _('Password reset')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name = 'merchant/password_reset/password-reset-done.html'
    title = _('Password reset sent')


@login_required(login_url='merchant/login')
def merchant_dashboard(request):
    if request.user.is_merchant:
        # for colleges
        if request.user.merchant_type == 1:
            context = {
                'merchant': request.user,
                'total_courses': len(CollegeCourse.objects.filter(college__user=request.user)),
                'total_faculty': len(CollegeFacultyMember.objects.filter(college__user=request.user))
            }

        # for coaching centers
        elif request.user.merchant_type == 2:
            context = {
                'merchant': request.user,
                'total_courses': len(Course.objects.filter(coaching__merchant=request.user, is_active=True)),
                'total_faculty': len(CoachingFacultyMember.objects.filter(coaching__merchant=request.user))
            }

        # for jobs
        elif request.user.merchant_type == 3:
            context = {
                'merchant': request.user,
                'active_jobs': len(Job.objects.filter(recruiter=JobRecruiter.objects.get(user=request.user))),
                'total_applicants': len(JobApplications.objects.filter(job_appication__recruiter__user=request.user.id))
            }

        return render(request, 'merchant/new_dashboard/merchant_dashboard.html', context=context)
    return render(request, 'merchant/login.html')


@login_required(login_url='merchant/login')
def merchant_messages(request):
    if request.user.is_merchant:
        merchant = request.user

        receiver = User.objects.get(is_superuser=True)
        if request.method == "POST":
            msg = request.POST['msg']
            print(msg)
            message = Message(sender=request.user, receiver=receiver,
                              message=msg, timestamp=datetime.now())
            message.save()
            print(message)
            return redirect('merchant_messages')
        messages = list(Message.objects.filter(
            sender=request.user).filter(receiver=receiver))
        messages += list(Message.objects.filter(
            sender=receiver).filter(receiver=request.user))
        from operator import attrgetter
        messages = sorted(messages, key=attrgetter('id'))
        context = {'messages': messages,
                   'merchant': request.user}
        print(messages)
        return render(request, 'merchant/new_dashboard/chat.html', context)


@login_required(login_url='merchant/login')
def merchant_table(request):
    return render(request, 'merchant/new_dashboard/export-table.html')


@login_required(login_url='merchant/login')
def merchant_contact(request):
    return render(request, 'merchant/new_dashboard/contact.html')


@login_required(login_url='merchant/login')
def merchant_forms2(request):
    return render(request, 'merchant/new_dashboard/basic-form2.html')


@login_required(login_url='merchant/login')
def merchant_gallery(request):
    return render(request, 'merchant/new_dashboard/gallery1.html')


@login_required(login_url='merchant/login')
def merchant_invoice(request):
    return render(request, 'merchant/new_dashboard/invoice.html')


@login_required(login_url='merchant/login')
def merchant_payment(request):
    if request.user.is_merchant:
        merchant = request.user

        try:
            payment = BankAccountDetails.objects.get(coaching=coaching)
        except:
            payment = None
        if request.method == "POST":
            account_holder = request.POST['name']
            bank_name = request.POST['bank_name']
            ifsc = request.POST['ifsc']
            mobile = request.POST['mobile']
            try:
                adhar = request.FILES['adhar']
            except:
                adhar = None
            try:
                pan = request.FILES['pan']
            except:
                pan = None
            account_no = request.POST['number']
            if payment:
                payment = BankAccountDetails.objects.filter(coaching=coaching).update(account_holder=account_holder,
                                                                                      account_no=account_no, ifsc_code=ifsc, bank_name=bank_name, mobile_no=mobile)
                payment = BankAccountDetails.objects.get(coaching=coaching)
                if adhar:
                    payment.adhar_card = adhar
                if pan:
                    payment.pan_card = pan
                payment.save()
            else:
                payment = BankAccountDetails(account_holder=account_holder, account_no=account_no, ifsc_code=ifsc, bank_name=bank_name,
                                             adhar_card=adhar, pan_card=pan, coaching=coaching, mobile_no=mobile)
                payment.save()
            return redirect('payment_info')
        context = {'merchant': request.user,
                   'coaching': coaching, 'account': payment}
        return render(request, 'merchant/new_dashboard/payment.html', context)


@login_required(login_url='merchant/login')
def merchant_profile(request):
    if request.user.is_merchant:
        info = Merchant_Details.objects.get(merchant=request.user)
        merchant = request.user

        if request.method == "POST":
            fname = request.POST['fname']
            lname = request.POST['lname']
            mobile = request.POST['mobile']
            stream = request.POST['stream']
            info = Merchant_Details.objects.filter(id=info.id).update(
                first_name=fname, last_name=lname, mobile=mobile, stream=stream)
            return redirect('merchant_profile')
        context = {'info': info, 'merchant': request.user,
                   'coaching': coaching}
        return render(request, 'merchant/new_dashboard/profile.html', context)
    return render(request, 'signup.html')


@login_required(login_url='merchant/login')
def logout_user(request):
    logout(request)
    return redirect('index')


@login_required(login_url='merchant/login')
def merchant_address(request):
    if request.user.is_merchant:
        merchant = request.user

        try:
            address = Address.objects.get(user=request.user)
        except:
            address = None
        if request.method == "POST":
            line1 = request.POST['line']
            apartment = request.POST['apartment']
            building = request.POST['building']
            landmark = request.POST['landmark']
            city = request.POST['city']
            district = request.POST['district']
            state = request.POST['state']
            pincode = request.POST['pincode']
            if address:
                address = Address.objects.filter(user=request.user).update(line1=line1, apartment=apartment, building=building,
                                                                           landmark=landmark, city=city, district=district, state=state, pincode=pincode)
            else:
                address = Address(user=request.user, line1=line1, apartment=apartment, building=building,
                                  landmark=landmark, city=city, district=district, state=state, pincode=pincode)
                address.save()
            return redirect('merchant_address')
            coaching = Coaching.objects.get(user=request.user)
        context = {'merchant': request.user,
                   'address': address}
        return render(request, 'merchant/new_dashboard/address.html', context)


def subscribe(request):
    if request.method == 'POST':
        Subscriber.objects.create(email=request.POST['email']).save()

        return redirect('merchant_view')


def contact(request):
    if request.method == 'POST':
        CustomerQuestion.objects.create(
            email=request.POST['email'],
            mobile=request.POST['phone'],
            name=request.POST['name'],
            message=request.POST['message']
        ).save()

        return redirect('merchant_view')
