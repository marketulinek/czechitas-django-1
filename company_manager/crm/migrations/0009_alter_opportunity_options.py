# Generated by Django 4.0.3 on 2022-05-04 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_opportunity_created_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='opportunity',
            options={'get_latest_by': 'created_at', 'verbose_name_plural': 'Opportunities'},
        ),
    ]