# Generated by Django 3.2 on 2022-12-12 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_alter_reviewreport_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.IntegerField(choices=[(0, '无'), (1, '关注'), (2, '申诉学者接受-给用户'), (3, '申诉学者接受-给学者'), (4, '申诉学者驳回'), (5, '门户认领成功'), (6, '门户认领失败'), (7, '申诉学术成果接受-给用户'), (8, '申诉学术成果接受-给学者'), (9, '申诉学术成果失败'), (10, '评论'), (11, '回复评论'), (12, '举报评论')], default=0),
        ),
        migrations.AlterField(
            model_name='reviewreport',
            name='description',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='reviewreport',
            name='title',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
