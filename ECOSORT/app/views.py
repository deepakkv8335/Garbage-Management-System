from django.shortcuts import render, redirect
from .models import CustomUser, Package, Booking #, HealthAssistant
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.urls import reverse
from django.utils import timezone
from .forms import BookingStatusForm
from django.http import HttpResponse
from app.models import VendorRequest
from django.core.mail import send_mail
from ECOSORT.settings import EMAIL_HOST_USER


#authentication section
def userregister(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']

        if CustomUser.objects.filter(username=username).exists():
            messages.info(request, 'Username is occupied')
            return redirect(userregister)
        
        elif CustomUser.objects.filter(phone_number=phone).exists():
            messages.error(request, 'Phone number is already registered')
            return redirect(userregister)
        
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email address is already registered')
            return redirect(userregister)
    
        else:
            data = CustomUser.objects.create_user(username=username, email=email, password=password, phone_number=phone, user_type="user")
            data.save()
            send_mail("Welcome", f"Hey {username},\nWe're excited to let you know that your account has been successfully created!\nNow you're ready to explore all the great features we have to offer.", EMAIL_HOST_USER, [email], fail_silently=True)
            messages.success(request, "Account created sucessfully!")
            return redirect(userlogin)
    else:
        return render(request, 'userregister.html')
    

def vendorregister(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username is occupied')
            return redirect(vendorregister)
        
        elif CustomUser.objects.filter(phone_number=phone).exists():
            messages.error(request, 'Phone number is already registered')
            return redirect(vendorregister)
        
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email address is already registered')
            return redirect(vendorregister)
        
        else:
            data = CustomUser.objects.create_user(username=username, email=email, password=password, phone_number=phone, user_type="agency")
            data.save()
            send_mail("Welcome", f"Hey {username},\nWe're excited to let you know that your vendor account has been successfully created!\nNow you're ready to explore all the great features we have to offer.", EMAIL_HOST_USER, [email], fail_silently=True)
            messages.success(request, "Account created sucessfully")
            return redirect(vendorlogin)
    else:
        return render(request, 'vendorregister.html')
    

def userlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        admin_user = authenticate(request, username=username, password=password)
        if admin_user is not None and admin_user.is_staff:
            login(request, admin_user)
            return redirect(reverse('admin:index'))
             
        elif user is not None:    
            login(request, user)
            if user.user_type == "user":     
                return redirect(userhome)
            if user.user_type == "agency":
                context = {
                'message': "Invalid login credentials"
            }
            return render(request, 'userlogin.html', context)
        else:
            context = {
                'message': "Invalid login credentials"
            }
            return render(request, 'userlogin.html', context)
    else:
        return render(request, 'userlogin.html')
    

def vendorlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        admin_user = authenticate(request, username=username, password=password)
        if admin_user is not None and admin_user.is_staff:
            login(request, admin_user)
            return redirect(reverse('admin:index')) 
        elif user is not None:
                 
            login(request, user)
            if user.user_type == "agency":     
                return redirect(vendordashboard)
            if user.user_type == "user":
                context = {
                'message': "Invalid login credentials"
            }
            return render(request, 'vendorlogin.html', context)
        else:
            context = {
                'message': "Invalid login credentials"
            }
            return render(request, 'vendorlogin.html', context)
    else:
        return render(request, 'vendorlogin.html')
    

def Logout(request):
    logout(request)
    return redirect(index)


#main section
def index(request):
    data = Package.objects.all().order_by('-price')
    return render(request, 'index.html', {'packages':data})


def services(request):
    return render(request, 'services.html')

def console(request):
    return render(request, 'console.html')


def VendorRequests(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        print(name,email,phone)
        ins = VendorRequest(name=name,email=email,phone=phone)
        ins.save()
        send_mail("Applied Successfully", f"Hey {name},\nYou have successfully applied for the Vendor Program.\nOur team will review your submission and get back to you shortly.", EMAIL_HOST_USER, [email], fail_silently=True)
        messages.success(request, "Details submitted sucessfully, We wil contact you soon!")
        return redirect(successpage)

    return render(request, 'VendorRequests.html')


def successpage(request):
    return render(request, 'successpage.html')


def forgetpassworduser(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            print("Email: ", email)
            if user.user_type == "user":   
                print("Working")
                if CustomUser.objects.filter(email=email).exists():
                    user = CustomUser.objects.get(email=email)
                    print("User Exist")
                    send_mail("Reset Your Password", f"Hey {user},\nClick the link to reset your password.\n http://127.0.0.1:8000/resetpassworduser/{user}/", EMAIL_HOST_USER, [email], fail_silently=True)
                    messages.success(request, "A password reset email has been successfully sent to your inbox!")
                    return redirect(emailsuccesspage)
                else:
                    messages.success(request, "Email doesn't exist")
                    return render(request, 'forgetpassworduser.html')
            else:
                messages.success(request, "Email doesn't exist")
                return render(request, 'forgetpassworduser.html')
        else:
            messages.success(request, "Email doesn't exist")
            return render(request, 'forgetpassworduser.html')
    return render(request, 'forgetpassworduser.html')


def forgetpasswordvendor(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            print("Email: ", email)
            if user.user_type == "agency":   
                print("Working")
                if CustomUser.objects.filter(email=email).exists():
                    user = CustomUser.objects.get(email=email)
                    print("User Exist")
                    send_mail("Reset Your Password", f"Hey {user},\nClick the link to reset your password.\n http://127.0.0.1:8000/resetpasswordvendor/{user}/", EMAIL_HOST_USER, [email], fail_silently=True)
                    messages.success(request, "A password reset email has been successfully sent to your inbox!")
                    return redirect(emailsuccesspage)
                else:
                    messages.success(request, "Email doesn't exist")
                    return render(request, 'forgetpasswordvendor.html')
            else:
                messages.success(request, "Email doesn't exist")
                return render(request, 'forgetpasswordvendor.html')
        else:
            messages.success(request, "Email doesn't exist")
            return render(request, 'forgetpasswordvendor.html')
    return render(request, 'forgetpasswordvendor.html')


def resetpassworduser(request, user):
    userid = CustomUser.objects.get(username=user)
    useremail = userid.email
    print("Userid: ", userid)
    print("Useremail: ", useremail)
    if request.method == "POST":
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")
        print("Pass1 and Pass2: ", pass1 , pass2)

        if pass1 == pass2:
            userid.set_password(pass1)
            userid.save()
            messages.success(request, "Password reset sucessfully!")
            send_mail("Your Password Has Been Successfully Reset", f"Your password has been successfully reset.\nYou can now log in to your account using your new password.", EMAIL_HOST_USER, [useremail], fail_silently=True)
            return redirect(resetsuccesspageuser)
        else:
            messages.error(request, "Password doesn't match!")
            return render(request, "resetpassworduser.html")

    return render(request, "resetpassworduser.html")


def resetpasswordvendor(request, user):
    userid = CustomUser.objects.get(username=user)
    useremail = userid.email
    print("Userid: ", userid)
    print("Useremail: ", useremail)
    if request.method == "POST":
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")
        print("Pass1 and Pass2: ", pass1 , pass2)
        
        if pass1 == pass2:
            userid.set_password(pass1)
            userid.save()
            messages.success(request, "Password reset sucessfully!")
            send_mail("Your Password Has Been Successfully Reset", f"Your password has been successfully reset.\nYou can now log in to your account using your new password.", EMAIL_HOST_USER, [useremail], fail_silently=True)
            return redirect(resetsuccesspagevendor)
        else:
            messages.error(request, "Password doesn't match!")
            return render(request, "resetpasswordvendor.html")

    return render(request, "resetpasswordvendor.html")


def resetsuccesspageuser(request):
    return render(request, 'resetsuccesspageuser.html')


def resetsuccesspagevendor(request):
    return render(request, 'resetsuccesspagevendor.html')


def emailsuccesspage(request):
    return render(request, 'emailsuccesspage.html')


#vendor section
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=vendorlogin)
def vendordashboard(request):
    User = CustomUser.objects.get(id=request.user.id)
    booking_data = Booking.objects.filter(package_id__user_id=request.user.id).order_by('-status')
    pending_bookings_count = Booking.objects.filter(status='pending').count()
    waiting_bookings_count = Booking.objects.filter(status='waiting').count()
    approved_bookings_count = Booking.objects.filter(status='approved').count()
    reject_bookings_count = Booking.objects.filter(status='reject').count()
    picked_bookings_count = Booking.objects.filter(status='picked').count()


    context = {
        'bookings':booking_data,
        'User':User,
        'pending_bookings_count':pending_bookings_count,
        'waiting_bookings_count':waiting_bookings_count,
        'approved_bookings_count':approved_bookings_count,
        'reject_bookings_count':reject_bookings_count,
        'picked_bookings_count':picked_bookings_count
    }
    return render(request, 'Vendor/vendordashboard.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=vendorlogin)
def vendorprofile(request):
    User = CustomUser.objects.get(id=request.user.id)
    if request.method == 'POST':
        User.username = request.POST['username']
        User.email = request.POST['email']
        User.phone_number = request.POST['phone_number']

        if CustomUser.objects.filter(username=User.username).exists():
            # messages.info(request, 'Username is occupied')
            return redirect(vendorprofile)
        
        User.save()
        return redirect(vendorprofile)
    else:
        context = {
            'User':User,
        }
        return render(request, 'Vendor/vendorprofile.html', context)
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=vendorlogin)
def bookingdetails(request,id):
    User = CustomUser.objects.get(id=request.user.id)
    booking_data = Booking.objects.get(id=id)
    print(booking_data)
    context = {
        'bookings':booking_data,
        'User':User
    }
    return render(request, 'Vendor/bookingdetails.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=vendorlogin)    
def edit_bookingstatus(request,id):
    booking = Booking.objects.get(id=id)
    if request.method == 'POST':
        user_email = booking.user_id.email

        status = request.POST['status']
        if status == 'approve':
            booking.status = 'waiting'
            send_mail("Pickup Accepted", f"Your order has been accepted successfully.\nIt will be picked up on the scheduled day.", EMAIL_HOST_USER, [user_email], fail_silently=True)
        elif status == 'reject':
            booking.status = 'reject'
            send_mail("Pickup Rejected", f"Unfortunately, your order has been rejected.\nPlease contact us if you have any questions or need further assistance.", EMAIL_HOST_USER, [user_email], fail_silently=True)
        elif status == 'picked':
            booking.status = 'picked'
            send_mail("Pickup Sucessful", f"Your order has been successfully picked up.\nThank you for choosing our service!", EMAIL_HOST_USER, [user_email], fail_silently=True)
        booking.save()
        return redirect(vendordashboard)
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=vendorlogin)
def add_package(request):
    user = CustomUser.objects.get(id=request.user.id)
    if request.method == 'POST':
        package_name = request.POST['package_name']
        price = request.POST['price']
        description = request.POST['description']
        
        data = Package.objects.create(user_id=user, 
                                      package_name=package_name, 
                                      price=price, 
                                      description=description
                                    )
        data.save()
        packages = Package.objects.filter(user_id=user)
        return render(request, 'Vendor/addpackage.html', {'packages':packages, 'User':user})
    else:
        packages = Package.objects.filter(user_id=user)
        return render(request, 'Vendor/addpackage.html', {'packages':packages, 'User':user})
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=vendorlogin)
def edit_package(request, id):
    user = CustomUser.objects.get(id=request.user.id)
    packages = Package.objects.get(user_id=user, id=id)
    if request.method == 'POST':
        packages.package_name = request.POST['package_name']
        packages.price = request.POST['price']
        packages.description = request.POST['description']
        packages.is_active =False

        packages.save()
        
        return redirect(add_package)
    else:
        context = {
            'id':id,
            'packages':packages
        }    
        return render(request, 'Vendor/edit-package.html', context)
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=vendorlogin)
def delete_package(request, id):
    data = Package.objects.get(id=id)
    data.delete()
    return redirect(add_package)


#user section
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=userlogin)
def userhome(request):
    User = CustomUser.objects.get(id=request.user.id)
    packages = Package.objects.all().order_by('-price')
    context = {
        'User':User,
        'packages':packages 
    }
    return render(request, 'User/userhome.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=userlogin)
def userservices(request):
    User = CustomUser.objects.get(id=request.user.id)
    packages = Package.objects.all().order_by('-price')
    context = {
        'User':User,
        'packages':packages 
    }
    return render(request, 'User/userservices.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=userlogin)
def userprofile(request):
    User = CustomUser.objects.get(id=request.user.id)
    if request.method == 'POST':
        User.username = request.POST['username']
        User.email = request.POST['email']
        User.phone_number = request.POST['phone_number']

        if CustomUser.objects.filter(username=User.username).exists():
            messages.info(request, 'Username is occupied')
            return redirect(userprofile)
        
        User.save()
        return redirect(userprofile)
    else:
        context = {
            'User':User,
        }
        return render(request, 'User/userprofile.html', context)
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=userlogin)
def servicebooking(request,id):
    User = CustomUser.objects.get(id=request.user.id)
    package = Package.objects.get(id=id)
    booking_data = Booking.objects.filter(package_id=id)
    
    if request.method == 'POST':
        name = request.POST['name']
        date = request.POST['date']
        address = request.POST['address']
        phone =request.POST['phone']
        print(name, address, date)

        user = CustomUser.objects.get(id=request.user.id)
        user_email = user.email

        booking_date = datetime.strptime(date, '%Y-%m-%d').date()

        total_amount = package.price 

        booking = Booking.objects.create(
                                         user_id=User,
                                         package_id=package,
                                         name=name, 
                                         booking_date=booking_date, 
                                         address=address,
                                         phone=phone,
                                         total_amount=total_amount
                                         )                      
        booking.save()
        send_mail("Pickup Pending", f"Your pickup order has been successfully received.\nTo proceed with the next steps, please confirm your payment at your earliest convenience.\nIf you have any questions or need assistance, feel free to contact us.", EMAIL_HOST_USER, [user_email], fail_silently=True)
        return redirect(userviewbookings)
    else:
        context = {
            'package':package,
            'booking_data':booking_data,
            'User':User

        }
        return render(request, 'User/servicebooking.html', context)
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=userlogin)
def userviewbookings(request):
    User = CustomUser.objects.get(id=request.user.id)
    bookings_data = Booking.objects.filter(user_id=User).order_by('-status','-date')
    return render(request, 'User/userviewbookings.html', {'bookings_data':bookings_data, 'User':User})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=userlogin)
def payments(request,id):
    User = CustomUser.objects.get(id=request.user.id)
    booking = Booking.objects.get(id=id)
    if request.method == 'POST':
        payment_status = request.POST['status']
        booking.status = payment_status
        booking.save()
        return redirect(userviewbookings)

    else:    
        return render(request, 'User/payment.html', {'User':User, 'booking':booking})
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=userlogin)
def cancel_booking(request,id):
    bookings_data = Booking.objects.get(id=id)
    if request.method == 'POST':
        bookings_data.status='canceled'
        bookings_data.save()
        return redirect(userviewbookings)
    
    