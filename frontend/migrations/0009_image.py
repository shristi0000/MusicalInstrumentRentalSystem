# Generated by Django 4.2.10 on 2024-04-09 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0008_alter_rentinstruments_instrument_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.FileField(upload_to='InstrumentHub_Images')),
            ],
        ),
    ]
