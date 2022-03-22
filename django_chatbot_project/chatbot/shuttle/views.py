from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# from myHome.inseopbot import Login
# from myHome.inseopbot import weather
from shuttle.models import morning, noon
from django.db.models import F


# 오전 셔틀을 DB에서 불러오는 함수
def data_amfun():
    data_am = F.get(morning).decode('utf-8')
    data_shuttle = json.loads(data_am)
    return data_shuttle


def keyboard(request):
    return JsonResponse(
        {
            'type': 'buttons',
            'buttons': ['오전셔틀']
        }
    )


@csrf_exempt
def message(request):
    # 버튼값 처리
    json_str = (request.body).decode('utf-8')
    received_json = json.loads(json_str)
    button_name = received_json['action']['detailParams']['content']['value']

    try:
        am_num = [1, 2, 3, 4, 5, 6, 7, 8]
        mor_du = []
        mor_ch = []
        for i in range(len(am_num)):
            mor = morning.objects.get(num=am_num[i])
            mor_du.append(mor.dujeong)
            mor_ch.append(mor.cheon_station_am)

        # print(mor_du)
        pm_num = 9
        after = noon.objects.get(num=pm_num)

    except Exception as e:
        print(e)

    # 오전셔틀 버튼

    if button_name == "오전셔틀":
        answer_1 = "\n오전 셔틀은 다음과 같습니다.\n"
        answer_2 = "\n---------------두정역출발---------------"
        answer_3 = "\n-------------------------------------"
        answer_4 = "\n---------------천안역출발---------------"

        response_body = {
            'version': "2.0",
            'template': {
                'outputs': [
                    {
                        'simpleText': {
                            'text': answer_1 + answer_2 + "\n" + mor_du[0] + "\n" + mor_du[1] + "\n" + mor_du[2] + "\n" + mor_du[3] + "\n" + mor_du[4] + "\n" + mor_du[5] + "\n" + mor_du[6] + "\n" +mor_du[7] + answer_3 + "\n" + answer_4 + "\n" + mor_ch[0] + "\n" + mor_ch[1] + "\n" + mor_ch[2] + "\n" + mor_ch[3] + "\n" + mor_ch[4] + "\n" + mor_ch[5] + "\n" + mor_ch[6] + "\n" + mor_ch[7] + answer_3
                        }
                    }
                ],
            }
        }

    else:
        response_body = {
            'version': "2.0",
            'template': {
                'outputs': [
                    {
                        'simpleText': {
                            'text': "제발 되게 해주세요,,"
                        }
                    }
                ],
            }
        }

    return JsonResponse(response_body)