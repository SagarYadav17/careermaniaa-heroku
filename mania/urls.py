from django.urls import path, include
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),

    path('register_user', views.register_user, name='register_user'),
    path('login', views.login_user, name='login_user'),

    path('filters', views.filters, name='filters'),
    path('products', views.products, name='products'),
    path('reset_password', auth_views.PasswordResetView.as_view(),
         name='reset_password'),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(
    ), name='password_reset_complete'),
    path('activate/<uidb64>/<token>',
         views.ActivateAccountView.as_view(), name="activate"),
    path('science_coachings', views.science_coachings, name='science_coachings'),
    path('commerce_coachings', views.commerce_coachings,
         name='commerce_coachings'),
    path('other_coachings', views.other_coachings, name='other_coachings'),

    path('add_to_cart/<str:id>', views.add_to_cart, name='add_to_cart'),
    path('cart', views.cart, name='cart'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<str:id>', views.add_to_wishlist, name='add_to_wishlist'),
    path('del_item/<str:id>', views.delete_cartitem, name='del_item'),
    path('del_wishlist_item/<str:id>', views.delete_wishlistitem, name='del_wishlist_item'),
    path('search', views.search, name='search'),
     path('about', views.about, name='about'),

     path("checkout/<str:id>", views.checkout, name="checkout"),
    path("payment", views.handlerequest, name="HandleRequest"),
    path("profile", views.profile, name="profile"),
    path("bookings", views.bookings, name="bookings"),
    path("product/<str:id>", views.product, name="product"),
]
