from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booking', '0003_event_title'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AlterField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='booking',
            name='download_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='booking',
            name='last_downloaded',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together={('event', 'seat')},
        ),
        migrations.CreateModel(
            name='DownloadLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.booking')),
            ],
        ),
    ]
