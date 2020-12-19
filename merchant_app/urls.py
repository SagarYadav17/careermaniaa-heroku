from django.urls import path
from merchant_app import views


urlpatterns = [
    path('join-us', views.merchant_view, name='merchant_view'),

    path('merchant/register', views.register_merchant, name='merchant/register'),
    path('merchant/login', views.login_merchant, name='merchant/login'),
    path('merchant', views.merchant_dashboard, name='merchant'),
    path('logout', views.logout_user, name='logout'),
    path('merchant/forget-password', views.PasswordResetView.as_view(), name='merchant/forget-password'),

    path('merchant/messages', views.merchant_messages, name="merchant_messages"),
    path('merchant/table', views.merchant_table, name="merchant_table"),
    path('merchant/contact', views.merchant_contact, name="merchant_contact"),
    path('merchant/forms2', views.merchant_forms2, name="merchant_forms2"),
    path('merchant/gallery', views.merchant_gallery, name="merchant_gallery"),
    path('merchant/invoice', views.merchant_invoice, name="merchant_invoice"),

<<<<<<< HEAD
    path('courses', views.merchant_courses, name="merchant_courses"),
    path('payment_info', views.merchant_payment, name="payment_info"),
    path('merchant_profile', views.merchant_profile, name="merchant_profile"),
=======
    path('merchant/courses', views.merchant_courses, name="merchant_courses"),
    path('merchant/payment_info', views.merchant_payment, name="payment_info"),
    path('merchant/profile', views.merchant_profile, name="merchant_profile"),
>>>>>>> 8509701e0746e6745bf7c3fc1c8f015422280cdd

    path('merchant/forms_details/<user>',
         views.forms_details, name='forms_details'),

    path('merchant/add_coaching/<user>',
         views.add_coaching, name='add_coaching'),
    path('merchant/coaching', views.update_coaching, name='coaching'),

    path('merchant/add_coaching_metadata/<user>',
         views.add_coaching_metadata, name='add_coaching_metadata'),
    path('merchant/owner', views.update_coaching_metadata, name='owner'),

    path('merchant/add_branch', views.add_branch, name='add_branch'),
    path('merchant/update_branch/<str:id>',
         views.update_branch, name='update_branch'),
    path('merchant/delete_branch/<str:id>',
         views.delete_branch, name='delete_branch'),

    path('merchant/add_course', views.add_course, name='add_course'),
    path('merchant/update_course/<str:id>',
         views.update_course, name='update_course'),
    path('merchant/delete_course/<str:id>',
         views.delete_course, name='delete_course'),

    path('merchant/add_faculty', views.add_faculty, name='add_faculty'),
    path('merchant/update_faculty/<str:id>',
         views.update_faculty, name='update_faculty'),
    path('merchant/delete_faculty/<str:id>',
         views.delete_faculty, name='delete_faculty'),

    path('merchant/add_batch', views.add_batch, name='add_batch'),
    path('merchant/update_batch/<str:id>',
         views.update_batch, name='update_batch'),
    path('merchant/delete_batch/<str:id>',
         views.delete_batch, name='delete_batch'),

    path('merchant/add_offer', views.add_offer, name='add_offer'),
    path('merchant/update_offer/<str:id>',
         views.update_offer, name='update_offer'),
    path('merchant/delete_offer/<str:id>',
         views.delete_offer, name='delete_offer'),

    path('merchant/add_discount', views.add_discount, name='add_discount'),
    path('merchant/update_discount/<str:id>',
         views.update_discount, name='update_discount'),
    path('merchant/delete_discount/<str:id>',
         views.delete_discount, name='delete_discount'),
]
