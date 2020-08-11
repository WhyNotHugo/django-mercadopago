import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("mp", "0018_payment_mpid_biginteger"),
    ]

    operations = [
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=256, verbose_name="title",),),
                (
                    "currency_id",
                    models.CharField(
                        default="ARS", max_length=3, verbose_name="currency id",
                    ),
                ),
                (
                    "description",
                    models.CharField(max_length=256, verbose_name="description",),
                ),
                ("quantity", models.PositiveSmallIntegerField(default=1),),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=9),),
            ],
            options={"verbose_name": "item", "verbose_name_plural": "items"},
        ),
        migrations.AlterField(
            model_name="preference",
            name="mp_id",
            field=models.CharField(
                help_text="The id MercadoPago has assigned for this Preference",
                max_length=46,
                null=True,
                verbose_name="mercadopago id",
            ),
        ),
        migrations.AddField(
            model_name="item",
            name="preference",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="items",
                to="mp.Preference",
                verbose_name="preference",
            ),
        ),
    ]
