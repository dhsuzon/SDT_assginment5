# Generated by Django 5.1.1 on 2024-11-23 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_alter_categorymodel_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorymodel',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
