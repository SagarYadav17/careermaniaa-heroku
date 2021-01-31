from django.urls import path
from merchant_app import views, coaching, job, college


urlpatterns = [
    path('join-us', views.merchant_view, name='merchant_view'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('contact', views.contact, name='contact'),

    path('merchant/register', views.register_merchant, name='merchant/register'),
    path('merchant/login', views.login_merchant, name='merchant/login'),
    path('merchant/reverify', views.reverifyAccount, name='merchant/reverify'),
    path('merchant', views.merchant_dashboard, name='merchant'),
    path('logout', views.logout_merchant, name='merchant/logout'),
    path('merchant/forget-password', views.PasswordResetView.as_view(),
         name='merchant/forget-password'),
    path('merchant/reset_password_sent', views.PasswordResetDoneView.as_view(),
         name='merchant/password_reset_done'),

    path('merchant/messages', views.merchant_messages, name="merchant_messages"),
    path('merchant/table', views.merchant_table, name="merchant_table"),
    path('merchant/contact', views.merchant_contact, name="merchant_contact"),
    path('merchant/forms2', views.merchant_forms2, name="merchant_forms2"),
    path('merchant/gallery', views.merchant_gallery, name="merchant_gallery"),
    path('merchant/invoice', views.merchant_invoice, name="merchant_invoice"),

    path('merchant/courses', coaching.merchant_courses, name="merchant_courses"),
    path('merchant/payment_info', views.merchant_payment, name="payment_info"),
    path('merchant_profile', views.merchant_profile, name="merchant_profile"),
    path('merchant_address', views.merchant_address, name="merchant_address"),

    path('merchant/forms_details/<user>',
         views.forms_details, name='forms_details'),

    path('merchant/add_coaching/<user>',
         coaching.add_coaching, name='add_coaching'),
    path('merchant/coaching', coaching.update_coaching, name='coaching'),

    path('merchant/add_coaching_metadata/<user>',
         coaching.add_coaching_metadata, name='add_coaching_metadata'),
    path('merchant/owner', coaching.update_coaching_metadata, name='owner'),

    path('merchant/add_branch', coaching.add_branch, name='add_branch'),
    path('merchant/update_branch/<str:id>',
         coaching.update_branch, name='update_branch'),
    path('merchant/delete_branch/<str:id>',
         coaching.delete_branch, name='delete_branch'),

    path('merchant/add_course', coaching.add_course, name='add_course'),
    path('merchant/update_course/<str:id>',
         coaching.update_course, name='update_course'),
    path('merchant/delete_course/<str:id>',
         coaching.delete_course, name='delete_course'),

    path('merchant/add_faculty', coaching.add_faculty, name='add_faculty'),
    path('merchant/update_faculty/<str:id>',
         coaching.update_faculty, name='update_faculty'),
    path('merchant/delete_faculty/<str:id>',
         coaching.delete_faculty, name='delete_faculty'),

    path('merchant/add_batch', coaching.add_batch, name='add_batch'),
    path('merchant/update_batch/<str:id>',
         coaching.update_batch, name='update_batch'),
    path('merchant/delete_batch/<str:id>',
         coaching.delete_batch, name='delete_batch'),

    path('merchant/add_offer', coaching.add_offer, name='add_offer'),
    path('merchant/update_offer/<str:id>',
         coaching.update_offer, name='update_offer'),
    path('merchant/delete_offer/<str:id>',
         coaching.delete_offer, name='delete_offer'),

    path('merchant/add_discount', coaching.add_discount, name='add_discount'),
    path('merchant/update_discount/<str:id>',
         coaching.update_discount, name='update_discount'),
    path('merchant/delete_discount/<str:id>',
         coaching.delete_discount, name='delete_discount'),

    # JOBS
    path('merchant/job/profile', job.profile, name='job/profile'),
    path('merchant/create/job', job.add_job, name='add_job'),
    path('merchant/jobs', job.jobs_list, name='all_jobs'),
    path('merchant/delete/job/<str:id>', job.delete_job, name='delete_job'),
    path('merchant/delete/job/applicant/<str:id>',
         job.delete_applicant, name='delete_applicants'),
    path('merchant/job/aplicants/<str:id>',
         job.applicants, name='all_applicants'),

    # COLLEGES
    path('merchant/colllege/profile', college.profile, name='college/profile'),
    path('merchant/college/members',
         college.faculty_members, name='faculty_members'),
    path('merchant/college/member/delete<str:id>',
         college.delete_faculty_member, name='delete_member'),
    path('merchant/college/course', college.course, name='college/course'),
    path('merchant/college/course/delete/<str:id>',
         college.delete_collegeCourse, name='delete/college/course')
]
