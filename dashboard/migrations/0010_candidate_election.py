# Generated by Django 5.1.1 on 2024-10-13 15:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_remove_candidate_election'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='election',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='candidates', to='dashboard.election'),
        ),
    ]
