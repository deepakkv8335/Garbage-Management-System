"""
URL configuration for ECOSORT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    #authentication url's
    path('userregister', views.userregister, name="userregister"),
    path('vendorregister', views.vendorregister, name="vendorregister"),
    path('userlogin', views.userlogin, name="userlogin"),
    path('vendorlogin', views.vendorlogin, name="vendorlogin"),
    path('Logout', views.Logout, name="Logout"),

    #main url's
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('services', views.services, name="services"),
    path('console', views.console, name="console"),
    path('VendorRequests', views.VendorRequests, name="VendorRequests"),
    path('successpage', views.successpage, name="successpage"),
    path('forgetpassworduser', views.forgetpassworduser, name="forgetpassworduser"),
    path('forgetpasswordvendor', views.forgetpasswordvendor, name="forgetpasswordvendor"),
    path('resetpassworduser/<str:user>/', views.resetpassworduser, name="resetpassworduser"),
    path('resetpasswordvendor/<str:user>/', views.resetpasswordvendor, name="resetpasswordvendor"),
    path('resetsuccesspageuser', views.resetsuccesspageuser, name="resetsuccesspageuser"),
    path('resetsuccesspagevendor', views.resetsuccesspagevendor, name="resetsuccesspagevendor"),
    path('emailsuccesspage', views.emailsuccesspage, name="emailsuccesspage"),

    #vendor url's
    path('vendordashboard', views.vendordashboard, name="vendordashboard"),
    path('vendorprofile', views.vendorprofile, name="vendorprofile"),
    path('bookingdetails/<int:id>', views.bookingdetails, name="bookingdetails"),
    path('edit_bookingstatus/<int:id>', views.edit_bookingstatus, name="edit_bookingstatus"),
    path('add_package', views.add_package, name="add_package"),
    path('edit_package/<int:id>', views.edit_package, name="edit_package"),
    path('delete_package/<int:id>', views.delete_package, name="delete_package"),

    #user url's
    path('userhome', views.userhome, name="userhome"),
    path('userservices', views.userservices, name="userservices"),
    path('userprofile', views.userprofile, name="userprofile"),
    path('servicebooking/<int:id>', views.servicebooking, name="servicebooking"),
    path('userviewbookings', views.userviewbookings, name="userviewbookings"),
    path('payments/<int:id>', views.payments, name="payments"),
    path('cancel_booking/<int:id>', views.cancel_booking, name="cancel_booking"),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
