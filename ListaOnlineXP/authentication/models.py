# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

    user = models.OneToOneField(User)

    def is_of_group(self, group_name):
        for group in self.user.groups.all():
            if group.name == group_name:
                return True
        return False

    def is_teacher(self):
        return self.is_of_group('Teacher')

    def __unicode__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)
