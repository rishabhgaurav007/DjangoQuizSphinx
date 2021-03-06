# Generated by Django 2.1.5 on 2019-03-31 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subjective', '0003_auto_20190331_1424'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerSub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_ans', models.CharField(max_length=2000, verbose_name='userbyans')),
                ('ans_text', models.CharField(max_length=3000, verbose_name='your answer')),
                ('is_attempted', models.IntegerField(default=1)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subjective.QuestionSub')),
            ],
        ),
    ]
