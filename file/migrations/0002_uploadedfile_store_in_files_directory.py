# Generated manually for the visible ``files`` upload directory.

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('file', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedfile',
            name='file',
            field=models.FileField(upload_to=''),
        ),
    ]
