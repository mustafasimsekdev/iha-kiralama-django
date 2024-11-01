# Generated by Django 5.1.2 on 2024-11-01 11:37

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('personals', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
            ],
        ),
        migrations.CreateModel(
            name='AircraftProduction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assembly_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('aircraft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='processes.aircraft')),
                ('assembly_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PartProduction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('produced_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('recycled_date', models.DateTimeField(blank=True, null=True)),
                ('is_assembled', models.BooleanField(default=False)),
                ('aircraft_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parts', to='processes.aircraft')),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='processes.part')),
                ('producing_personal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='produced_parts', to=settings.AUTH_USER_MODEL)),
                ('recycled_personal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recycled_parts', to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personals.team')),
            ],
        ),
        migrations.CreateModel(
            name='PartOfAircraft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aircraft_production', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parts_used', to='processes.aircraftproduction')),
                ('part_production', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='processes.partproduction')),
            ],
        ),
        migrations.CreateModel(
            name='PartStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('aircraft_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='processes.aircraft')),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='processes.part')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personals.team')),
            ],
        ),
    ]