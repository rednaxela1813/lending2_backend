from django.db import migrations, models
from django.db.models import CASCADE


def migrate_managerprofile_company(apps, schema_editor):
    ManagerProfile = apps.get_model("accounting", "ManagerProfile")
    OldCompany = apps.get_model("accounting", "Company")
    CompanyInfo = apps.get_model("company", "CompanyInfo")

    # Try to reuse existing CompanyInfo if possible
    default_company = CompanyInfo.objects.first()
    for profile in ManagerProfile.objects.all():
        target = None
        if profile.company_id:
            try:
                old = OldCompany.objects.get(pk=profile.company_id)
                target = CompanyInfo.objects.filter(name=old.name).first()
                if not target:
                    target = CompanyInfo.objects.create(
                        name=old.name,
                        ico=old.ico,
                        dic=old.dic,
                        address="(migrated)",
                        phone="N/A",
                        email="placeholder@example.com",
                    )
            except OldCompany.DoesNotExist:
                pass
        if not target:
            if default_company:
                target = default_company
            else:
                target = CompanyInfo.objects.create(
                    name="Default Company",
                    ico="",
                    dic="",
                    address="(unset)",
                    phone="N/A",
                    email="placeholder@example.com",
                )
                default_company = target
        profile.company_info = target
        profile.save(update_fields=["company_info"])


class Migration(migrations.Migration):

    dependencies = [
        ("company", "0001_initial"),
        ("accounting", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="managerprofile",
            name="company_info",
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=CASCADE,
                related_name="managers",
                to="company.companyinfo",
            ),
        ),
        migrations.RunPython(migrate_managerprofile_company, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="managerprofile",
            name="company",
        ),
        migrations.RenameField(
            model_name="managerprofile",
            old_name="company_info",
            new_name="company",
        ),
    ]
