# Generated by Django 4.0.2 on 2022-02-10 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InterviewSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('time', models.TimeField(null=True)),
                ('slot', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='PanelMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=40)),
                ('phone', models.CharField(max_length=12)),
                ('branch', models.CharField(max_length=12, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ParticipantDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=40)),
                ('phone', models.CharField(max_length=12)),
                ('branch', models.CharField(max_length=12, null=True)),
                ('member_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PanelRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('host', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('panel_members', models.ManyToManyField(blank=True, related_name='members', to='base.PanelMember')),
                ('participants', models.ManyToManyField(blank=True, related_name='participants', to='base.ParticipantDetail')),
                ('set_time', models.ManyToManyField(blank=True, to='base.InterviewSlot')),
            ],
        ),
    ]