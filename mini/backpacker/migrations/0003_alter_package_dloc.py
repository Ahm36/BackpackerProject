# Generated by Django 4.0 on 2022-02-23 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backpacker', '0002_alter_package_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='dloc',
            field=models.CharField(max_length=300),
        ),
    ]
