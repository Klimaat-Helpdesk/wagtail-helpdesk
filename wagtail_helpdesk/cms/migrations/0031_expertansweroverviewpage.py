# Generated by Django 3.2.16 on 2022-11-29 09:58

from django.db import migrations, models
import django.db.models.deletion
import wagtail.contrib.routable_page.models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0030_askquestionpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpertAnswerOverviewPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
    ]
