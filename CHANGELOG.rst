Changelog
=========

v4.6.2
------
* Fix notifications view crashing when receiving a POST for a merchant order
  (it seems these notifications are messed up and have rubbish).
* Notifications endpoints now return JSON (which should make testing apps
  slightly more pleasant).

v4.6.1
------
* Fix parsing of notifications received via POST, which seem to have a
  different format to those which are received via GET.

v4.5.0
------
* Added a missing migration for recent notification changes.
* Notifications are now processed either if received via GET or POST.
  Formerly, only GET was used, but this seems to be changing recently.

v4.4.0
------

* Merged ``STATUS_UNPROCESSED`` and ``STATUS_WITH_UPDATES`` into just
  ``STATUS_PENDING``. The latter was not actually used as expected, and the
  overlap was confusing and of little use.
* Allow polling Preference statuses via the admin.
* Fix crashes when dealing with unknown preferences.
* Improved logging for received notifications.

v4.3.0
------

* Notification and callback URLs are now unique per-preference, making it
  even clearer to identify them by URL. This version keeps backwards
  compatibility with old URLs (for yet-to-be-paid preferences with old-style
  URLs).
* Notifications now have a direct relationship to the preference they belong
  to.

v4.2.0
------

* Rename package to ``django-mercadopago``.

v4.1.1
------

* Indicate that this package is being renamed to ``django-mercadopago`` on
  PyPI.
* List ``factory-boy`` as an optional dependency (only if you're using test
  fixtures).

v4.1.0
------

* Provide fixtures for all models.

v4.0.0
------

* Replaced ``payer`` with ``extra_fields``, which allow sending a lot more
  custom data to MercadoPago when creating preferences.

v3.0.0
------

* Allow sending ``payer`` and ``description`` when creating preferences.
* Replaced ``MERCADOPAGO_ASYNC`` with the opposite ``MERCADOPAGO_AUTOPROCESS``
  setting, since asynchronous processing will never be built in (only the
  necessary helpers)
* Fire a signal when a notification is received. The docs mention how to listen
  to it, which you might want to do if you'd like to do asynchronous
  processing.
* Add a management command to poll unpaid preferences.
* Introduced this changelog.
