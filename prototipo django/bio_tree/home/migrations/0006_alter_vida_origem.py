# Generated by Django 4.0.2 on 2022-02-18 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_vida_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vida',
            name='origem',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
