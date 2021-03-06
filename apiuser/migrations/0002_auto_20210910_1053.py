# Generated by Django 3.2.3 on 2021-09-10 10:53

from django.db import migrations
from apiuser.serializers import UserRegistrationSerializer

def seed_users(apps, schema_editor):
    users =  [
        {'email':'admin@test.com', 'password':'testing', 'first_name':'James', 'last_name':'Cole', 'role':'admin'},
        {'email':'doctor@test.com', 'password':'testing', 'first_name':'Harvey', 'last_name':'Coffie', 'role':'doctor'},
        {'email':'screener@test.com', 'password':'testing', 'first_name':'Lena', 'last_name':'Freya', 'role':'screener'},
        {'email':'manager@test.com', 'password':'testing', 'first_name':'Jay', 'last_name':'Garrick', 'role':'manager'},
        {'email':'dataclerk@test.com', 'password':'testing', 'first_name':'Dent', 'last_name':'Mane', 'role':'dataclerk'},
        {'email':'employee@test.com', 'password':'testing', 'first_name':'John', 'last_name':'Denton', 'role':'employee'},
    ]

    for user in users:
        serializer = UserRegistrationSerializer(data=user)
        serializer.is_valid()
        serializer.save()

class Migration(migrations.Migration):

    dependencies = [
        ('apiuser', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_users),
    ]
