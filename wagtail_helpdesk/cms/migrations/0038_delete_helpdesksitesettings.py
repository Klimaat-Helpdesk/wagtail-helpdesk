# Generated by Django 3.2.16 on 2022-12-22 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0037_streamfield_use_json_field'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HelpdeskSiteSettings',
        ),
    ]