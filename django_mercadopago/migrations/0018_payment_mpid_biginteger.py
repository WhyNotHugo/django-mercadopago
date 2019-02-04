from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mp', '0017_preference_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='mp_id',
            field=models.BigIntegerField(unique=True, verbose_name='mp id'),
        ),
    ]
