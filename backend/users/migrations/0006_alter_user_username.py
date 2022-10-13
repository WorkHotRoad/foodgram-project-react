# Generated by Django 4.1.2 on 2022-10-13 10:17

import django.core.validators
from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+\\Z', message='Password should be a combination of Alphabets and Numbers'), users.validators.validate_username]),
        ),
    ]