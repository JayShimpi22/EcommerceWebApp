from django.urls import path
from myapp import views
urlpatterns = [
    path('',views.home,name='home'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('update_item/',views.updateItem,name='update_item'),
    path('process_order/',views.process_order,name='process_order'),
    
]
