from django.conf import settings
from django.core.files.storage import get_storage_class
from django.db import models
from django.utils.functional import LazyObject
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from easy_thumbnails.fields import ThumbnailerImageField
from django_countries.fields import CountryField
from taggit.managers import TaggableManager
from django.contrib.auth import get_user_model

User = get_user_model()

class AvatarStorage(LazyObject):
    def _setup(self):
        AVATAR_FILE_STORAGE = getattr(
            settings,
            'AVATAR_FILE_STORAGE',
            settings.DEFAULT_FILE_STORAGE
        )
        self._wrapped = get_storage_class(AVATAR_FILE_STORAGE)()

avatar_storage = AvatarStorage()

social_net_prefixes = dict(
    Skype='skype:',
    Twitter='https://twitter.com/',
    LinkedIn='https://linkedin.com/',
    Facebook='https://www.facebook.com/',
    Pinterest='https://www.pinterest.com/',
)


class ContactGroup(models.Model):
    #user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=255, verbose_name='Group Name', unique=True)

    class Meta:
        ordering = ['name']
        #unique_together = ('user', 'name')

    def __str__(self):
        return self.name


class Contact(models.Model):
    
    class PersonType(models.TextChoices):
        NATURAL = 'Natural', _('Natural person')
        LEGAL = 'Legal', _('Legal person')

    person_type = models.CharField(
        max_length=255,
        choices=PersonType.choices,
        default=PersonType.NATURAL,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    groups = models.ManyToManyField(ContactGroup)
    formatted_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    middle_name = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    organization = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True)
    blurb = models.TextField(null=True, blank=True)
    profile_image = ThumbnailerImageField(
        upload_to="profile_images/",
        blank=True,
        null=True
    )
    qr_image = models.ImageField(upload_to="qr_images/", blank=True, null=True)
    twitter_handle = models.CharField(max_length=15, blank=True, null=True)
    worked_with = models.ManyToManyField('self', blank=True)
    tags = TaggableManager(blank=True,)

    class Meta:
        ordering = ['formatted_name', 'last_name', 'first_name']

    def __init__(self, *args, **kwargs):
        super(Contact, self).__init__(*args, **kwargs)
        self.profile_image.storage = avatar_storage
        self.profile_image.thumbnail_storage = avatar_storage

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Address(models.Model):

    class AddressType(models.TextChoices):
        HOME = 'Home', _('Home')
        WORK = 'Work', _('Work')

    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name="addresses",
    )
    street = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = CountryField()
    zip = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, choices=AddressType.choices)
    public_visible = models.BooleanField(default=False)
    contact_visible = models.BooleanField(default=False)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=7,
        null=True,
        blank=True,
    )
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True,
    )
    zoom = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(21)
        ]
    )

    def __str__(self):
        return '%s %s: %s %s, %s, %s' % (
            self.contact.first_name,
            self.contact.last_name,
            self.street,
            self.city,
            self.state,
            self.country
        )


class PhoneNumber(models.Model):
    
    class TelephoneType(models.TextChoices):
        MOBILE = 'M', _('Mobile')
        MOBILE_WORK = 'MW', _('Mobile Work')
        WORK = 'W', _('Work')
        FAX = 'F', _('Fax')
        SKYPE = 'S', _('Skype')
        ANSWERING_SERVICE = 'AS', _('Answering service')

    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name="phonenumbers"
    )
    phone = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=TelephoneType.choices)
    public_visible = models.BooleanField(default=False)
    contact_visible = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s: %s" % (
            self.contact.first_name,
            self.contact.last_name,
            self.phone
        )


class Email(models.Model):
    
    class EmailType(models.TextChoices):
        PERSONAL = 'P', _('Personal')
        WORK = 'W', _('Work')

    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name="emails",
    )
    email = models.EmailField()
    type = models.CharField(max_length=255, choices=EmailType.choices)
    public_visible = models.BooleanField(default=False)
    contact_visible = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s: %s" % (
            self.contact.first_name,
            self.contact.last_name,
            self.email
        )


class Website(models.Model):
    
    class WebsiteType(models.TextChoices):
        WORK = 'W', _('Work')
        PERSONAL = 'PE', _('Personal')
        PORTFOLIO = 'PO', _('Portfolio')
        BLOG = 'Blog', _('Blog')

    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name="websites",
    )
    website = models.URLField(blank=True)
    type = models.CharField(max_length=255, choices=WebsiteType.choices)
    public_visible = models.BooleanField(default=False)
    contact_visible = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s: %s" % (self.contact.first_name, self.type, self.website)


class SocialNetwork(models.Model):
    
    class SocialNetworkType(models.TextChoices):
        SKYPE = 'S', 'Skype'
        TWITTER = 'T', 'Twitter'
        LINKEDIN = 'LI', 'LinkedIn'
        FACEBOOK = 'F', 'Facebook'
        PINTEREST = 'P', 'Pinterest'

    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name="socialnetworks",
    )
    handle = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=SocialNetworkType.choices)
    public_visible = models.BooleanField(default=False)
    contact_visible = models.BooleanField(default=False)

    @property
    def url(self):
        prefixes = social_net_prefixes
        prefix = getattr(settings, '%s_PREFIX' % self.type.upper(), prefixes[self.type])
        return '%s%s' % (prefix, self.handle)

    def __str__(self):
        return "%s %s: %s" % (self.contact.first_name, self.type, self.handle)
