from django.urls import path
from merchant_app import views


urlpatterns = [
    path('join-us', views.merchant_view, name='merchant_view'),

    path('register_merchant', views.register_merchant, name='register_merchant'),
    path('login_merchant', views.login_merchant, name='login_merchant'),
    path('merchant', views.merchant_dashboard, name='merchant'),
    path('logout', views.logout_user, name='logout'),

    path('messages', views.merchant_messages, name="merchant_messages"),
    path('table', views.merchant_table, name="merchant_table"),
    path('contact', views.merchant_contact, name="merchant_contact"),
    path('forms2', views.merchant_forms2, name="merchant_forms2"),
    path('gallery', views.merchant_gallery, name="merchant_gallery"),
    path('invoice', views.merchant_invoice, name="merchant_invoice"),

    path('courses', views.merchant_courses, name="merchant_courses"),
    path('payment_info', views.merchant_payment, name="payment_info"),
    path('profile', views.merchant_profile, name="merchant_profile"),

    path('forms_details/<user>', views.forms_details, name='forms_details'),

    path('add_coaching/<user>', views.add_coaching, name='add_coaching'),
    path('coaching', views.update_coaching, name='coaching'),

    path('add_coaching_metadata/<user>',
         views.add_coaching_metadata, name='add_coaching_metadata'),
    path('owner', views.update_coaching_metadata, name='owner'),

    path('add_branch', views.add_branch, name='add_branch'),
    path('update_branch/<str:id>', views.update_branch, name='update_branch'),
    path('delete_branch/<str:id>', views.delete_branch, name='delete_branch'),

    path('add_course', views.add_course, name='add_course'),
    path('update_course/<str:id>', views.update_course, name='update_course'),
    path('delete_course/<str:id>', views.delete_course, name='delete_course'),

    path('add_faculty', views.add_faculty, name='add_faculty'),
    path('update_faculty/<str:id>', views.update_faculty, name='update_faculty'),
    path('delete_faculty/<str:id>', views.delete_faculty, name='delete_faculty'),

    path('add_batch', views.add_batch, name='add_batch'),
    path('update_batch/<str:id>', views.update_batch, name='update_batch'),
    path('delete_batch/<str:id>', views.delete_batch, name='delete_batch'),

    path('add_offer', views.add_offer, name='add_offer'),
    path('update_offer/<str:id>', views.update_offer, name='update_offer'),
    path('delete_offer/<str:id>', views.delete_offer, name='delete_offer'),

    path('add_discount', views.add_discount, name='add_discount'),
    path('update_discount/<str:id>',
         views.update_discount, name='update_discount'),
    path('delete_discount/<str:id>',
         views.delete_discount, name='delete_discount'),
]
