import csv
import os
from django.db import migrations
from django.conf import settings
from unicodedata import decimal

Date = 0
France = 1
Germany = 2
Korea = 3
US = 4
UK = 5

def add_covid19(apps, schema_editor):
    covid19 = apps.get_model("chart", "covid19")
    csv_file = os.path.join(settings.BASE_DIR, 'covid_19.csv')
    with open(csv_file) as dataset:                   # 파일 객체 dataset
        reader = csv.reader(dataset)                    # 파일 객체 dataset에 대한 판독기 획득
        next(reader)  # ignore first row (headers)      # __next__() 호출 때마다 한 라인 판독
        for entry in reader:                            # 판독기에 대하여 반복 처리
            covid19.objects.create(                       # DB 행 생성
                date=entry[Date],
                france=float(entry[France]),
                germany=float(entry[Germany]),
                korea=float(entry[Korea]),
                us=float(entry[US]),
                uk=float(entry[UK])
            )

class Migration(migrations.Migration):
    dependencies = [                            # 선행 관계
        ('chart', '0003_covid19')]
    operations = [                              # 작업
        migrations.RunPython(add_covid19),   # add_passengers 함수를 호출
    ]