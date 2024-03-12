# Generated by Django 4.2 on 2024-03-11 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myAPP', '0003_monthly_staff_clearance_any_other_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackingYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='dip_details',
            name='tracking_year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myAPP.trackingyear'),
        ),
    ]
