# Generated by Django 3.0.7 on 2020-07-01 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_events_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='event_image',
            field=models.ImageField(default=None, upload_to=None),
            preserve_default=False,
        ),
    ]
