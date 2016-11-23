import os, string, random
from django.conf import settings as django_settings
from django.utils.deconstruct import deconstructible
from django.db import models

############################################################
# Internal Utils

def tourldash(string):
    s =  u''.join(e if e.isalnum() else u'-' for e in string)
    return u'-'.join([s for s in s.split(u'-') if s])

def randomString(length, choice=(string.ascii_letters + string.digits)):
        return ''.join(random.SystemRandom().choice(choice) for _ in range(length))

@deconstructible
class uploadImage(object):
    def __init__(self, prefix, length=30):
        self.prefix = prefix
        self.length = length

    def __call__(self, instance, filename):
        _, extension = os.path.splitext(filename)
        if not extension:
            extension = '.png'
        return u'{static_uploaded_files_prefix}{prefix}/{id}{string}{random}{extension}'.format(
            static_uploaded_files_prefix=django_settings.STATIC_UPLOADED_FILES_PREFIX,
            prefix=self.prefix,
            id=instance.id if instance.id else '',
            string=tourldash(unicode(instance)),
            random=randomString(4),
            extension=extension,
        )

def get_image_url(imagePath):
    if not imagePath:
        return None
    imageURL = unicode(imagePath)
    if '//' in imageURL:
        return imageURL
    if imageURL.startswith('web'):
        imageURL = imageURL.replace('web', '', 1)
    return u'{}{}'.format(django_settings.STATIC_FULL_URL, imageURL)

############################################################
# Models

class SocialLink(models.Model):
    image = models.ImageField(upload_to=uploadImage(prefix='s'))
    url = models.CharField(max_length=500)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=400, blank=True)
    importance = models.PositiveIntegerField(default=1)
    small = models.BooleanField(default=False)

    @property
    def image_url(self):
        return get_image_url(self.image)

    def __unicode__(self):
        return self.name

class Stat(models.Model):
    name = models.CharField(max_length=40)
    value = models.CharField(max_length=40)

    def __unicode__(self):
        return u'{}: {}'.format(self.name, self.value)

class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class Project(models.Model):
    image = models.ImageField(upload_to=uploadImage(prefix='p'))
    name = models.CharField(max_length=200)
    beginning = models.DateField()
    end = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    description = models.TextField()
    stats = models.ManyToManyField(Stat)
    tags = models.ManyToManyField(Tag)
    url = models.CharField(max_length=500, blank=True)
    source_code_url = models.CharField(max_length=500, blank=True)
    screenshot1 = models.ImageField(upload_to=uploadImage(prefix='p/s'), null=True)
    screenshot2 = models.ImageField(upload_to=uploadImage(prefix='p/s'), null=True)
    screenshot3 = models.ImageField(upload_to=uploadImage(prefix='p/s'), null=True)
    small = models.BooleanField(default=True)
    color = models.CharField(max_length=32, blank=True)

    @property
    def image_url(self):
        return get_image_url(self.image)

    @property
    def screenshot1_url(self):
        return get_image_url(self.screenshot1)

    @property
    def screenshot2_url(self):
        return get_image_url(self.screenshot2)

    @property
    def screenshot3_url(self):
        return get_image_url(self.screenshot3)

    @property
    def web_url(self):
        return u'/project/{id}/{name}/'.format(
            id=self.id,
            name=tourldash(unicode(self)),
        )

    def __unicode__(self):
        return self.name
