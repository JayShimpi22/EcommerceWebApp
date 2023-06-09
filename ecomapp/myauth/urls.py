from django.urls import path
from myauth import views
urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',views.loginapp,name='loginapp'),
    path('logout/',views.logoutapp,name='logout'),
    path('activate/<uidb64>/<token>/',views.ActivateAccount.as_view(),name='activate'),
    path('reset-password/',views.RequestResetPasswordView.as_view(),name='reset_password'),
    path('set-new-password/<uidb64>/<token>/',views.SetNewPasswordView.as_view(),name='set-new-password'),

]
