django-mercadopago
==================

.. image:: https://gitlab.com/hobarrera/django-mercadopago/badges/master/build.svg
  :target: https://gitlab.com/hobarrera/django-mercadopago/commits/master
  :alt: build status

.. image:: https://codecov.io/gl/hobarrera/django-mercadopago/branch/master/graph/badge.svg
  :target: https://codecov.io/gl/hobarrera/django-mercadopago
  :alt: coverage report

.. image:: https://img.shields.io/pypi/v/django-mercadopago.svg
  :target: https://pypi.python.org/pypi/django-mercadopago
  :alt: version on pypi

.. image:: https://img.shields.io/pypi/l/django-mercadopago.svg
  :alt: licence

**django-mercadopago** is a simple django application for interacting with
`MercadoPago <https://www.mercadopago.com.ar/>`_, aiming to be rather simple,
and only covers the basic uses cases.

Features
--------

Our intention is not to cover 100% of the features of the upstream API, but
rather provide a simple app that allows accepting and tracking payments. This
should suffice for simple sites like shopping carts, online sales, etc.

Pull requests are always welcome. Please don't hesitate to open an issue if you
encounter a problem. New features will generally only be added as needed, but
again, accepted if you submit a patch.

Installation
------------

Installation should generally be done via pip::

    pip install django-mercadopago

Configuration
-------------

You'll need to obtainer your API credentials (``app id`` and ``secret key``)
`here <https://applications.mercadopago.com/>`_ and  create an ``Account``
object with them. This creation can be done via the django admin included with
this app or programmatically.

You should also expose the notifications endpoints like this::

    url(r'^mercadopago/', include('django_mercadopago.urls'), namespace='mp'),
    # Make sure namespace is 'mp', since we assume it is for notification URL
    # contruction.

Note that these endpoints are **required**, since notification callbacks won't
work without them.

There are also a few Django settings that configure the behaviour of this app:

MERCADOPAGO_AUTOPROCESS
~~~~~~~~~~~~~~~~~~~~~~~

**Required**

If ``MERCADOPAGO_AUTOPROCESS`` is ``True``, notifications will be processed as
soon as they are received. Otherwise, it's up to the developer to process them.
A signal is always fired when a notification has been created, and a common
pattern if not auto-processing is to have a celery task to process them::

    @receiver(notification_received)
    def process_notification(sender, **kwargs):
        tasks.process_notification.delay(notification=sender)

MERCADOPAGO_POST_PAYMENT_VIEW
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Required**

The setting ``MERCADOPAGO_POST_PAYMENT_VIEW`` must define name of the view
where users are redirected after a payment.  This view will receive as an
argument the ``id`` of the notification created for this payment.

MERCADOPAGO_BASE_HOST
~~~~~~~~~~~~~~~~~~~~~

**Required**

``MERCADOPAGO_BASE_HOST`` defines the domain name to use for notification URLs.
It'll be prepended to the exact URL of the exposed notifications endpoint.

Usage
-----

MercadoPago lets you create preferences, for which you'll later receive
notifications (indicating if it was paid, or what happened)::

    self.preference = Preference.objects.create(
        title='the product name',
        price=10.0,
        reference='order-38452',
        success_url='http://example.com/mp_done',
        account=account,
    )

If your app will only be using a single MercadoPago account, just use::

    account = Account.objects.first()

Finally, you can handle payment notifications in real time using a
``post_update`` hook::

    @receiver(post_save, sender=MercadoPagoPayment)
    def process_payment(sender, instance=None, created=False, **kwargs):
        do_stuff()

Backwards compatibility
-----------------------

Note that, prior to v4.2.0, this package was called
``django-mercadopago-simple`` on PyPI. Older release exist under that name.

Version 2.0.0 changes the database schema quite a bit. While older data is
retained, some missing fields had to be filled. Auto-generated data will have
negative key values, and should easily be recognizable.

Regrettably, filling in this data automatically is not possible. However, there
is no data loss involved.

Licence
-------

This software is distributed under the ISC licence. See LICENCE for details.

Copyright (c) 2015-2017 Hugo Osvaldo Barrera <hugo@barrera.io>
