# Generated by Django 3.1.7 on 2021-02-25 18:16

import apps.projects.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20210225_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='image',
            field=models.ImageField(upload_to=apps.projects.models.PathAndRename('images/')),
        ),
        migrations.AlterField(
            model_name='project',
            name='gallery',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project', to='projects.gallery'),
        ),
    ]