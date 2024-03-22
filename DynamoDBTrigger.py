import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    response_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
    }
    try:
        # 받아온 이벤트 
        print('event {}'.format(event))
        # DynamoDB 이벤트 처리
        for record in event['Records']:
            print('로그: 레코드 이벤트 통과')
            # 각 레코드에는 이벤트 정보가 들어있음
            # UPDATE, REMOVE 등 다른 이벤트에 대한 처리도 작성 가능
            if record['eventName'] == 'INSERT':
                # INSERT 이벤트 처리 로직 작성
                # record['dynamodb']['NewImage']에서 새로운 아이템의 데이터에 접근 가능
                new_item = record['dynamodb']['NewImage']
                # 여기에 원하는 작업 수행
                print("새로운 아이템이 추가되었습니다:", new_item)
                # DynamoDB 이벤트에서 데이터 가져오기
                combinedData = new_item
        # 입력 값들을 합치기
        #combined_data = f"{input_data1} {input_data2} {input_data3}" if input_data3 else f"{input_data1} {input_data2} 0"

        # 응답 생성
        response = {
            'statusCode': 200,
            'headers': response_headers,
            'body': json.dumps({'message': combinedData})
        }

        return response

    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return {
            'statusCode': 500,
            'headers': response_headers,
            'body': json.dumps({'error': str(e)})
        }
