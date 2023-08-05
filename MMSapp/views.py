import os
from django.shortcuts import render

import datetime
from hashlib import sha256
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.template.loader import get_template
# from Crud_p.form import ImageForm
from .models import  Inquiry, Students, Admin, Contact, Allstudentsadmissionlist
from django.contrib.auth.models import User
import csv

from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from MMS import settings 
from django.template.loader import render_to_string 
from . tokens import generate_token
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from xhtml2pdf import pisa


# Create your views here.



def home(request):
    std = Students.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        number = request.POST['number']
        subject = request.POST['subject']
        
        s = Inquiry()
        
        s.name = name
        s.email = email
        s.number = number
        s.subject = subject
        
        s.save()
        
        messages.success(request, "Thank you for Inquiry")
        return redirect('/')
    return render(request, "crud/index5.html", {'std' :std})

def addstudent(request):
    
    if request.method == "POST":
        roll = request.POST['roll']
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']  
        
        
        
        if Students.objects.filter(roll=roll):
            messages.error(request, " Roll number is already inserted.")
            return redirect('addstudent')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Inserted!!")
            return redirect('addstudent')
        
        if Students.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number Already Inserted!!")
            return redirect('addstudent')
        
        s = Students()
        
        s.roll = roll 
        s.name = name
        s.email = email
        s.address = address
        s.phone = phone
        s.save()
        messages.success(request, " your data has been inserted successfully!")
    
    return render(request, "Admin_panel/addstudent.html")

def delete_std(request, roll):
    s= Students.objects.get(pk=roll)
    s.delete()
    messages.success(request," Data has been deleted!")
    return HttpResponseRedirect(reverse('adminpanel'))

def edit(request, roll):
    std= Students.objects.get(pk=roll)
    # return HttpResponseRedirect(reverse('edit',{'std':std}))
    return render(request, "crud/edit.html",{'std':std})

def updaterecord(request, id):
    if request.method == "POST":
        roll=request.POST.get("roll")
        name=request.POST.get("name")
        email=request.POST.get("email")
        address=request.POST.get("address")
        phone=request.POST.get("phone")
        
        if Students.objects.filter(roll=roll):
            messages.error(request, " Roll number is already inserted.")
            return redirect('addstudent')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Inserted!!")
            return redirect('adminpanel')

        s = Students(
            id = id,
            roll = roll,
            name = name,
            email = email,
            address = address,
            phone = phone
        )
    
    s.save()
    return HttpResponseRedirect(reverse('adminpanel'))
    # return redirect("home")
    
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
        
    writer = csv.writer(response)
    writer.writerow(['id','roll','name','email','address','phone'])
    
    for student in Students.objects.all().values_list('id','roll','name','email','address','phone'):
       writer.writerow(student)
    response['content-Disposition'] = 'attachment; filename=Students.csv'
        
    return response


def adminpanel(request):
    if request.session.has_key('Admin'):
        return redirect(home)
    if request.session.has_key('adminpanel'):  
        if request.session.has_key('deleterr'):
            messages.error(request, 'no such user to delete!') 
            del request.session['deleterr']
        if request.session.has_key('deletesucc'):
            messages.success(request, 'User deleted successfully!')   
            del request.session['deletesucc']    
        if request.session.has_key('updateuser'):
            messages.success(request, 'User updated successfully!')   
            del request.session['updateuser']
        if request.session.has_key('createuser'):
            messages.success(request, 'User added successfully!')   
            del request.session['createuser']   
        if request.session.has_key('searchuser'):
            messages.error(request, 'No such user!')   
            del request.session['searchuser']   
        std = Students.objects.all()
        msg = Allstudentsadmissionlist.objects.all().count()
        return render(request, 'Admin_panel/index.html', {'std': std, 'msg':msg})
        
    elif request.POST:
            usern = request.POST.get('username')
            passw = request.POST.get('password')
            # passwenc = sha256(passw.encode())
            admins = Admin.objects.filter(username=usern,password=passw)
            if admins:
                request.session['adminpanel'] = 1
                return redirect(adminpanel)
            else:    
                return render(request, 'crud/admin-login.html', {'error': 'Invalid credentials!'})      
    else:    
        return render(request, 'crud/admin-login.html')    
    
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
def adminlogout(request):
    request.session.flush()
    messages.success(request, "Logged Out Successfully!!")
    return redirect(adminpanel)




# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         pass1 = request.POST['pass1']
        
#         user = authenticate(username=username, password=pass1)
        
#         if user is not None:
#             dj_login(request, user)
#             fname = user.first_name
#             return render(request, "crud/home.html",{"fname":fname})
#         else:
#             messages.error(request, "Bad Credentials!!")
#             return redirect('login')
    
#     return render(request, "crud/login.html")

  

# def signup(request):
    
#     if request.method == "POST":
#         username = request.POST['username']
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         email = request.POST['email']
#         pass1 = request.POST['pass1']
#         pass2 = request.POST['pass2']     
        
#         if User.objects.filter(username = username):
#             messages.error(request," Username already exist! please try some other username")
#             return redirect('signup')
        
#         if User.objects.filter(email = email):
#             messages.error(request," Email already registered!")
#             return redirect('signup')
        
#         if len(username)>10:
#             messages.error(request," Username must be under 10 character")
        
#         if pass1 != pass2:
#             messages.error(request," Passwords do not match")
        
#         if not username.isalnum():
#             messages.error(request," username must be alpha-Numeric!")
#             return redirect('signup')        
        
#         myuser = User.objects.create_user(username, email, pass1)
#         myuser.first_name = fname
#         myuser.last_name = lname
#         # myuser.is_active = False
#         myuser.is_active = False
#         myuser.save()
               
#         messages.success(request, "your account has been successfully created! we have sent you a confirmation email, please cofirm your email in order to activeate your account.")

#         subject = "welcome to digital art collection!"
#         message = "hello" + myuser.first_name + "!! \n"+ "welcome to DAC \n Thank you for visiting our website \n We have also sent you a confiramtion email, please confirm your email address in order to activeate your acccount. \n\n thank you "
#         from_email = settings.EMAIL_HOST_USER
#         recipient_list = [myuser.email]
#         send_mail(subject, message, from_email, recipient_list, fail_silently = True)
        
#         #email address confirmation email
#         current_site = get_current_si email_subject = "Confirm your Email @ GFte(request)
#        G - Django Login!!"
#         message2 = render_to_string('email_confirmation.html',{
            
#             'name': myuser.first_name,
#             'domain': current_site.domain,
#             'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
#             'token': generate_token.make_token(myuser)
#         })
#         email = EmailMessage( 
#             email_subject,
#             message2,
#             settings.EMAIL_HOST_USER,
#             [myuser.email],
#             )
#         email.fail_silently = True
#         email.send()
#         return redirect('login')
    
#     return render(request, "crud/signup.html")

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('SignIn')
    else:
        return render(request,'activation_failed.html')

def tables_data(request):
    std = Students.objects.all()
    return render(request,"Admin_panel/tables-data.html", {'std' :std})

def users_profile(request):
    
    return render(request,"Admin_panel/users_profile.html")

def admissionList(request):
    std = Allstudentsadmissionlist.objects.all()
    return render(request,"Admin_panel/admissionList.html",{'std':std})

def about(request):
    return render(request,"crud/about.html")

