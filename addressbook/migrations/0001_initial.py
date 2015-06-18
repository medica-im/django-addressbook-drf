# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_localflavor_us.models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('street', models.CharField(max_length=b'50')),
                ('city', models.CharField(max_length=b'40')),
                ('state', django_localflavor_us.models.USStateField(max_length=2, choices=[(b'AL', b'Alabama'), (b'AK', b'Alaska'), (b'AS', b'American Samoa'), (b'AZ', b'Arizona'), (b'AR', b'Arkansas'), (b'AA', b'Armed Forces Americas'), (b'AE', b'Armed Forces Europe'), (b'AP', b'Armed Forces Pacific'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DE', b'Delaware'), (b'DC', b'District of Columbia'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'GU', b'Guam'), (b'HI', b'Hawaii'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'IA', b'Iowa'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'ME', b'Maine'), (b'MD', b'Maryland'), (b'MA', b'Massachusetts'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MS', b'Mississippi'), (b'MO', b'Missouri'), (b'MT', b'Montana'), (b'NE', b'Nebraska'), (b'NV', b'Nevada'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NY', b'New York'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'MP', b'Northern Mariana Islands'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'PR', b'Puerto Rico'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VT', b'Vermont'), (b'VI', b'Virgin Islands'), (b'VA', b'Virginia'), (b'WA', b'Washington'), (b'WV', b'West Virginia'), (b'WI', b'Wisconsin'), (b'WY', b'Wyoming')])),
                ('zip', models.CharField(max_length=b'10')),
                ('type', models.CharField(max_length=b'20', choices=[(b'Home', b'Home'), (b'Work', b'Work')])),
                ('public_visible', models.BooleanField(default=False)),
                ('contact_visible', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_name', models.CharField(max_length=b'40')),
                ('first_name', models.CharField(max_length=b'40')),
                ('middle_name', models.CharField(max_length=b'40', blank=True)),
                ('title', models.CharField(max_length=b'40', blank=True)),
                ('organization', models.CharField(max_length=b'50', blank=True)),
                ('url', models.URLField(blank=True)),
                ('blurb', models.TextField(null=True, blank=True)),
                ('profile_image', easy_thumbnails.fields.ThumbnailerImageField(null=True, upload_to=b'profile_images/', blank=True)),
                ('qr_image', models.ImageField(null=True, upload_to=b'qr_images/', blank=True)),
                ('twitter_handle', models.CharField(max_length=b'50', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContactGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=b'40', verbose_name=b'Group Name')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('type', models.CharField(max_length=b'20', choices=[(b'Home', b'Home'), (b'Work', b'Work')])),
                ('public_visible', models.BooleanField(default=False)),
                ('contact_visible', models.BooleanField(default=False)),
                ('contact', models.ForeignKey(to='addressbook.Contact')),
            ],
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=b'20')),
                ('type', models.CharField(max_length=b'20', choices=[(b'Mobile', b'Mobile'), (b'Work', b'Work'), (b'Fax', b'Fax'), (b'Skype', b'Skype')])),
                ('public_visible', models.BooleanField(default=False)),
                ('contact_visible', models.BooleanField(default=False)),
                ('contact', models.ForeignKey(to='addressbook.Contact')),
            ],
        ),
        migrations.CreateModel(
            name='SocialNetwork',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('handle', models.CharField(max_length=b'50')),
                ('type', models.CharField(max_length=b'20', choices=[(b'Skype', b'Skype'), (b'Twitter', b'Twitter'), (b'LinkedIn', b'LinkedIn'), (b'Facebook', b'Facebook'), (b'Pinterest', b'Pinterest')])),
                ('public_visible', models.BooleanField(default=False)),
                ('contact_visible', models.BooleanField(default=False)),
                ('contact', models.ForeignKey(to='addressbook.Contact')),
            ],
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('website', models.URLField(blank=True)),
                ('type', models.CharField(max_length=b'20', choices=[(b'Work', b'Work'), (b'Personal', b'Personal'), (b'Portfolio', b'Portfolio'), (b'Blog', b'Blog')])),
                ('public_visible', models.BooleanField(default=False)),
                ('contact_visible', models.BooleanField(default=False)),
                ('contact', models.ForeignKey(to='addressbook.Contact')),
            ],
        ),
        migrations.AddField(
            model_name='contact',
            name='group',
            field=models.ForeignKey(to='addressbook.ContactGroup'),
        ),
        migrations.AddField(
            model_name='address',
            name='contact',
            field=models.ForeignKey(to='addressbook.Contact'),
        ),
        migrations.AlterUniqueTogether(
            name='contactgroup',
            unique_together=set([('user', 'name')]),
        ),
    ]
