from django.db import migrations, models
from django.db.models import CASCADE


def migrate_company_refs(apps, schema_editor):
    EditableText = apps.get_model("dashboard", "EditableText")
    EditableImage = apps.get_model("dashboard", "EditableImage")
    OldCompany = apps.get_model("accounting", "Company")
    CompanyInfo = apps.get_model("company", "CompanyInfo")

    default_company = CompanyInfo.objects.first()

    def resolve_company(old_company_id):
        nonlocal default_company
        if not old_company_id:
            return default_company
        try:
            old = OldCompany.objects.get(pk=old_company_id)
        except OldCompany.DoesNotExist:
            return default_company
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
        if not default_company:
            default_company = target
        return target

    for obj in EditableText.objects.all():
        target = resolve_company(obj.company_id)
        obj.company_id = target.id if target else None
        obj.save(update_fields=["company"])

    for obj in EditableImage.objects.all():
        target = resolve_company(obj.company_id)
        obj.company_id = target.id if target else None
        obj.save(update_fields=["company"])


class Migration(migrations.Migration):

    dependencies = [
        ("company", "0001_initial"),
        ("accounting", "0002_managerprofile_to_companyinfo"),
        ("dashboard", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(migrate_company_refs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="editabletext",
            name="company",
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=CASCADE,
                related_name="editable_texts",
                to="company.companyinfo",
            ),
        ),
        migrations.AlterField(
            model_name="editableimage",
            name="company",
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=CASCADE,
                related_name="editable_images",
                to="company.companyinfo",
            ),
        ),
    ]
