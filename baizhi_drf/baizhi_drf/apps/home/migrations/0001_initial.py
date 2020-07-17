# Generated by Django 2.0.6 on 2020-07-17 04:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_show', models.BooleanField(default=False, verbose_name='是否显示')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('ordering', models.SmallIntegerField(default=1, verbose_name='排序')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.BaseModel')),
                ('image', models.ImageField(max_length=200, upload_to='banner', verbose_name='轮播图')),
                ('title', models.CharField(max_length=200, verbose_name='轮播图名称')),
                ('link', models.CharField(max_length=300, verbose_name='轮播图链接')),
            ],
            options={
                'verbose_name': '轮播图',
                'verbose_name_plural': '轮播图',
                'db_table': 'bz_banner',
            },
            bases=('home.basemodel',),
        ),
        migrations.CreateModel(
            name='Navigation',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.BaseModel')),
                ('title', models.CharField(max_length=200, verbose_name='导航标题')),
                ('link', models.CharField(max_length=300, verbose_name='导航链接')),
                ('position', models.SmallIntegerField(choices=[(0, '顶部'), (1, '底部')], default=0)),
                ('is_site', models.BooleanField(default=False, verbose_name='外部链接')),
            ],
            options={
                'verbose_name': '导航',
                'verbose_name_plural': '导航',
                'db_table': 'bz_nav',
            },
            bases=('home.basemodel',),
        ),
    ]