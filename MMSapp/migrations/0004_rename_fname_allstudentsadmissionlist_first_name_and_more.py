# Generated by Django 4.2 on 2023-07-26 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MMSapp', '0003_allstudentsadmissionlist_delete_admissionform'),
    ]

    operations = [
        migrations.RenameField(
            model_name='allstudentsadmissionlist',
            old_name='fname',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='allstudentsadmissionlist',
            old_name='lname',
            new_name='last_name',
        ),
    ]
