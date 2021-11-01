# Generated by Django 3.2.7 on 2021-10-29 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Caregiver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caregiver_id', models.CharField(max_length=20)),
                ('caregiver_data', models.JSONField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=20)),
                ('client_data', models.JSONField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Eponym',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=20, null=True)),
                ('language', models.CharField(max_length=20)),
                ('status', models.IntegerField(default=0)),
                ('caregiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='REST.caregiver')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='REST.client')),
            ],
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_text', models.TextField()),
                ('status', models.IntegerField(default=0)),
                ('entities', models.JSONField(null=True)),
                ('replacement_text', models.TextField(null=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='REST.session')),
            ],
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_entity', models.CharField(max_length=100)),
                ('out_entity', models.CharField(max_length=100, null=True)),
                ('type_entity', models.CharField(max_length=100, null=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='REST.session')),
            ],
        ),
    ]
