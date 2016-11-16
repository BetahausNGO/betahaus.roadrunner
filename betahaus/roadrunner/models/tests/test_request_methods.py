from datetime import datetime, timedelta
from unittest import TestCase

from pyramid.request import apply_request_extensions
from arche.testing import barebone_fixture
from pyramid import testing


class RequestMethodTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('arche.testing')
        self.config.include('arche.testing.catalog')
        self.config.include('arche.testing.workflow')

    def tearDown(self):
        testing.tearDown()

    @property
    def _mut(self):
        from betahaus.roadrunner.models import request_methods
        return request_methods

    def _fixture(self):
        root = barebone_fixture(self.config)
        request = testing.DummyRequest()
        apply_request_extensions(request)
        request.root = root
        return root, request

    def test_sum_time(self):
        from betahaus.roadrunner.models.task import Task
        from betahaus.roadrunner.models.time_entry import TimeEntry
        root, request = self._fixture()
        root['task'] = task = Task()
        task['1'] = TimeEntry(
            creator=['robin'],
            start_time=datetime(1999, 12, 12, hour=11),
            stop_time=datetime(1999, 12, 12, hour=12)
        )
        task['2'] = TimeEntry(
            creator=['robin'],
            start_time=datetime(1999, 12, 12, hour=12),
            stop_time=datetime(1999, 12, 12, hour=14)
        )
        task['3'] = TimeEntry(
            creator=['arvid'],
            start_time=datetime(1999, 12, 12, hour=12),
            stop_time=datetime(1999, 12, 12, hour=14)
        )
        res = self._mut.sum_time(request, task)
        self.assertEqual({'arvid': timedelta(hours=2), 'robin': timedelta(hours=3)}, res)

    def test_format_delta(self):
        root, request = self._fixture()
        dt = timedelta(hours=1, minutes=3, seconds=50)
        self.assertEqual(self._mut.format_delta(request, dt, asstr=False), (1, 3, 50))
        self.assertEqual(self._mut.format_delta(request, dt, asstr=True), "1:03:50")
