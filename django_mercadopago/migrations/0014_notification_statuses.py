from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mp', '0013_notification_preference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.CharField(
                choices=[
                    ('unp', 'Pending'),
                    ('pro', 'Processed'),
                    ('ign', 'Ignored'),
                    ('ok', 'Okay'),
                    ('404', 'Error 404'),
                    ('err', 'Error')
                ],
                default='unp',
                max_length=3,
                verbose_name='status'
            ),
        ),
    ]
