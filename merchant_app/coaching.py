from django.shortcuts import render, redirect
from mania.models import User
from merchant_app.models import *

from django.contrib.auth.decorators import login_required


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
        coaching = Coaching.objects.get(merchant=merchant)
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
def add_coaching(request, user):
    user = User.objects.get(username=user)
    if user.is_merchant and user.is_verified:
        if request.method == "POST":
            name = request.POST['name']
            registration_number = request.POST['reg']
            country = request.POST['country']
            state = request.POST['state']
            address = request.POST['address']
            director_name = request.POST['director']
            phone_number = request.POST['phone']
            image = request.FILES['image']
            merchant = user
            coaching = Coaching(
                name=name, merchant=merchant, logo=image, registration_number=registration_number, country=country,
                state=state, address=address, director_name=director_name, phone_number=phone_number)
            coaching.save()
            return redirect('add_coaching_metadata', user=user.username)
        return render(request, 'merchant/dashboard/add_coaching.html', {'merchant': user})
    return render(request, 'signup.html')


@login_required(login_url='merchant/login')
def add_coaching_metadata(request, user):
    user = User.objects.get(username=user)
    if user.is_merchant and user.is_verified:
        if request.method == "POST":
            name = request.POST['name']
            mobile = request.POST['contact1']
            establish = request.POST['date']
            owner_image = request.FILES['owner_image']
            merchant = user
            coaching = Coaching.objects.get(merchant=merchant)
            coaching_data = CoachingMetaData(coaching=coaching, mobile=mobile,
                                             owner_name=name, established_on=establish, owner_image=owner_image)
            coaching_data.save()
            return redirect('merchant_view')
        return render(request, 'merchant/dashboard/add_coaching_metadata.html', {'merchant': user})
    return render(request, 'signup.html')


@login_required(login_url='merchant/login')
def update_coaching(request):
    if request.user.is_merchant:
        merchant = request.user
        coaching = Coaching.objects.get(merchant=merchant)
        if request.method == "POST":
            name = request.POST['name']
            registration_number = request.POST['reg']
            country = request.POST['country']
            state = request.POST['state']
            address = request.POST['address']
            director_name = request.POST['director']
            phone_number = request.POST['phone']
            image = request.FILES['image']
            coaching.name = name
            coaching.registration_number = registration_number
            coaching.country = country
            coaching.state = state
            coaching.address = address
            coaching.director_name = director_name
            coaching.phone_number = phone_number
            try:
                image = request.FILES['logo']
            except:
                image = None
            if image:
                coaching.logo = image
            coaching.save()
            return redirect('coaching')
        context = {'merchant': request.user, 'coaching': coaching}
        return render(request, 'merchant/new_dashboard/coaching.html', context=context)
    return render(request, 'signup.html')


@login_required(login_url='merchant/login')
def update_coaching_metadata(request):
    if request.user.is_merchant:
        merchant = request.user
        coaching = Coaching.objects.get(merchant=merchant)
        info = CoachingMetaData.objects.get(coaching=coaching)
        if request.method == "POST":
            name = request.POST['name']
            mobile = request.POST['mobile']
            establish = request.POST['date']
            info.owner_name = name
            info.established_on = establish
            info.mobile = mobile
            try:
                owner_image = request.FILES['owner_image']
            except:
                owner_image = None
            if owner_image:
                info.owner_image = owner_image
            info.save()
            return redirect('owner')
        context = {'merchant': request.user,
                   'coaching': coaching, 'owner': info}
        return render(request, 'merchant/new_dashboard/owner.html', context)
    return render(request, 'signup.html')


@login_required(login_url='merchant/login')
def add_branch(request):
    if request.user.is_merchant:
        merchant = request.user
        merchant = request.user
        coaching = Coaching.objects.get(merchant=merchant)
        if request.method == "POST":
            name = request.POST['name']
            branch_type = request.POST['branch_type']
            branch = Branch(name=name, coaching=coaching,
                            branch_type=branch_type)
            branch.save()
            return redirect('add_branch')
        branches = Branch.objects.filter(coaching=coaching)
        context = {'merchant': request.user,
                   'coaching': coaching, 'branches': branches}
        return render(request, 'merchant/new_dashboard/branch.html', context)
    return render(request, 'signup.html')


