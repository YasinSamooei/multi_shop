# Generated by Django 3.2.12 on 2022-09-03 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, unique=True, verbose_name='email-adress')),
                ('full_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='fullname')),
                ('username', models.CharField(blank=True, max_length=50, null=True, verbose_name='username')),
                ('is_active', models.BooleanField(default=True, verbose_name='active-user')),
                ('is_admin', models.BooleanField(default=False, verbose_name='admin')),
                ('phone', models.CharField(max_length=11, unique=True, verbose_name='phone-number')),
                ('image', models.ImageField(blank=True, null=True, upload_to='profiles/images', verbose_name='تصویر')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='Otp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=32)),
                ('phone', models.CharField(max_length=11)),
                ('code', models.SmallIntegerField()),
                ('expiration_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'optcode',
                'verbose_name_plural': 'optcodes',
            },
        ),
    ]
