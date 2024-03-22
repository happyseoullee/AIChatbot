import json
import boto3
import random

def lambda_handler(event, context):
    try:
        # 사용자가 입력한 PIN과 Question 값 가져오기
        #pin = event['pin']
        #question = event['question']
        
        # API Gateway에서 전달된 데이터 가져오기
        pin = json.loads(event['body'])['pin']
        question = json.loads(event['body'])['question']
        
        # DynamoDB 위치 설정
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
        table = dynamodb.Table('acs-test-dynamoDB')

        # 입력한 PIN과 Question 값으로 DynamoDB에서 해당 항목 찾기
        response = table.get_item(Key={'Pin': pin, 'Question': question})
        item = response.get('Item')

        if not item:
            raise ValueError("No item found matching the provided PIN and Question.")
        
        # answer 키 생성 (랜덤값으로 채우기)
        answer_value = str(random.randint(1, 100))

        # DynamoDB 업데이트
        table.update_item(
            Key={'Pin': pin, 'Question': question},
            UpdateExpression='SET answer = :val',
            ExpressionAttributeValues={':val': answer_value}
        )

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'Answer key generated and updated successfully', 'answer': answer_value})
        }

    except Exception as e:
        error_message = str(e)
        print(f"An error occurred: {error_message}")
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': error_message})
        }
