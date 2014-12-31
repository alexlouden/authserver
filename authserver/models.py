import logging

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models
from jsonfield import JSONField


logger = logging.getLogger(__name__)


class BaseModel(models.Model):
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        abstract = True
        get_latest_by = "created"


class UserManager(DjangoUserManager):

    def create_user(self, name, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            name=name,
            email=UserManager.normalize_email(email),
        )
        user.set_password(password)
        user.save()
        return user

    def get_by_natural_key(self, username):
        return self.get(email__iexact=username)


class User(BaseModel, AbstractBaseUser):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True, db_index=True)

    locale = models.CharField(max_length=5, blank=True, default='en_US')
    timezone = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    data = JSONField()

    roles = models.ManyToManyField('Role')

    objects = UserManager()

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'{0.id} {0.name!r}'.format(self)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    @property
    def is_admin(self):
        return self.has_role('admin')

    @is_admin.setter
    def is_admin(self, value):
        return self.add_role('admin')

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    def has_role(self, role_name):
        return self.roles.filter(name=role_name).exists()

    def add_role(self, role_name):
        if self.has_role(role_name):
            return False

        try:
            role, created = Role.objects.get_or_create(name=role_name)
            self.roles.add(role)
            return True
        except:
            return False

    def remove_role(self, role_name):

        if not self.has_role(role_name):
            return False

        role = Role.object.get(name=role_name)
        self.roles.remove(role)
        return True


class Role(BaseModel):

    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class APIKey(BaseModel):

    user = models.ForeignKey(User, related_name='keys')

    key = models.CharField(max_length=64)
    secret = models.CharField(max_length=64)

    def __unicode__(self):
        return self.key

    class Meta:
        ordering = ('key',)
