# Generated by Django 3.1.6 on 2023-01-30 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveSmallIntegerField(blank=True, choices=[('1', '1'), ('2', 2), ('3', 3), ('4', 4), ('5', 5)], max_length=1024, verbose_name='Note'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=models.TextField(blank=True, max_length=2048),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='title',
            field=models.CharField(max_length=128),
        ),
    ]