@login_required(login_url='merchant/login')
def update_branch(request, id):
    if request.user.is_merchant:
        merchant = request.user
        coaching = Coaching.objects.get(merchant=merchant)
        if request.method == "POST":
            name = request.POST['name']
            branch_type = request.POST['branch_type']
            branch = Branch.objects.filter(id=id).update(
                name=name, branch_type=branch_type)
            return redirect('add_branch')
        branches = Branch.objects.filter(coaching=coaching)
        branch = Branch.objects.get(id=id)
        context = {'merchant': request.user, 'coaching': coaching,
                   'branches': branches, 'branch': branch}
        return render(request, 'merchant/new_dashboard/branch.html', context)
    return render(request, 'signup.html')


@login_required(login_url='merchant/login')
def delete_branch(request, id):
    if request.user.is_merchant:
        branch = Branch.objects.get(id=id)
        branch.delete()
        return redirect('add_branch')
    return render(request, 'signup.html')


@login_required(login_url='merchant/login')
def merchant_courses(request):
    if request.user.is_merchant:
        merchant = request.user
        coaching = Coaching.objects.get(merchant=merchant)
        branches = Branch.objects.filter(coaching=coaching)
        courses = Course.objects.filter(coaching=coaching)
        context = {'courses': courses,
                   'merchant': request.user, 'coaching': coaching}
        return render(request, 'merchant/new_dashboard/courses.html', context)


@login_required(login_url='merchant/login')
def add_course(request):
    if request.user.is_merchant:
        merchant = request.user
        coaching = Coaching.objects.get(merchant=merchant)
        if request.method == "POST":
            branch_taken = request.POST['branch']
            stream = request.POST['stream']
            name = request.POST['name']
            description = request.POST['description']
            timeperiod = request.POST['timeperiod']
            trial = request.POST['trial']
            fees = float(request.POST['fees'])
            currency = request.POST['currency']
            active = request.POST['active']
            branch = Branch.objects.get(name=branch_taken)
            course = Course(name=name, description=description, branch=branch, timePeriod=timeperiod, trial=trial,
                            stream=stream, fees=fees, currency=currency, coaching=coaching)
            myfile = request.FILES["syllabus"]
            course.syllabus = myfile
            if active == "off":
                course.is_active = False
            elif active == "on":
                course.is_active = True
            course.save()
            return redirect('add_course')
        branches = Branch.objects.filter(coaching=coaching)
        streams = ['Science', 'Commerce', 'Other']
        context = {'merchant': request.user,
                   'coaching': coaching, 'branches': branches, 'streams': streams}
        return render(request, 'merchant/new_dashboard/add_course.html', context)
    return render(request, 'merchant/signup.html')


@login_required(login_url='merchant/login')
def update_course(request, id):
    if request.user.is_merchant:
        merchant = request.user
        coaching = Coaching.objects.get(merchant=merchant)
        if request.method == "POST":
            branch_taken = request.POST['branch']
            stream = request.POST['stream']
            name = request.POST['name']
            description = request.POST['description']
            timeperiod = request.POST['timeperiod']
            trial = request.POST['trial']
            fees = float(request.POST['fees'])
            currency = request.POST['currency']
            active = request.POST['active']
            branch = Branch.objects.get(name=branch_taken)
            course = Course.objects.filter(id=id).update(name=name, description=description, branch=branch, timePeriod=timeperiod, trial=trial,
                                                         stream=stream, fees=fees, currency=currency)
            course = Course.objects.get(id=id)
            try:
                myfile = request.FILES["syllabus"]
                course.syllabus = myfile
            except:
                myfile = None
            if active == "off":
                course.is_active = False
            elif active == "on":
                course.is_active = True
            course.save()
            return redirect('merchant_courses')
        branches = Branch.objects.filter(coaching=coaching)
        course = Course.objects.get(id=id)
        streams = ['Science', 'Commerce', 'Other']
        context = {'merchant': request.user,
                   'coaching': coaching, 'branches': branches, 'streams': streams, 'course': course}
        return render(request, 'merchant/new_dashboard/add_course.html', context)
    return render(request, 'merchant/signup.html')


@login_required(login_url='merchant/login')
def delete_course(request, id):
    if request.user.is_merchant:
        course = Course.objects.get(id=id)
        course.delete()
        return redirect('merchant_courses')
    return render(request, 'signup.html')


