# Generated by Django 3.2.16 on 2022-12-13 12:37

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0034_helpdesksitesettings_socialmediasettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='header_buttons',
            field=wagtail.fields.StreamField([('item', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(verbose_name='Titel')), ('page', wagtail.blocks.PageChooserBlock(verbose_name='Pagina'))]))], blank=True, use_json_field=None, verbose_name='Buttons'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='intro',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='recent_question_buttons',
            field=wagtail.fields.StreamField([('item', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(verbose_name='Titel')), ('page', wagtail.blocks.PageChooserBlock(verbose_name='Pagina'))]))], blank=True, use_json_field=None, verbose_name='Buttons'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='recent_question_title',
            field=models.CharField(blank=True, max_length=255, verbose_name='Title'),
        ),
        migrations.CreateModel(
            name='StickySettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default="Didn't find the answer you were looking for? Check out the pending questions or ask your own question!", max_length=255, verbose_name='Text')),
                ('buttons', wagtail.fields.StreamField([('item', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(verbose_name='Titel')), ('page', wagtail.blocks.PageChooserBlock(verbose_name='Pagina'))]))], blank=True, use_json_field=None, verbose_name='Buttons')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
            ],
            options={
                'verbose_name': 'Sticky',
            },
        ),
    ]
