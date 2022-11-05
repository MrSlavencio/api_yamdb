# Generated by Django 2.2.16 on 2022-11-05 18:05

from django.db import migrations, models
import reviews.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20221104_2239'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='review',
            new_name='review_id',
        ),
        migrations.RenameField(
            model_name='reviews',
            old_name='title',
            new_name='title_id',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='title',
        ),
        migrations.AddField(
            model_name='comments',
            name='text',
            field=models.TextField(default='test'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reviews',
            name='score',
            field=models.IntegerField(default=5, validators=[reviews.validators.validate_score]),
            preserve_default=False,
        ),
    ]