@login_required(login_url='merchant/login')
def add_faculty(request):
    if request.user.is_merchant:
        merchant = request.user
        coaching = Coaching.objects.get(merchant=merchant)
        if request.method == "POST":
            name = request.POST['name']
            age = int(request.POST['age'])
            specialization = request.POST['specialization']
            faculty_image = request.FILES['pic']
            faculty = CoachingFacultyMember(name=name, age=age, specialization=specialization,
                                            coaching=coaching, faculty_image=faculty_image)
            faculty.save()
            return redirect('add_faculty')
        faculties = CoachingFacultyMember.objects.filter(coaching=coaching)
        context = {'merchant': request.user,
                   'coaching': coaching, 'faculties': faculties}
        return render(request, 'merchant/new_dashboard/faculty.html', context)
    return render(request, 'merchant/signup.html')


@login_required(login_url='merchant/login')
def update_faculty(request, id):
    if request.user.is_merchant:
        merchant = request.user
        coaching = Coaching.objects.get(merchant=merchant)
        if request.method == "POST":
            name = request.POST['name']
            age = int(request.POST['age'])
            specialization = request.POST['specialization']
            try:
                faculty_image = request.FILES['pic']
            except:
                faculty_image = None
            faculty = CoachingFacultyMember.objects.filter(id=id).update(
                name=name, age=age, specialization=specialization)
            faculty = CoachingFacultyMember.objects.get(id=id)
            if faculty_image:
                faculty.faculty_image = faculty_image
            faculty.save()
            return redirect('add_faculty')
        faculties = CoachingFacultyMember.objects.filter(coaching=coaching)
        faculty = CoachingFacultyMember.objects.get(id=id)
        context = {'merchant': request.user, 'coaching': coaching,
                   'faculties': faculties, 'edit_faculty': faculty}
        return render(request, 'merchant/new_dashboard/faculty.html', context)
    return render(request, 'merchant/signup.html')


@login_required(login_url='merchant/login')
def delete_faculty(request, id):
    if request.user.is_merchant:
        faculty = CoachingFacultyMember.objects.get(id=id)
        faculty.delete()
        return redirect('add_faculty')
    return render(request, 'signup.html')


@login_required(login_url='merchant/login')
def add_batch(request):
    if request.user.is_merchant:
        merchant = request.user
        coaching = Coaching.objects.get(merchant=merchant)
        if request.method == "POST":
            name = request.POST['name']
            limit = request.POST['limit']
            start = request.POST['start']
            end = request.POST['end']
            enrolled = float(request.POST['enrolled'])
            active = request.POST['active']
            course_taken = request.POST['course']
            course = Course.objects.get(name=course_taken)
            faculty_taken = request.POST['faculty']
            faculty = CoachingFacultyMember.objects.get(name=faculty_taken)
            batch = Batch(name=name, student_limit=limit, start_time=start, end_time=end, students_enrolled=enrolled,
                          course=course, teacher=faculty)
            if active == "off":
                batch.is_active = False
            elif active == "on":
                batch.is_active = True
            batch.save()
            return redirect('add_batch')
        coaching = Coaching.objects.get(merchant=merchant)
        branches = Branch.objects.filter(coaching=coaching)
        batches = []
        courses = Course.objects.filter(coaching=coaching)
        for course in courses:
            batches += list(Batch.objects.filter(course=course))
        faculties = CoachingFacultyMember.objects.filter(coaching=coaching)
        context = {'merchant': request.user, 'coaching': coaching,
                   'courses': courses, 'faculties': faculties, 'batches': batches}
        return render(request, 'merchant/new_dashboard/batch.html', context)
    return render(request, 'merchant/signup.html')


