from django.db import migrations


def move_item_data(apps, schema_editor):
    """Move Item data from Preference into the new model."""
    db_alias = schema_editor.connection.alias

    Preference = apps.get_model("mp", "Preference")
    Item = apps.get_model("mp", "Item")

    for preference in Preference.objects.using(db_alias).all():
        Item.objects.using(db_alias).create(
            preference=preference,
            title=preference.title,
            description=preference.description,
            quantity=preference.quantity,
            unit_price=preference.price,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("mp", "0019_split_preference_items"),
    ]

    operations = [
        migrations.RunPython(move_item_data),
    ]
