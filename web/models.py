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
class uploadFile(object):
    def __init__(self, prefix, length=30):
        self.prefix = prefix
        self.length = length

    def __call__(self, instance, filename):
        _, extension = os.path.splitext(filename)
        return u'{static_uploaded_files_prefix}{prefix}/{id}{string}{random}{extension}'.format(
            static_uploaded_files_prefix=django_settings.STATIC_UPLOADED_FILES_PREFIX,
            prefix=self.prefix,
            id=instance.id if instance.id else '',
            string=tourldash(unicode(instance)),
            random=randomString(4),
            extension=extension if extension else '',
        )

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

def get_file_url(filePath):
    if not filePath:
        return None
    fileURL = unicode(filePath)
    if '//' in fileURL:
        return fileURL
    if fileURL.startswith('web'):
        fileURL = fileURL.replace('web', '', 1)
    return u'{}{}'.format(django_settings.STATIC_FULL_URL, fileURL)

############################################################
# Models

class SocialTag(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class SocialLink(models.Model):
    image = models.ImageField(upload_to=uploadImage(prefix='s'))
    url = models.CharField(max_length=500)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=400, blank=True)
    importance = models.PositiveIntegerField(default=1)
    small = models.BooleanField(default=False)
    tags = models.ManyToManyField(SocialTag)

    @property
    def image_url(self):
        return get_file_url(self.image)

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
    image = models.ImageField(upload_to=uploadImage(prefix='p'), blank=True, null=True)
    name = models.CharField(max_length=200)
    beginning = models.DateField()
    end = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    description = models.TextField()
    stats = models.ManyToManyField(Stat)
    tags = models.ManyToManyField(Tag)
    url = models.CharField(max_length=500, blank=True)
    source_code_url = models.CharField(max_length=500, blank=True)
    screenshot1 = models.ImageField(upload_to=uploadImage(prefix='p/s'), null=True, blank=True)
    screenshot2 = models.ImageField(upload_to=uploadImage(prefix='p/s'), null=True, blank=True)
    screenshot3 = models.ImageField(upload_to=uploadImage(prefix='p/s'), null=True, blank=True)
    small = models.BooleanField(default=True)
    color = models.CharField(max_length=32, blank=True)

    @property
    def image_url(self):
        return get_file_url(self.image)

    @property
    def screenshot1_url(self):
        return get_file_url(self.screenshot1)

    @property
    def screenshot2_url(self):
        return get_file_url(self.screenshot2)

    @property
    def screenshot3_url(self):
        return get_file_url(self.screenshot3)

    @property
    def web_url(self):
        return u'/project/{id}/{name}/'.format(
            id=self.id,
            name=tourldash(unicode(self)),
        )

    def __unicode__(self):
        return self.name

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    importance = models.PositiveIntegerField(default=50)

    def __unicode__(self):
        return '{} ({})'.format(self.question, self.importance)

class PublicTag(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class Public(models.Model):
    creation = models.DateTimeField(auto_now_add=True)
    modification = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    tags = models.ManyToManyField(PublicTag)
    image = models.ImageField(upload_to=uploadImage(prefix='p'), null=True, blank=True)
    file = models.FileField(upload_to=uploadFile(prefix='pf'), null=True, blank=True)
    url = models.CharField(max_length=500, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    text_markdown = models.BooleanField(default=True)
    private = models.BooleanField(default=False)

    @property
    def image_url(self):
        return get_file_url(self.image)

    @property
    def file_url(self):
        return get_file_url(self.file)

    def __unicode__(self):
        return self.name
