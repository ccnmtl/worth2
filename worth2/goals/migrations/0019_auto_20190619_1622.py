# Generated by Django 2.1.9 on 2019-06-19 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0018_auto_20150702_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goalcheckinoption',
            name='order',
            field=models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order'),
        ),
        migrations.AlterField(
            model_name='goalcheckinoption',
            name='text',
            field=models.TextField(help_text='An option for the "What got in the way" dropdown for goal check-in.'),
        ),
        migrations.AlterField(
            model_name='goalcheckinresponse',
            name='i_will_do_this',
            field=models.CharField(choices=[('yes', 'I did it!'), ('in progress', "I'm still working on it."), ('no', "I haven't started this goal.")], max_length=255),
        ),
        migrations.AlterField(
            model_name='goaloption',
            name='goal_type',
            field=models.CharField(choices=[('services', 'Services'), ('risk reduction', 'Risk Reduction'), ('social support', 'Social Support')], db_index=True, default='services', max_length=255),
        ),
        migrations.AlterField(
            model_name='goaloption',
            name='order',
            field=models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order'),
        ),
        migrations.AlterField(
            model_name='goaloption',
            name='text',
            field=models.TextField(help_text='An option for the dropdowns in a specific GoalSetting pageblock.'),
        ),
        migrations.AlterField(
            model_name='goalsettingblock',
            name='goal_amount',
            field=models.PositiveSmallIntegerField(default=1, help_text='The number of goals on this block, including the main one.'),
        ),
        migrations.AlterField(
            model_name='goalsettingblock',
            name='goal_type',
            field=models.CharField(choices=[('services', 'Services'), ('risk reduction', 'Risk Reduction'), ('social support', 'Social Support')], default='services', max_length=255),
        ),
    ]
