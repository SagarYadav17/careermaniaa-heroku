from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from merchant_app.models import College, CollegeFacultyMember, CollegeCourse


@login_required(login_url='merchant/login')
def profile(request):
    if request.method == "POST":
        College.objects.update(
            contact_no=request.POST['phone'],
            college_address=request.POST['address'],
            college_name=request.POST['college_name'],
            chairman=request.POST['chairman']
        )
        return redirect('college/profile')

    context = {
        'college': College.objects.get(user=request.user)
    }

    return render(request, 'merchant/new_dashboard/colleges/profile.html', context)


def faculty_members(request):
    if request.method == 'POST':
        member = CollegeFacultyMember.objects.create(
            college=College.objects.get(user=request.user),
            full_name=request.POST['full_name'],
            department=request.POST['department'],
            post=request.POST['post']
        )
        member.save()
        return redirect('faculty_members')

    context = {
        'members': CollegeFacultyMember.objects.filter(college=College.objects.get(user=request.user)),
        'total': len(CollegeFacultyMember.objects.filter(college=College.objects.get(user=request.user)))
    }

    return render(request, 'merchant/new_dashboard/colleges/members.html', context)


def delete_faculty_member(request, id):
    CollegeFacultyMember.objects.get(id=id).delete()
    return redirect('faculty_members')


def course(request):
    if request.method == 'POST':
        CollegeCourse.objects.create(
            college=College.objects.get(user=request.user),
            name=request.POST['name'],
            description=request.POST['description'],
            timePeriod=request.POST['timePeriod'],
            fees=request.POST['fees']
        )
        return redirect('college/course')

    courses = CollegeCourse.objects.filter(
        college=College.objects.get(user=request.user))
    context = {
        'courses': courses,
        'total': len(courses)
    }
    return render(request, 'merchant/new_dashboard/colleges/courses.html', context)


def delete_collegeCourse(request, id):
    CollegeCourse.objects.get(id=id).delete()
    return redirect('college/course')
