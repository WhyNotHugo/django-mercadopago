from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("mp", "0008_auto_20151018_2208"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="notification",
            field=models.OneToOneField(
                null=True,
                blank=True,
                related_name="payment",
                verbose_name="notificación",
                help_text="La notificación que nos informó de este pago.",
                to="mp.Notification",
                on_delete=models.CASCADE,
            ),
        ),
    ]
