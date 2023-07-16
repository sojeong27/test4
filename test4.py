import json
import configparser
import http.client
import streamlit as st

class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def _send_request(self, completion_request):
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id
        }

        conn = http.client.HTTPSConnection(self._host)
        conn.request('POST', '/testapp/v1/completions/LK-D2', json.dumps(completion_request), headers)
        response = conn.getresponse()
        result = json.loads(response.read().decode(encoding='utf-8'))
        conn.close()
        return result

    def execute(self, completion_request):
        res = self._send_request(completion_request)
        if res['status']['code'] == '20000':
            return res['result']['text']
        else:
            return 'Error'

config = configparser.ConfigParser()
config.sections()
config.read('./your_apikey4.ini')

completion_executor = CompletionExecutor(
    host=config['CLOVA']['host'],
    api_key=config['CLOVA']['api_key'],
    api_key_primary_val=config['CLOVA']['api_key_primary_val'],
    request_id=config['CLOVA']['request_id']
)

st.title('좋은 질문 생성기')
keyword = st.text_input(
    '키워드', 
    placeholder='키워드를 입력해 주세요'
)

question = st.selectbox(
    '질문 유형',
    ('지식', '이해', '적용'), 
    index=1
)

if question == '지식':
    quset = '생김새', '이름', '색깔', '좋아하는 것', '뜻', '의미', '모양', '구성 요소'
if question == '이해':
    quset = '같은 종류는', '비슷한 예는', '비슷한 것', '다른 것', '같은 것', '비교하면', '분류하면'
if question == '적용':
    quset = '비슷한 느낌의 물건은', '만약 나라면', '모양이 변한다면', '만약 없다면'

if keyword and question:
    preset_text = f'키워드와 질문 유형을 포함하여 탐구 질문을 생성합니다. 각 문장마다 번호를 붙여 질문만 10개를 제시합니다. 답변과 답변 예시는 생성하지 않습니다.\n\n키워드:{keyword}\n\n질문 유형:{quset}'

    request_data = {
        'text': preset_text,
        'maxTokens': 200,
        'temperature': 0.2,
        'topK': 0,
        'topP': 0.8,
        'repeatPenalty': 5.0,
        'start': '\n###질문:',
        'stopBefore': ['###', '키워드:', '질문 유형:', '질문', '###\n'],
        'includeTokens': True,
        'includeAiFilters': True,
        'includeProbs': True
    }

    response_text = completion_executor.execute(request_data)
    #print(response_text)
    st.markdown(response_text.split('###')[1])