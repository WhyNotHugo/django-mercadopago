from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("mp", "0003_payment_status_detail_length"),
    ]

    operations = [
        migrations.AddField(
            model_name="preference",
            name="owner",
            field=models.ForeignKey(
                to="mp.Account",
                verbose_name="dueño",
                related_name="preferences",
                default=1,
                on_delete=models.CASCADE,
            ),
            preserve_default=False,
        ),
    ]
