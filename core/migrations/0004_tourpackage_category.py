# Generated by Django 5.2.3 on 2025-06-25 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_tourpackage_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourpackage',
            name='category',
            field=models.CharField(choices=[('top', 'Top Pick'), ('budget', 'Budget-Friendly'), ('luxury', 'Luxury'), ('adventure', 'Adventure'), ('beach', 'Beach Side'), ('hill', 'Hill Station')], default='top', max_length=20),
        ),
    ]
