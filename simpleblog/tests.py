# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

# from django.test import TestCase

# class SimpleTest(TestCase):
#     def test_basic_addition(self):
#         """
#         Tests that 1 + 1 always equals 2.
#         """
#         self.assertEqual(1 + 1, 2)

from django.utils import unittest
from simpleblog.models import Entry

class AnimalTestCase(unittest.TestCase):
    def setUp(self):
        self.entry1 = Entry(title="Sample Entry1", content="bla bla bla bla bla").put()
        self.entry2 = Entry(title="Sample Entry2", content="ble ble ble ble ble").put()

    def test_consistency(self):
        """Should be the same as when created"""
        self.assertEqual(self.entry1.title, 'Sample Entry1')
        self.assertEqual(self.entry2.title, 'Sample Entry2')