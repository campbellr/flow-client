import os

from unittest2 import TestCase as _TestCase
import requests

from flow import FlowClient


class TestCase(_TestCase):
    @classmethod
    def setUpClass(cls):
        cls.email = os.environ.get('FLOW_EMAIL')
        cls.password = os.environ.get('FLOW_PASSWORD')
        if not cls.email or not cls.password:
            raise AssertionError("FLOW_EMAIL and FLOW_PASSWORD env "
                                 "variables must be set.")


class TestFlowClient(TestCase):

    def test_login_failure(self):
        client = FlowClient()
        with self.assertRaises(requests.HTTPError):
            client.login('username', 'password')

    def test_login_success(self):
        client = FlowClient()
        client.login(self.email, self.password)

    def test_activities(self):
        client = FlowClient()
        client.login(self.email, self.password)
        activities = client.activities()
        self.assertNotEqual(activities, [])


class TestActivity(TestCase):

    def setUp(self):
        self.client = FlowClient()
        self.client.login(self.email, self.password)
        self.activity = self.client.activities()[0]

    def test_activity_dir(self):
        d = dir(self.activity)
        self.assertIn('session', d)
        self.assertIn('type', d)
        self.assertIn('distance', d)

    def test_activity_getattr(self):
        self.assertIsNotNone(self.activity.distance)

    def test_activity_tcx(self):
        tcx = self.activity.tcx()
        self.assertIsInstance(tcx, str)
        self.assertTrue(tcx.startswith("<?xml"))
