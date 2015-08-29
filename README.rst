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

Usage
-----

The following settings apply to this application::

    MERCADOPAGO_CLIENT_ID = 123456789
    MERCADOPAGO_CLIENT_SECRET = 'asdf123'
    MERCADOPAGO_SANDBOX = False
    # Process notifications as soon as they are received.
    MERCADOPAGO_ASYNC = False

NOTE: Asynchronous notification processing is still WIP.

To charge a user, you need to create a ``Preference``::

    self.preference = Preference.objects.create(
        title='the product name',
        price=10.0,
        reference='order-38452',
        success_url='http://example.com/mp_done',
    )

You can use the IPN to listen to payment notifications. You'll need to
configure them `here
<https://www.mercadopago.com/mla/herramientas/notificaciones>`_ and then expose
the endpoint by adding the following to your ``urls.py``::

    url(r'^mercadopago/', include('django_mercadopago.urls')),

Finally, you can handle payment notifications in real time using a
``post_update`` hook::

    @receiver(post_save, sender=MercadoPagoPayment)
    def process_payment(sender, instance=None, created=False, **kwargs):
        do_stuff()

Licence
-------

This software is distributed under the ISC licence. See LICENCE for details.

Copyright (c) 2015 Hugo Osvaldo Barrera <hugo@barrera.io>