def contact(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        phone = request.POST['phone']
        email = request.POST['email']
        message = request.POST['message'] 
        
        s = Contact()
        
        s.fname = fname
        s.lname = lname
        s.phone = phone
        s.email = email
        s.message = message
        s.save()
        messages.success(request, "Thank You for feedback")
        return redirect('contact')    
    return render(request,"crud/contact.html")

def blog(request):
    return render(request,"crud/blog.html")

def blogdetails(request):
    return render(request,"crud/blogdetails.html")

def coursedetails(request):
    return render(request,"crud/coursedetails.html")

def teachersingle(request):
    return render(request,"crud/teacherssingle.html")

def teacherswithoutfilter(request):
    return render(request,"crud/teacherswithoutfilter.html")

def gallery3(request):
    return render(request,"crud/gallery3.html")

def teachers(request):
    return render(request,"crud/teachers.html")

def modal(request):
    return render(request,"crud/modal.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def logout_view(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('SignIn') 
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def SignIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(request, username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('SignIn')
    else:    
        return render(request,"crud/SignIn.html")

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']     
        
        if User.objects.filter(username = username):
            messages.error(request," Username already exist! please try some other username")
            return redirect('register')
        
        if username != fname:
            messages.error(request,"The username and first name are not the same!")
            messages.error(request,"Username and first name must be the same.")
            return redirect('register')
        
        
        if User.objects.filter(email = email):
            messages.error(request," Email already registered!")
            return redirect('register')
        
        if len(username)>10:
            messages.error(request," Username must be under 10 character")
            return redirect('register')
        
        if pass1 != pass2:
            messages.error(request," Passwords do not match")
            return redirect('register')
        
        if not username.isalnum():
            messages.error(request," username must be alpha-Numeric!")
            return redirect('register')        
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
               
        messages.success(request, "your account has been successfully created! we have sent you a confirmation email, please cofirm your email in order to activeate your account.")

        subject = "welcome to digital art collection!"
        message = "hello" + myuser.first_name + "!! \n"+ "welcome to DAC \n Thank you for visiting our website \n We have also sent you a confiramtion email, please confirm your email address in order to activeate your acccount. \n\n thank you "
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [myuser.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently = True)
        
        #email address confirmation email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ GFG - Django Login!!"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage( 
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
            )
        email.fail_silently = True
        email.send()
        return redirect('SignIn')
    return render(request,"crud/register.html")
    

def country(request):
    return render(request,"crud/country.html")

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
        
    writer = csv.writer(response)
    writer.writerow(['image','first_name','last_name','fathername','mothername','Permanent_Address','country','state','city','pincode','email','Snumber','Gnumber','DOB','Religion','gender','category','course','SSCyear','SSCBoard','t1','m1','p1','HSCyear','HSCboard','t2','m2','p2','graduationYear','Collegename','t3','m3','p3','HSCstream','application_number','application_number_integer'])
    
    for student in Allstudentsadmissionlist.objects.all().values_list('image','first_name','last_name','fathername','mothername','Permanent_Address','country','state','city','pincode','email','Snumber','Gnumber','DOB','Religion','gender','category','course','SSCyear','SSCBoard','t1','m1','p1','HSCyear','HSCboard','t2','m2','p2','graduationYear','Collegename','t3','m3','p3','HSCstream','application_number','application_number_integer'):
       writer.writerow(student)
    response['content-Disposition'] = 'attachment; filename=AdmissionList.csv'
        
    return response

def delete_Al(request, image):
    s= Allstudentsadmissionlist.objects.get(pk=image)
    s.delete()
    messages.success(request," Data has been deleted!")
    return HttpResponseRedirect(reverse('admissionList'))
   


@login_required(login_url="/crud/SignIn")
def dashboard(request):
    user = User.objects.get(username=request.user.username)
    admission_form = Allstudentsadmissionlist.objects.filter(first_name=user).first()
    
    if admission_form:
        return render(request, "crud/admissionformPdf.html")
     
    else:
            if request.method == "POST":
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                fathername = request.POST.get('fathername')
                mothername = request.POST.get('mothername')
                Permanent_Address = request.POST.get('Permanent_Address')
                country = request.POST.get('country')
                state = request.POST.get('state')
                city = request.POST.get('city')
                pincode = request.POST.get('pincode')
                email = request.POST.get('email')
                Snumber = request.POST.get('Snumber')
                Gnumber = request.POST.get('Gnumber')
                DOB = request.POST.get('DOB')
                Religion = request.POST.get('Religion')
                gender = request.POST.get('gender')
                category = request.POST.get('category')
                course = request.POST.get('course')
                SSCyear = request.POST.get('SSCyear')
                SSCBoard = request.POST.get('SSCBoard')
                t1 = request.POST.get('t1')
                m1 = request.POST.get('m1')
                p1 = request.POST.get('p1')
                HSCyear = request.POST.get('HSCyear')
                HSCboard = request.POST.get('HSCboard')
                t2 = request.POST.get('t2')
                m2 = request.POST.get('m2')
                p2 = request.POST.get('p2')
                graduationYear = request.POST.get('graduationYear')
                Collegename = request.POST.get('Collegename')
                t3 = request.POST.get('t3')
                m3 = request.POST.get('m3')
                p3 = request.POST.get('p3')
                HSCstream = request.POST.get('HSCstream')
                image = request.FILES['image']
                image.name = image.name
        
                student = Allstudentsadmissionlist.objects.create(
                    image = image,
                    first_name = first_name,
                    last_name = last_name,
                    fathername = fathername,
                    mothername = mothername,
                    Permanent_Address = Permanent_Address,
                    country = country,
                    state = state,
                    city = city,
                    pincode = pincode,
                    email = email,
                    Snumber = Snumber,
                    Gnumber = Gnumber,
                    DOB = DOB,
                    Religion = Religion,
                    gender = gender,
                    category = category,
                    course = course,
                    SSCyear = SSCyear,
                    SSCBoard = SSCBoard,
                    t1 = t1,
                    m1 = m1,
                    p1 = p1,
                    HSCyear = HSCyear,
                    HSCboard = HSCboard,
                    t2 = t2,
                    m2 = m2,
                    p2 = p2,
                    graduationYear = graduationYear,
                    Collegename = Collegename,
                    t3 = t3,
                    m3 = m3,
                    p3 = p3,
                    HSCstream = HSCstream,  
                )
                application_number_integer = student.application_number_integer
                student.save()
                
                subject = "Admission Confirmation Letter"
                message = "Dear " + student.first_name + "!! \n"+ "\n\nCongratulations! We are delighted to inform you that your admission has been confirmed for the" + student.course +" at Matriculate Management System . We are thrilled to welcome you to our institution and are looking forward to having you as a part of our community.\n \n Details : \n\n -> Application Number : "+ str(student.application_number_integer) + "\n -> Course : "+ student.course +" \n -> Orientation Date : 15/08/2023 \n -> Timings : 09:00 AM \n \nPlease make sure to bring all the required documents and fees on the orientation day. If you have any questions or need further information, please don't hesitate to reach out to our admissions office at MMS@gmail.com or 8905519839.\n \nOnce again, congratulations on your admission! We are confident that you will have a successful and enriching academic journey at Matriculate Management System. \n\n\n\n Thank You!"
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [student.email]
                send_mail(subject, message, from_email, recipient_list, fail_silently = True)
                
                return redirect('Student_admission_Pdf', application_number_integer=student.application_number_integer)   
    return render(request,'crud/dashboard.html')
    
@csrf_exempt
def payment(request):
    std = Allstudentsadmissionlist.objects.all()
    return render(request, "crud/payment.html",{'std':std})

def AdmissionformPdf(request):    
        
    return render(request,"crud/admissionformPdf.html")


 
def Student_admission_Pdf(request,application_number_integer):
        try:
            admission_form = Allstudentsadmissionlist.objects.get(application_number_integer=application_number_integer)
        except Allstudentsadmissionlist.DoesNotExist:
            return HttpResponse('Form not found.')

        # image_url = admission_form.image.url if admission_form.image else os.path.join(settings.MEDIA_ROOT, 'default_student_image.jpg')
        # Context data to pass to the template
        context = {'admission_form': admission_form}

        # Create a PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename="admission_form_{application_number_integer}.pdf"'
        template = render(request, 'crud/StudentadmissionPdf.html', context)

        # Generate the PDF using xhtml2pdf
        pisa_status = pisa.CreatePDF(template.content, dest=response)
        if pisa_status.err:
            return HttpResponse('PDF generation failed.')
        return response    
    # return render(request,"crud/Student_admission_Pdf.html")
    
def pdf(request):
    if request.method == 'POST':
        application_number_integer = request.POST.get('application_number_integer')
        return redirect('Student_admission_Pdf', application_number_integer=application_number_integer)

def re_generate(request,application_number): 
        try:
            admission_form = Allstudentsadmissionlist.objects.get(application_number=application_number)
        except Allstudentsadmissionlist.DoesNotExist:
            return HttpResponse('Form not found.')

        # Context data to pass to the template
        context = {'admission_form': admission_form,}

        # Create a PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename="admission_form_{application_number}.pdf"'
        template = render(request, 'crud/StudentadmissionPdf.html', context)

        # Generate the PDF using xhtml2pdf
        pisa_status = pisa.CreatePDF(template.content, dest=response)
        if pisa_status.err:
            return HttpResponse('PDF generation failed.')
        return response  