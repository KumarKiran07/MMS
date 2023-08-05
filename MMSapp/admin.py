from django.contrib import admin

from MMSapp.models import Students, Admin, Inquiry, Contact, Allstudentsadmissionlist

admin.site.register(Students)

admin.site.register(Admin)

admin.site.register(Allstudentsadmissionlist)

admin.site.register(Inquiry)

admin.site.register(Contact)
# Register your models here.
