from django.shortcuts import render, redirect
from merchant_app.models import Job, JobRecruiter
from django.contrib.auth.decorators import login_required
from mania.models import JobApplications


@login_required(login_url='merchant/login')
def profile(request):
    context = {
        'user': JobRecruiter.objects.get(user=request.user)
    }
    return render(request, 'merchant/new_dashboard/jobs/profile.html', context)


@login_required(login_url='merchant/login')
def add_job(request):
    merchant = request.user
    if request.method == 'POST':
        Job.objects.create(
            description=request.POST['description'],
            recruiter=JobRecruiter.objects.get(user=request.user),
            title=request.POST['title'],
            skills=request.POST['skills'],
            available_posts=request.POST['available_posts']
        ).save()
        return redirect('add_job')

    return render(request, 'merchant/new_dashboard/jobs/add_job.html')


@login_required(login_url='merchant/login')
def jobs_list(request):
    context = {
        'jobs': Job.objects.filter(recruiter=JobRecruiter.objects.get(user=request.user))
    }
    return render(request, 'merchant/new_dashboard/jobs/all_jobs.html', context)


@login_required(login_url='merchant/login')
def delete_job(request, id):
    job = Job.objects.get(id=id)
    job.delete()
    return redirect('all_jobs')


@login_required(login_url='merchant/login')
def applicants(request, id):
    context = {
        'applicants': JobApplications.objects.filter(job_appication__id=id)
    }

    return render(request, 'merchant/new_dashboard/jobs/applicants.html', context)


@login_required(login_url='merchant/login')
def delete_applicant(request, id):
    job = JobApplications.objects.get(id=id)
    job.delete()
    return redirect('all_jobs')
    