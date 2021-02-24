from django.contrib import admin

from mania.models import *
from merchant_app.models import *

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    list_filter = ['merchant_type']
    search_fields = ['email', 'username']


class FAQAdmin(admin.ModelAdmin):
    list_display = ['question']
    search_fields = ['question', 'answer']


class CoachingAdmin(admin.ModelAdmin):
    list_display = ['merchant', 'name', 'state']
    search_fields = ['name', 'registration_number',
                     'merchant', 'director_name']
    list_filter = ['state']


class CoachingFacultyMemberAdmin(admin.ModelAdmin):
    list_display = ['coaching', 'name', 'specialization']
    search_fields = ['name']
    list_filter = ['specialization']


class CollegeAdmin(admin.ModelAdmin):
    list_display = ['college_name', 'university_type', 'institute_type']
    search_fields = ['college_name', 'chairman', 'registration_no']
    list_filter = ['university_type', 'institute_type', 'state']


class CollegeFacultyMemberAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'department', 'college']
    search_fields = ['full_name']


class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'status']
    search_fields = ['user']
    list_filter = ['status']


class JobRecruiterAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'state', 'director_name']
    list_filter = ['state', 'industry_type']
    search_fields = ['company_name', 'director_name', 'registration_no']


class JobAdmin(admin.ModelAdmin):
    list_display = ['recruiter', 'title', 'job_type', 'posted_on']
    list_filter = ['job_type', 'posted_on', 'recruiter']


admin.site.register(User, UserAdmin)
admin.site.register(Coaching, CoachingAdmin)
admin.site.register(CoachingMetaData)
admin.site.register(Branch)
admin.site.register(Address)
admin.site.register(Course)
admin.site.register(Batch)
admin.site.register(CoachingFacultyMember, CoachingFacultyMemberAdmin)
admin.site.register(Geolocation)
admin.site.register(BankAccountDetails)
admin.site.register(Merchant_Details)
admin.site.register(Message)
admin.site.register(College, CollegeAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Registration)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(UniversityType)
admin.site.register(ClassType)
admin.site.register(IndustryType)
admin.site.register(InstitutionType)
admin.site.register(Subscriber)
admin.site.register(CustomerQuestion)
admin.site.register(JobRecruiter, JobRecruiterAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(CollegeFacultyMember, CollegeFacultyMemberAdmin)
