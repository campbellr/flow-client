import datetime
import logging
from zipfile import ZipFile
from StringIO import StringIO

import requests


FLOW_URL = 'https://flow.polar.com'
FLOW_LOGIN_URL = "{}/ajaxLogin".format(FLOW_URL)
FLOW_LOGIN_POST_URL = "{}/login".format(FLOW_URL)
ACTIVITIES_URL = "{}/training/getCalendarEvents".format(FLOW_URL)

logger = logging.getLogger(__name__)


# TODO: look into this url for gathering training data:
#    https://flow.polar.com/training/analysis/<id>/range/data
#    https://flow.polar.com/training/analysis/71760805/range/data
# TODO: look into this url for gathering activity data:
#    https://flow.polar.com/activity/data/<end>/<start>
#    eg: https://flow.polar.com/activity/data/30.3.2015/10.5.2015

class FlowClient(object):

    """Interact with the (unofficial) Polar Flow API."""

    def __init__(self):
        self.session = requests.session()

    def login(self, username, password):
        postdata = {'email': username,
                    'password': password,
                    'returnURL': '/'}
        # We need to go here to gather some cookies
        self.session.get(FLOW_LOGIN_URL)
        resp = self.session.post(FLOW_LOGIN_POST_URL, data=postdata)
        if resp.status_code != 200:
            resp.raise_for_status()

    # FIXME: these aren't really activities as Flow defines them, they're
    # training sessions?
    # activity is the activity tracking stuff
    def activities(self, *args, **kwargs):
        """Return all activities between ``start_date`` and ``end_date``.

        ``end_date`` defaults to the current time, ``start_date`` defaults to
        30  days before ``end_date``.
        """
        return list(self.iter_activities(*args, **kwargs))

    def iter_activities(self, start_date=None, end_date=None):
        """Return a generator yielding `Activity` objects."""
        logger.debug("Fetching activities between %s and %s",
                     start_date, end_date)
        end_date = end_date or datetime.datetime.now()
        start_date = start_date or (end_date - datetime.timedelta(days=30))
        params = {'start': _format_date(start_date),
                  'end': _format_date(end_date)}
        resp = self.session.get(ACTIVITIES_URL, params=params)
        resp.raise_for_status()
        for data in resp.json():
            yield Activity(self.session, data)


# FIXME: it would be ideal if Activity didn't have to take a session object
# and instead just took an id (or optionally the activity data if already
# available)
class Activity(object):

    """Represents a single activity in Polar Flow.

    ``session`` must be an already authenticated `Session` object.

    """

    def __init__(self, session, data):
        self.session = session
        self.data = data

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self.data['listItemId'])

    def __getattr__(self, name):
        try:
            return self.data[name]
        except KeyError:
            raise AttributeError(name)

    def __dir__(self):
        return sorted(set(self.data.keys() +
                          dir(type(self)) +
                          list(self.__dict__)))

    def tcx(self):
        """Return the contents of the TCX file for the given activity.

        ``activity`` can either be an id or an activity dictionary
        (as returned by `get_activities`).

        """
        logging.debug("Fetching TCX file for %s", self.data['url'])
        tcx_url = FLOW_URL + self.data['url'] + '/export/tcx'

        resp = self.session.get(tcx_url)
        resp.raise_for_status()
        with ZipFile(StringIO(resp.content), 'r') as tcx_zip:
            namelist = tcx_zip.namelist()
            assert len(namelist) == 1, "Expected only one item in zip"
            tcx_name = tcx_zip.namelist()[0]
            # FIXME: should this return something other than a raw string?
            #   * parsed xml?
            #   * Some custom TCX object?
            return tcx_zip.read(tcx_name)


def _format_date(dt):
    return dt.strftime('%d.%m.%Y')
