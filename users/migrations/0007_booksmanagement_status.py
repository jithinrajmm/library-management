# Generated by Django 4.1.1 on 2022-09-17 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_booksmanagement'),
    ]

    operations = [
        migrations.AddField(
            model_name='booksmanagement',
            name='status',
            field=models.CharField(default='borrowed', max_length=50),
        ),
    ]