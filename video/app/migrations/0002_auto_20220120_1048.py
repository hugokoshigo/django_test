# Generated by Django 3.2.3 on 2022-01-20 02:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='nationality',
            new_name='country',
        ),
        migrations.RenameField(
            model_name='video',
            old_name='stattus',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='video',
            old_name='from_to',
            new_name='video_source',
        ),
        migrations.AlterUniqueTogether(
            name='video',
            unique_together={('video_name', 'video_type', 'video_source', 'country')},
        ),
    ]
