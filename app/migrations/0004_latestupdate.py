# Generated by Django 5.0.3 on 2024-03-06 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_codesnippet_id_codesnippet_code_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='LatestUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update', models.CharField(max_length=1000)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
