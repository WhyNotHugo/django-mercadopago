from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("mp", "0017_preference_quantity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="mp_id",
            field=models.BigIntegerField(unique=True, verbose_name="mp id"),
        ),
    ]
