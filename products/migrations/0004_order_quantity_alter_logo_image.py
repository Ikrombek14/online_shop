# Generated by Django 5.0.6 on 2024-06-09 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='logo',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='logo/'),
        ),
    ]
