from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from merchant_app.models import College, CollegeFacultyMember


@login_required(login_url='merchant/login')
def profile(request):
    context = {
        'college': College.objects.get(user=request.user)
    }
    return render(request, 'merchant/new_dashboard/colleges/profile.html', context)


def add_faculty_member(request):
    if request.method == 'POST':
        member = CollegeFacultyMember.objects.create(
            college=College.objects.get(user=request.user),
            full_name=request.POST['full_name'],
            department=request.POST['department'],
            post=request.POST['post']
        )
        member.save()
        return redirect('add_college_member')

    return render(request, 'merchant/new_dashboard/colleges/add_member.html')


def faculty_members(request):
    context = {
        'members': CollegeFacultyMember.objects.filter(college=College.objects.get(user=request.user))
    }

    return render(request, 'merchant/new_dashboard/colleges/members.html', context)
