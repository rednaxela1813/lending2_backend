from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0002_use_companyinfo"),
        ("accounting", "0002_managerprofile_to_companyinfo"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Company",
        ),
    ]
