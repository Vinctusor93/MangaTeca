# Generated by Django 4.2.19 on 2025-03-13 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_postmanga_urlimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='postmanga',
            name='titleUrl',
            field=models.CharField(default='ciao', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='postmanga',
            name='title',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]
