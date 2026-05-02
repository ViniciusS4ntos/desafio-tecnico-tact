import csv
import os
from django.db import migrations


def importar_csv(apps, schema_editor):
    CensoCelular = apps.get_model('datamobile', 'CensoCelular')
    
    
    csv_path = os.path.join(
        os.path.dirname(__file__),   
        '..', '..', 'data', 'tab2011_postgres.csv'
    )
    csv_path = os.path.abspath(csv_path)

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        objs = []
        for i, row in enumerate(reader, start=1):
            objs.append(CensoCelular(
                id=i,
                grupo_idade=row['grupo_idade'],
                brasil=int(row['brasil'].replace('.', '')),
                norte=int(row['norte'].replace('.', '')),
                nordeste=int(row['nordeste'].replace('.', '')),
                sudeste=int(row['sudeste'].replace('.', '')),
                sul=int(row['sul'].replace('.', '')),
                centro_oeste=int(row['centro_oeste'].replace('.', '')),
            ))
        CensoCelular.objects.bulk_create(objs)


class Migration(migrations.Migration):

    dependencies = [
        ('datamobile', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(importar_csv, migrations.RunPython.noop),
    ]