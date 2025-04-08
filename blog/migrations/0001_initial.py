# Generated by Django 4.2.19 on 2025-03-27 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tag', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('color', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['tag'],
            },
        ),
        migrations.CreateModel(
            name='PostManga',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=400)),
                ('lastChapter', models.CharField(max_length=100)),
                ('dateLastChapter', models.CharField(max_length=20)),
                ('author', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('date_created', models.DateField(auto_now=True)),
                ('urlImage', models.URLField(max_length=300)),
                ('image', models.FileField(blank=True, null=True, upload_to='images/manga/')),
                ('tags', models.ManyToManyField(to='blog.tag')),
            ],
        ),
    ]
