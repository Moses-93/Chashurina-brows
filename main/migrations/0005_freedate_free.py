# Generated by Django 5.1.1 on 2024-09-16 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_freedate_remove_notes_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="freedate",
            name="free",
            field=models.BooleanField(default=True),
        ),
    ]
