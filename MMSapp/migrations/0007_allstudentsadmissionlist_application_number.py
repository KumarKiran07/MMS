# Generated by Django 4.2 on 2023-07-26 11:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('MMSapp', '0006_alter_allstudentsadmissionlist_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='allstudentsadmissionlist',
            name='application_number',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
