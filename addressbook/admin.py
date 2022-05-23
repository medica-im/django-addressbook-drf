from django.contrib import admin
from django import forms
from taggit_labels.widgets import LabelWidget
from taggit.forms import TagField
from addressbook.models import *

class SocialInline(admin.TabularInline):
    model = SocialNetwork
    extra = 0

class WebsiteInline(admin.TabularInline):
    model = Website
    extra = 0

class PhoneInline(admin.TabularInline):
    model = PhoneNumber
    extra = 0

class EmailInline(admin.TabularInline):
    model = Email
    extra = 0

class AddressInline(admin.StackedInline):
    model = Address
    extra = 0



#class ContactForm(forms.ModelForm):
#    tags = TagField(required=False, widget=LabelWidget)

class ContactAdmin(admin.ModelAdmin):
    #form = ContactForm
    list_display = (
        'formatted_name',
        'last_name',
        'first_name',
        'middle_name',
        'title',
        'person_type',
        'organization',
        'user',
        'profile_image',
    )
    autocomplete_fields = ['user']
    inlines = [
        AddressInline,
        EmailInline,
        PhoneInline,
        SocialInline,
        WebsiteInline,
    ]

admin.site.register(Contact, ContactAdmin)

admin.site.register(ContactGroup, admin.ModelAdmin)
admin.site.register(PhoneNumber, admin.ModelAdmin)
admin.site.register(Website, admin.ModelAdmin)
admin.site.register(SocialNetwork, admin.ModelAdmin)
admin.site.register(Email, admin.ModelAdmin)
admin.site.register(Address, admin.ModelAdmin)
