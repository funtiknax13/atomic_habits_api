# Generated by Django 4.2.5 on 2023-09-23 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='award',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='вознаграждение'),
        ),
    ]
