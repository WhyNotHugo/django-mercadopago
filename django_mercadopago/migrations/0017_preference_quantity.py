from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("mp", "0016_update_model_meta"),
    ]

    operations = [
        migrations.AddField(
            model_name="preference",
            name="quantity",
            field=models.PositiveIntegerField(default=1, verbose_name="quantity"),
        ),
    ]
