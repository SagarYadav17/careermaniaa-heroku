from django.contrib import admin

from mania.models import *
from merchant_app.models import *

# Register your models here.

admin.site.register(User)

admin.site.register(Coaching)
admin.site.register(CoachingMetaData)
admin.site.register(Branch)
admin.site.register(Address)
admin.site.register(Course)
admin.site.register(Batch)
admin.site.register(CoachingFacultyMember)
admin.site.register(Geolocation)
admin.site.register(BankAccountDetails)
admin.site.register(Merchant_Details)
admin.site.register(Message)
admin.site.register(College)
admin.site.register(Job)
admin.site.register(Registration)
admin.site.register(FAQ)
admin.site.register(UniversityType)
admin.site.register(ClassType)
admin.site.register(IndustryType)
admin.site.register(InstitutionType)
admin.site.register(Subscriber)
admin.site.register(CustomerQuestion)
admin.site.register(JobRecruiter)
