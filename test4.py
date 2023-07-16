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
    ('지식', 
    '이해',
    '적용',
    ), 
    index=1
)

if question == '지식':
    quset = '책에 어떤 동물이 나왔나요?', '이 동물의 이름은 무엇인가요?', '달팽이는 어떤 음식을 좋아하나요?'
if question == '이해':
    quset = '달팽이는 동물일까요, 곤충일까요?', '달팽이처럼 느린 동물은 또 무엇이 있을까요?', '달팽이를 키울 대 주의해야 할 점은 무엇인가요?'
if question == '적용':
    quset = '거북이 모양으로 만든 물건에는 어떤 것들이 있나요?', '달팽이와 거북이는 어떤 점이 비슷한가요? ', '만약 나에게도 달팽이처럼 등껍질이 있다면 어떻게 사용할 수 있을까요?'

if keyword and question:
    preset_text = f'키워드를 포함하여 질문 유형과 비슷한 질문을 생성합니다.\n\n키워드:{keyword}\n\n질문 유형:{quset}'

    request_data = {
        'text': preset_text,
        'maxTokens': 305,
        'temperature': 0.1,
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