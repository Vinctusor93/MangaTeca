# Generated by Django 5.1.6 on 2025-02-18 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_postmanga_urlimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmanga',
            name='description',
            field=models.TextField(),
        ),
    ]
