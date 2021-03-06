# Generated by Django 2.2.3 on 2019-09-02 10:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0002_auto_20190812_1850'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='dashboard.Answer')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='answer_comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'answer_comment',
            },
        ),
    ]
