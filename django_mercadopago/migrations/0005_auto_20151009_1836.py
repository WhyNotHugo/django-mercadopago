from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("mp", "0004_preference_owner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="status",
            field=models.CharField(
                verbose_name="estado",
                default="unp",
                max_length=3,
                choices=[
                    ("unp", "Sin procesar"),
                    ("ok", "Okay"),
                    ("404", "Error 404"),
                    ("err", "Error"),
                ],
            ),
        ),
    ]
