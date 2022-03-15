from django.conf import settings
from django.core.files.storage import get_storage_class
from django.db import models
from django.utils.functional import LazyObject

from easy_thumbnails.fields import ThumbnailerImageField
from django_countries.fields import CountryField
from taggit.managers import TaggableManager


class AvatarStorage(LazyObject):
    def _setup(self):
        AVATAR_FILE_STORAGE = getattr(settings, 'AVATAR_FILE_STORAGE', settings.DEFAULT_FILE_STORAGE)
        self._wrapped = get_storage_class(AVATAR_FILE_STORAGE)()

avatar_storage = AvatarStorage()

ADR_TYPES = (
    ('Home', 'Home'),
    ('Work', 'Work'),
)

TEL_TYPES = (
    ('Mobile', 'Mobile'),
    ('Mobile Work', 'Mobile Work'),
    ('Work', 'Work'),
    ('Fax', 'Fax'),
    ('Skype', 'Skype'),
)

EMAIL_TYPES = (
    ('Home', 'Home'),
    ('Work', 'Work'),
)

WEBSITE_TYPES = (
    ('Work', 'Work'),
    ('Personal', 'Personal'),
    ('Portfolio', 'Portfolio'),
    ('Blog', 'Blog'),
)

SOCNET_TYPES = (
    ('Skype', 'Skype'),
    ('Twitter', 'Twitter'),
    ('LinkedIn', 'LinkedIn'),
    ('Facebook', 'Facebook'),
    ('Pinterest', 'Pinterest'),
)

social_net_prefixes = dict(
    Skype='skype:',
    Twitter='https://twitter.com/',
    LinkedIn='http://linkedin.com/',
    Facebook='http://www.facebook.com/',
    Pinterest='http://www.pinterest.com/',
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
    groups = models.ManyToManyField(ContactGroup)
    last_name = models.CharField(max_length=255, blank=False)
    first_name = models.CharField(max_length=255, blank=False)
    middle_name = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    organization = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True)
    blurb = models.TextField(null=True, blank=True)
    profile_image = ThumbnailerImageField(upload_to="profile_images/", blank=True, null=True)
    qr_image = models.ImageField(upload_to="qr_images/", blank=True, null=True)
    twitter_handle = models.CharField(max_length=15, blank=True, null=True)
    worked_with = models.ManyToManyField('self', blank=True)
    tags = TaggableManager(blank=True,)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(Contact, self).__init__(*args, **kwargs)
        self.profile_image.storage = avatar_storage
        self.profile_image.thumbnail_storage = avatar_storage

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Address(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    street = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = CountryField()
    zip = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, choices=ADR_TYPES)
    public_visible = models.BooleanField(default=False)
    contact_visible = models.BooleanField(default=False)

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
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=TEL_TYPES)
    public_visible = models.BooleanField(default=False)
    contact_visible = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s: %s" % (
            self.contact.first_name,
            self.contact.last_name,
            self.phone
        )


class Email(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    email = models.EmailField()
    type = models.CharField(max_length=255, choices=EMAIL_TYPES)
    public_visible = models.BooleanField(default=False)
    contact_visible = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s: %s" % (
            self.contact.first_name,
            self.contact.last_name,
            self.email
        )


class Website(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    type = models.CharField(max_length=255, choices=WEBSITE_TYPES)
    public_visible = models.BooleanField(default=False)
    contact_visible = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s: %s" % (self.contact.first_name, self.type, self.website)


class SocialNetwork(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    handle = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=SOCNET_TYPES)
    public_visible = models.BooleanField(default=False)
    contact_visible = models.BooleanField(default=False)

    @property
    def url(self):
        prefixes = social_net_prefixes
        prefix = getattr(settings, '%s_PREFIX' % self.type.upper(), prefixes[self.type])
        return '%s%s' % (prefix, self.handle)

    def __str__(self):
        return "%s %s: %s" % (self.contact.first_name, self.type, self.handle)
