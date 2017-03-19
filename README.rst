django-mercadopago-simple
=========================

**django-mercadopago-simple** is a simple django application for interacting with
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

    pip install django-mercadopago-simple

Configuration
-------------

The following settings apply to this application::

    # Process notifications as soon as they are received:
    MERCADOPAGO_AUTOPROCESS = True
    # This is the hostname where your server will receive notifications:
    # Notifcation URLs will be sent with your preferences prefixing this to
    # their URLs.
    MERCADOPAGO_BASE_HOST = 'https://example.com/'

If ``MERCADOPAGO_AUTOPROCESS`` is ``True``, notifications will be processed as
soon as they are received. Otherwise, it's up to the developer to process them.
A signal is always fired when a notification has been created, and a common
pattern if not auto-processing is to have a celery task to process them::

    @receiver(notification_received)
    def process_notification(sender, **kwargs):
        tasks.process_notification.delay(notification=sender)

You'll also want to link your MercadoPago credentials to this app - maybe just
yours, maybe multiple accounts.

Once you've obtained your application ``app id`` and ``secret key`` `here
<https://applications.mercadopago.com/>`_, create an ``Account`` object with
them. This can be done via the django admin included with this app or
programmatically.

You should also expose the notifications endpoints like this::

    url(r'^mercadopago/', include('django_mercadopago.urls'), namespace='mp'),
    # Make sure namespace is 'mp', since we assume it is for notification URL
    # contruction.

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

Version 2.0.0 changes the database schema quite a bit. While older data is
retained, some missing fields had to be filled. Auto-generated data will have
negative key values, and should easily be recognizable.

Regrettably, filling in this data is not possible. However, there is no data
loss involved.

Licence
-------

This software is distributed under the ISC licence. See LICENCE for details.

Copyright (c) 2015-2017 Hugo Osvaldo Barrera <hugo@barrera.io>
