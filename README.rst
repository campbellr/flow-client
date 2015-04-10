====
Flow
====

A python client for `Polar Flow`_.

**NOTE:** This currently uses unsupported APIs (the same APIs that the
Polar Flow web app uses) so can break at any moment. Ideally we would
use `Polar AccessLink`_ but it requires approval from Polar, which I
haven't been able to get yet.

Features
========

* Fetch a list of activities within given date range
* Fetch the TCX file for any activity

Install
=======

This package isn't on PyPi yet, so the easiest way to install is directly
from the git repository::

    $ pip install git+git://github.com/campbellr/flow-client.git

Usage
=====

Usage is fairly simple. Simply instantiate a ``FlowClient``, login with your
Polar Flow credentials and fetch activities with the ``activities`` method:

.. code-block:: python

    >>> from flow import FlowClient
    >>>
    >>> client = FlowClient()
    >>> client.login('username@example.com', 'password')
    >>> # no arguments will fetch all activities in the last 30 days
    >>> activity = client.activities()[0]
    >>> print activity
    Activity(63464689)
    >>> print activity.type
    EXERCISE
    >>> print activity.datetime
    2015-03-10T19:38:18.000Z
    >>> print activity.distance
    4964.10009766

The entire list of attributes of an ``Activity`` can be viewed using ``dir``.

Finally, you can download the tcx file for a given activity with the
``Activty.tcx`` method:

.. code-block:: python

    >>> print activity.tcx()
    <?xml version="1.0" encoding="UTF-8"?><TrainingCenterDatabase xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"><Activities><Activity Sport="Running"><Id>2015-03-10T19:38:18.000Z</Id><Lap StartTime="2015-03-10T19:38:18.000Z"><TotalTimeSeconds>426.0</TotalTimeSeconds><DistanceMeters>1000.0</DistanceMeters>
  [...]

Contributing
============

Contributions are greatly appreciated! Feel free to submit a pull request, or file
an issue in our `issue tracker`_.

.. _Polar Flow: https://flow.polar.com
.. _issue tracker: https://github.com/campbellr/flow-client/issues
.. _Polar AccessLink: http://www.polar.com/en/connect_with_polar/polar_accesslink
