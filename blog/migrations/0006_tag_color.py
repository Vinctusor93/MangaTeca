# Generated by Django 4.2.19 on 2025-02-27 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_tag_postmanga_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='color',
            field=models.CharField(default='blue', max_length=100),
            preserve_default=False,
        ),
    ]
