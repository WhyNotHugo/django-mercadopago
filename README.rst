django-mercadopago
==================

.. image:: https://travis-ci.com/WhyNotHugo/django-mercadopago.svg?branch=master
  :target: https://travis-ci.com/WhyNotHugo/django-mercadopago
  :alt: build status

.. image:: https://codecov.io/gh/whynothugo/django-mercadopago/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/whynothugo/django-mercadopago
  :alt: coverage report

.. image:: https://img.shields.io/pypi/v/django-mercadopago.svg
  :target: https://pypi.python.org/pypi/django-mercadopago
  :alt: version on pypi

.. image:: https://img.shields.io/pypi/l/django-mercadopago.svg
  :target: https://github.com/WhyNotHugo/django-mercadopago/blob/master/LICENCE
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

There are also a few Django settings that configure the behaviour of this app.
All these settings are included in a single ``dict`` inside your Django
settings::

    MERCADOPAGO = {
        'autoprocess': True,
        'success_url': 'myapp:mp_success',
        'failure_url': 'myapp:mp_failure',
        'pending_url': 'myapp:mp_pending',
        'base_host': 'https://www.mysite.com
    }

See below for an explanation of each setting.

AUTOPROCESS
~~~~~~~~~~~

**Required**

If set to ``True``, notifications will be processed as soon as they are
received. Otherwise, it's up to the developer to process them.

A signal is always fired when a notification has been created, and a common
pattern if not auto-processing is to have a celery task to process them::

    @receiver(notification_received)
    def process_notification(sender, **kwargs):
        tasks.process_notification.delay(notification=sender)

SUCCESS_URL
~~~~~~~~~~~

**Required**

The named URL pattern where requests are redirected after a user successfully
completes a payment. This url will receive as an argument the ``id`` of the
notification created for this payment.

For example, this if this value were set to ``payment_recived``, a
corresponding URL pattern would look like this::

    url(
        r'pago_recibido/(?P<pk>.*)$',
        order.OrderPaidView.as_view(),
        name='payment_received',
    ),

FAILURE_URL
~~~~~~~~~~~

**Required**

The named URL pattern where requests are redirected after a user payment fails.
This url will receive as an argument the ``id`` of the preference that the user
attempted to pay


PENDING_URL
~~~~~~~~~~~

**Required**

The named URL pattern where requests are redirected after a user completes a
payment, but confirmation is pending (for example, a transaction that takes a
few days, bank deposit, etc).
This url will receive as an argument the ``id`` of the preference that the user
is attempting to pay.

BASE_HOST
~~~~~~~~~

**Required**

Defines the domain name to use for notification and callback URLs.  It'll be
prepended to the exact URL of the exposed notifications endpoint.

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

To complete a full payment flow, you'd:

* Create a ``Preference``.
* Use ``preference.url`` to forward the user to the payment page.
* If your webhooks are properly configured, the notification will be created as
  soon as the user completes the operation.
    * Depending on your ``AUTOPROCESS`` setting, the status may be updated
      automatically, or may be up to you (see above).
    * If you're not using webhooks, you'll have to poll the status manually
      from time to time (using ``poll_status``).

Backwards compatibility
-----------------------

As of v5.0.0, the notification and callback URL formats generated by v4.2.0 and
earlier is no longer supported. Users must upgrade to v4.3.0, and run this
version until all pending payments are completed (or expire), and only then
upgrade to v5.0.0.

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

Copyright (c) 2015-2018 Hugo Osvaldo Barrera <hugo@barrera.io>
