# Generated by Django 4.1.1 on 2022-09-17 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_books'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='status',
            field=models.CharField(default='available', max_length=100),
        ),
    ]