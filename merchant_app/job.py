from django.shortcuts import render, redirect
from merchant_app.forms import CreateJob
from merchant_app.models import Job, JobRecruiter
from django.contrib.auth.decorators import login_required


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
        form = CreateJob(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = merchant
            data.save()
            return redirect('add_job')

    return render(request, 'merchant/new_dashboard/jobs/add_job.html')


@login_required(login_url='merchant/login')
def jobs_list(request):
    context = {
        'jobs': Job.objects.filter(recruiter=request.user.id)
    }
    return render(request, 'merchant/new_dashboard/jobs/all_jobs.html', context)


@login_required(login_url='merchant/login')
def delete_job(request, id):
    job = Job.objects.get(id=id)
    job.delete()
    return redirect('all_jobs')
