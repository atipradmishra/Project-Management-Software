# Generated by Django 4.2 on 2024-03-14 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myAPP', '0004_trackingyear_dip_details_tracking_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity_timeframe',
            name='tracking_year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myAPP.trackingyear'),
        ),
        migrations.AddField(
            model_name='month_plan',
            name='target',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='month_plan',
            name='target_achived',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='monthly_project_clearance',
            name='is_approvedby_ceo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='monthly_project_clearance',
            name='is_approvedby_hr',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='monthly_project_clearance',
            name='is_rejectedby_ceo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='monthly_project_clearance',
            name='is_rejectedby_hr',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='monthly_project_clearance',
            name='is_submited',
            field=models.BooleanField(default=False),
        ),
    ]