@login_required(login_url='merchant/login')
def update_batch(request, id):
    if request.user.is_merchant:
        merchant = request.user
        coaching = Coaching.objects.get(merchant=merchant)
        batch = Batch.objects.get(id=id)
        if request.method == "POST":
            name = request.POST['name']
            limit = request.POST['limit']
            start = request.POST['start']
            end = request.POST['end']
            enrolled = float(request.POST['enrolled'])
            active = request.POST['active']
            course_taken = request.POST['course']
            course = Course.objects.get(name=course_taken)
            faculty_taken = request.POST['faculty']
            faculty = CoachingFacultyMember.objects.get(name=faculty_taken)
            batch = Batch.objects.filter(id=id).update(name=name, student_limit=limit, start_time=start, end_time=end, students_enrolled=enrolled,
                                                       course=course, teacher=faculty)
            batch = Batch.objects.get(id=id)
            if active == "off":
                batch.is_active = False
            elif active == "on":
                batch.is_active = True
            batch.save()
            return redirect('add_batch')
        coaching = Coaching.objects.get(merchant=merchant)
        branches = Branch.objects.filter(coaching=coaching)
        courses = []
        batches = []
        for branch in branches:
            courses += list(Course.objects.filter(branch=branch))
        for course in courses:
            batches += list(Batch.objects.filter(course=course))
        faculties = CoachingFacultyMember.objects.filter(coaching=coaching)
        context = {'merchant': request.user, 'coaching': coaching, 'courses': courses,
                   'faculties': faculties, 'batches': batches, 'edit_batch': batch}
        return render(request, 'merchant/new_dashboard/batch.html', context)
    return render(request, 'signup.html')


@login_required(login_url='merchant/login')
def delete_batch(request, id):
    if request.user.is_merchant:
        batch = Batch.objects.get(id=id)
        batch.delete()
        return redirect('add_batch')
    return render(request, 'signup.html')


@login_required(login_url='merchant/login')
def add_offer(request):
    if request.user.is_merchant:
        merchant = request.user
        coaching = Coaching.objects.get(merchant=merchant)
        if request.method == "POST":
            name = request.POST['name']
            description = request.POST['description']
            offer = Offer(name=name, description=description,
                          coaching=coaching)
            offer.save()
            return redirect('add_offer')
        offers = Offer.objects.filter(coaching=coaching)
        return render(request, 'merchant/new_dashboard/offer.html', {'offers': offers, 'merchant': request.user, 'coaching': coaching})
    return render(request, 'signup.html')


@login_required(login_url='merchant/login')
def update_offer(request, id):
    if request.user.is_merchant:
        merchant = request.user
        coaching = Coaching.objects.get(merchant=merchant)
        offer = Offer.objects.get(id=id)
        if request.method == "POST":
            name = request.POST['name']
            description = request.POST['description']
            offer.name = name
            offer.description = description
            offer.save()
            return redirect('add_offer')
        offers = Offer.objects.filter(coaching=coaching)
        return render(request, 'merchant/new_dashboard/offer.html', {'offers': offers, 'edit_offer': offer, 'merchant': request.user, 'coaching': coaching})
    return render(request, 'signup.html')


@login_required(login_url='merchant/login')
def delete_offer(request, id):
    if request.user.is_merchant:
        offer = Offer.objects.get(id=id)
        offer.delete()
        return redirect('add_offer')
    return render(request, 'signup.html')


@login_required(login_url='merchant/login')
def add_discount(request):
    if request.user.is_merchant:
        merchant = request.user
        coaching = Coaching.objects.get(merchant=merchant)
        if request.method == "POST":
            coupon = request.POST['coupon']
            description = request.POST['description']
            percent = request.POST['percent']
            discount = Discount(disc_code=coupon, description=description,
                                disc_percent=percent, coaching=coaching)
            discount.save()
            return redirect('add_discount')
        discounts = Discount.objects.filter(coaching=coaching)
        return render(request, 'merchant/new_dashboard/discount.html', {'discounts': discounts, 'merchant': request.user, 'coaching': coaching})
    return render(request, 'signup.html')


@login_required(login_url='merchant/login')
def update_discount(request, id):
    if request.user.is_merchant:
        merchant = request.user
        coaching = Coaching.objects.get(merchant=merchant)
        discount = Discount.objects.get(id=id)
        if request.method == "POST":
            coupon = request.POST['coupon']
            description = request.POST['description']
            percent = request.POST['percent']
            discount.disc_code = coupon
            discount.description = description
            discount.disc_percent = percent
            discount.save()
            return redirect('add_discount')
        discounts = Discount.objects.filter(coaching=coaching)
        return render(request, 'merchant/new_dashboard/discount.html', {'discounts': discounts, 'edit_discount': discount, 'merchant': request.user, 'coaching': coaching})
    return render(request, 'signup.html')


@login_required(login_url='merchant/login')
def delete_discount(request, id):
    if request.user.is_merchant:
        discount = Discount.objects.get(id=id)
        discount.delete()
        return redirect('add_discount')
    return render(request, 'signup.html')


