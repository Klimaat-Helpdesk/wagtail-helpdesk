# Generated by Django 4.2.15 on 2024-09-30 08:47

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0003_alter_answertag_tag"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="expertindexpage",
            name="outro",
        ),
        migrations.AddField(
            model_name="expertindexpage",
            name="outro_text",
            field=wagtail.fields.RichTextField(blank=True, verbose_name="Text"),
        ),
    ]
