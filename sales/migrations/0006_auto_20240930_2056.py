# Generated by Django 3.1.3 on 2024-09-30 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_auto_20240930_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image01',
            field=models.ImageField(upload_to='sales/image01/', verbose_name='업로드 이미지01'),
        ),
    ]
