# Generated by Django 2.1 on 2018-10-08 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mln', '0004_concert_arcade_arrows'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modulesavehoparcade',
            name='bottom',
        ),
        migrations.RemoveField(
            model_name='modulesavehoparcade',
            name='middle',
        ),
        migrations.RemoveField(
            model_name='modulesavehoparcade',
            name='top',
        ),
        migrations.AddField(
            model_name='modulesavehoparcade',
            name='bottom_0',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='modulesavehoparcade',
            name='bottom_1',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='modulesavehoparcade',
            name='bottom_2',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='modulesavehoparcade',
            name='middle_0',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='modulesavehoparcade',
            name='middle_1',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='modulesavehoparcade',
            name='middle_2',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='modulesavehoparcade',
            name='top_0',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='modulesavehoparcade',
            name='top_1',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='modulesavehoparcade',
            name='top_2',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]