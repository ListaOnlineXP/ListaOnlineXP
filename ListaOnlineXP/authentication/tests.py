#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase
from models import  Profile
from django.contrib.auth.models import User


class AuthenticationTestCase(TestCase):
    
    def setUp(self):
        self.user1 = User.objects.create(
            first_name="Steven",
            last_name="Koiti Tsukamoto",
            username=u"koiti",
            password=u"lalala"
        )
        self.user2 = User.objects.create(
            first_name="Thiago",
            last_name="da Silva Pinheiro",
            username=u"tsp",
            password=u"weasd"
        )
        self.user3 = User.objects.create(
            first_name="Bruno",
            last_name="Milan Perfetto",
            username=u"milan",
            password=u"1234"
        )
        self.profile1 = Profile.objects.create(
            user=User.objects.get(id=1)
        )
        self.profile2 = Profile.objects.create(
            user=User.objects.get(id=2)
        )
        self.profile3 = Profile.objects.create(
            user=User.objects.get(id=3)
        )
        
    def testStudentDB(self):
        self.assertEqual(
            Profile.objects.get(id=u'3').user.first_name,
            u"Bruno"
        )
        self.assertEqual(Profile.objects.count(), 3)
