# Generated by Django 5.1.3 on 2024-11-26 01:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name_plural": "Categories"},
        ),
        migrations.AlterModelOptions(
            name="expense",
            options={"ordering": ["-date"]},
        ),
    ]
