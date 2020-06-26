# chart/views.py
from django.shortcuts import render
from django.db.models import Count, Q
import json
from django.http import JsonResponse
from .models import *


def home(request):
    return render(request, 'home.html')


def world_population(request):
    return render(request, 'world_population.html')


def ticket_class_view_1(request):  # 방법 1
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(
            survived_count=Count('ticket_class',
                                 filter=Q(survived=True)),
            not_survived_count=Count('ticket_class',
                                     filter=Q(survived=False))) \
        .order_by('ticket_class')
    return render(request, 'ticket_class_1.html', {'dataset': dataset})
#  dataset = [
#    {'ticket_class': 1, 'survived_count': 200, 'not_survived_count': 123},
#    {'ticket_class': 2, 'survived_count': 119, 'not_survived_count': 158},
#    {'ticket_class': 3, 'survived_count': 181, 'not_survived_count': 528}
#  ]


def ticket_class_view_2(request):  # 방법 2
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
                  not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
        .order_by('ticket_class')

    # 빈 리스트 3종 준비
    categories = list()             # for xAxis
    survived_series = list()        # for series named 'Survived'
    not_survived_series = list()    # for series named 'Not survived'
    survive_rate = list()


    # 리스트 3종에 형식화된 값을 등록
    for entry in dataset:
        categories.append('%s Class' % entry['ticket_class'])    # for xAxis
        survived_series.append(entry['survived_count'])         # for series named 'Survived'
        not_survived_series.append(entry['not_survived_count'])  # for series named 'Not survived'
        survive_rate.append(entry['survived_count'] \
                       / (entry['survived_count'] + entry['not_survived_count']) * 100.0)




    # json.dumps() 함수로 리스트 3종을 JSON 데이터 형식으로 반환
    return render(request, 'ticket_class_2.html', {
        'categories': json.dumps(categories),
        'survived_series': json.dumps(survived_series),
        'not_survived_series': json.dumps(not_survived_series),
        'survive_rate': json.dumps(survive_rate)
    })


def ticket_class_view_3(request):  # 방법 3
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
                  not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
        .order_by('ticket_class')

    # 빈 리스트 3종 준비 (series 이름 뒤에 '_data' 추가)
    categories = list()                 # for xAxis
    survived_series_data = list()       # for series named 'Survived'
    not_survived_series_data = list()   # for series named 'Not survived'

    # 리스트 3종에 형식화된 값을 등록
    for entry in dataset:
        categories.append('%s Class' % entry['ticket_class'])         # for xAxis
        survived_series_data.append(entry['survived_count'])          # for series named 'Survived'
        not_survived_series_data.append(entry['not_survived_count'])  # for series named 'Not survived'

    survived_series = {
        'name': 'Survived',
        'data': survived_series_data,
        'color': 'green'
    }
    not_survived_series = {
        'name': 'Survived',
        'data': not_survived_series_data,
        'color': 'red'
    }

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Titanic Survivors by Ticket Class'},
        'xAxis': {'categories': categories},
        'series': [survived_series, not_survived_series]
    }
    dump = json.dumps(chart)

    return render(request, 'ticket_class_3.html', {'chart': dump})


def json_example(request):  # 접속 경로 'json-example/'에 대응하는 뷰
    return render(request, 'json_example.html')


def chart_data(request):  # 접속 경로 'json-example/data/'에 대응하는 뷰
    dataset = Passenger.objects \
        .values('embarked') \
        .exclude(embarked='') \
        .annotate(total=Count('id')) \
        .order_by('-total')
    #  [
    #    {'embarked': 'S', 'total': 914}
    #    {'embarked': 'C', 'total': 270},
    #    {'embarked': 'Q', 'total': 123},
    #  ]

    # # 탑승_항구 상수 정의
    # CHERBOURG = 'C'
    # QUEENSTOWN = 'Q'
    # SOUTHAMPTON = 'S'
    # PORT_CHOICES = (
    #     (CHERBOURG, 'Cherbourg'),
    #     (QUEENSTOWN, 'Queenstown'),
    #     (SOUTHAMPTON, 'Southampton'),
    # )
    port_display_name = dict()
    for port_tuple in Passenger.PORT_CHOICES:
        port_display_name[port_tuple[0]] = port_tuple[1]
    # port_display_name = {'C': 'Cherbourg', 'Q': 'Queenstown', 'S': 'Southampton'}

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Number of Titanic Passengers by Embarkation Port'},
        'series': [{
            'name': 'Embarkation Port',
            'data': list(map(
                lambda row: {'name': port_display_name[row['embarked']], 'y': row['total']},
                dataset))
            # 'data': [ {'name': 'Southampton', 'y': 914},
            #           {'name': 'Cherbourg', 'y': 270},
            #           {'name': 'Queenstown', 'y': 123}]
        }]
    }
    # [list(map(lambda))](https://wikidocs.net/64)

    return JsonResponse(chart)


def covid_19(request):
    dataset = covid19.objects \
        .values('date', 'france', 'germany', 'korea', 'us', 'uk') \
        .order_by('date')

    # 빈 리스트 4종 준비
    date_series= list()  # for xAxis
    france_series = list()  # for series named 'Survived'
    germany_series = list()  # for series named 'Not survived'
    korea_series = list()
    us_series = list()
    uk_series = list()

    # 리스트 4종에 형식화된 값을 등록
    for entry in dataset:
        date_series.append(entry['date'])  # for xAxis
        france_series.append(entry['france'])  # for series named 'Survived'
        germany_series.append(entry['germany'])  # for series named 'Not survived'
        korea_series.append(entry['korea'])
        us_series.append(entry['us'])
        uk_series.append(entry['uk'])

    france_series = {
        'name': 'France',
        'data': france_series,
        'color': 'green'
    }
    germany_series = {
        'name': 'Germany',
        'data': germany_series,
        'color': 'yellow'
    }
    korea_series = {
        'name': 'Korea',
        'data': korea_series,
        'color': 'black'
    }
    us_series = {
        'name': 'US',
        'data':us_series,
        'color': 'red'
    }
    uk_series = {
        'name': 'UK',
        'data': uk_series,
        'color': 'purple'
    }
    chart = {
        'chart': {'type': 'line'},
        'title': {'text': 'Covid-19 확진자 발생율'},
        'xAxis': {'date_series': date_series,
                  'type': 'datetime',
                  'labels': {
                      'format': '{value:%Y-%m-%d}',
                  }
          },
        'yAxis': {"labels": {"format": "{value}건/백만명 "},
                  "title": {"text": "합계건수"}
                  },
        'series': [france_series, germany_series, korea_series, us_series, uk_series]
    }

    dump = json.dumps(chart, default=str)

    return render(request, 'covid_19.html', {'chart': dump})


def covid19_jupyterlab(request):
    return render(request, 'covid19_jupyterlab.html')

