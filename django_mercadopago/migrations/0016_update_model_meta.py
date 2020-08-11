import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("mp", "0015_payment_preference_notnull"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="secret_key",
            field=models.CharField(
                help_text="The SECRET_KEY given by MercadoPago.",
                max_length=32,
                verbose_name="secret key",
            ),
        ),
        migrations.AlterField(
            model_name="notification",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="notifications",
                to="mp.Account",
                verbose_name="owner",
            ),
        ),
        migrations.AlterField(
            model_name="notification",
            name="preference",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="notifications",
                to="mp.Preference",
                verbose_name="preference",
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="notification",
            field=models.OneToOneField(
                blank=True,
                help_text="The notification that informed us of this payment.",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="payment",
                to="mp.Notification",
                verbose_name="notification",
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="preference",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="payments",
                to="mp.Preference",
                verbose_name="preference",
            ),
        ),
        migrations.AlterField(
            model_name="preference",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="preferences",
                to="mp.Account",
                verbose_name="owner",
            ),
        ),
    ]
