# Generated by Django 4.0.3 on 2022-03-07 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_category_blog_categories'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]
