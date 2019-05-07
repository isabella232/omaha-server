# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-07 07:20


from django.db import migrations


def delete_duplicated_os(apps, schema_editor):
    Os = apps.get_model("omaha", "Os")
    Request = apps.get_model("omaha", "Request")
    list_args = Os.objects.all().values('platform', 'version', 'sp', 'arch')
    not_dup_args = []
    dup_args = []

    for args in list_args:
        if args in not_dup_args:
            if args not in dup_args:
                dup_args.append(args)
        else:
            not_dup_args.append(args)

    print("\nDuplicated arguments: %s" % dup_args)
    for args in dup_args:
        dups = list(Os.objects.filter(**args))
        original = dups[0]
        for os in dups[1:]:
            Request.objects.filter(os=os.id).update(os=original.id)
            os.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('omaha', '0026_grant_permission_django_site'),
    ]

    operations = [
        migrations.RunPython(delete_duplicated_os, reverse_code=migrations.RunPython.noop),
    ]
