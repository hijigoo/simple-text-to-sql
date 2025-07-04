import boto3
import json
import pandas as pd

def generate_response(question, sql_query, query_result,
                     model_id='apac.anthropic.claude-3-7-sonnet-20250219-v1:0',
                     region_name='ap-northeast-2'):
    """
    Generate a natural language response to the user's question based on the SQL query and its results.
    
    Args:
        question (str): The original user question in natural language
        sql_query (str): The SQL query that was generated and executed
        query_result (pd.DataFrame): The result of executing the SQL query
        model_id (str): The AWS Bedrock model ID to use
        region_name (str): AWS region name
        
    Returns:
        str: Generated natural language response
    """
    bedrock = boto3.client('bedrock-runtime', region_name=region_name)
    
    # Convert DataFrame to formatted string for better readability
    if isinstance(query_result, pd.DataFrame):
        result_str = query_result.to_string(index=False)
    else:
        result_str = str(query_result)
    
    message = f"""
당신은 데이터베이스 전문가이자 친절한 비서입니다.
사용자의 질문에 대해 SQL 쿼리를 실행한 결과를 바탕으로 자연스러운 한국어로 답변을 제공합니다.
기술적인 용어는 최소화하고 일반 사용자가 이해하기 쉽게 설명하세요.
사용자의 질문과 관련된 인사이트나 흥미로운 점이 있다면 함께 언급해주세요.

다음 정보를 바탕으로 응답을 생성하세요:

사용자 질문: {question}
실행된 SQL 쿼리: {sql_query}
쿼리 실행 결과:
{result_str}

SQL 쿼리나 기술적 세부사항을 포함하지 말고 자연스러운 대화체로 답변하세요.
"""
    
    response = bedrock.converse(
        modelId=model_id,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": message,
                    }
                ]
            }
        ],
        system=[
            {
                "text": "사용자 질문에 대한 답변을 생성해주세요."
            }
        ],
        inferenceConfig={
            "maxTokens": 2048,
            "temperature": 0.7
        }
    )
    
    return response['output']['message']['content'][0]['text']
