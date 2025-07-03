import boto3
import json

def generate_sql(question, table_info, dialect,
                 model_id='apac.anthropic.claude-3-7-sonnet-20250219-v1:0',
                 region_name='ap-northeast-2'):
    bedrock = boto3.client('bedrock-runtime', region_name=region_name)
    
    system_message = f"""

당신은 {dialect} 전문가입니다.
회사의 데이터베이스에 대한 질문을 하는 사용자와 상호 작용하고 있습니다.
아래의 데이터베이스 스키마를 기반으로 사용자의 질문에 답할 SQL 쿼리를 작성하세요.
특정 테이블에서 모든 컬럼을 조회하지 마시고, 질문과 관련된 소수의 컬럼만 선택하여 조회하세요.
또한, 각 컬럼이 어떤 테이블에 속해 있는지도 반드시 확인하세요.

데이터베이스 스키마는 다음과 같습니다.
<schema> {table_info} </schema>

SQL 쿼리만 작성하고 다른 것은 작성하지 마세요.
SQL 쿼리를 다른 텍스트로 묶지 마세요. 심지어 backtick 으로도 묶지 마세요.

예시:
Question: 10명의 고객 이름을 보여주세요.
SQL Query: SELECT Name FROM Customers LIMIT 10;

Your turn:
Question: {question}
SQL Query:
"""
    
    response = bedrock.converse(
        modelId=model_id,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": question
                    }
                ]
            }
        ],
        system=[
            {
                "text": system_message
            }
        ],
        inferenceConfig={
            "maxTokens": 1024
        }
    )
    
    return response['output']['message']['content'][0]['text']