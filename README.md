# Simple Text-to-SQL

자연어 질문을 SQL 쿼리로 변환하는 시스템으로, Amazon Bedrock의 언어 모델을 활용하여 데이터베이스 질의를 자동화합니다. 이 시스템은 SQLite 데이터베이스 스키마 정보를 추출하고, 자연어 질문을 SQL로 변환한 후, 결과를 다시 자연어로 응답합니다.

## 주요 기능

- 자연어 질문을 최적화된 SQL 쿼리로 변환
- 두 가지 방식의 데이터베이스 스키마 정보 추출:
  - 네이티브 SQLite 접근법
  - LangChain의 SQLDatabase 유틸리티
- 다양한 Amazon Bedrock 모델 지원 (Claude-3 등)
- 생성된 SQL 쿼리 실행 및 결과 조회
- 질의 결과를 바탕으로 자연어 응답 생성
- CSV 파일을 SQL 및 SQLite DB로 변환

## 프로젝트 구조

```
lg-ensol-text2sql/
│
├── main.py                        # 메인 실행 파일
├── README.md                      # 프로젝트 설명서
├── requirements.txt               # 필수 패키지 목록
│
├── data/                          # 데이터 파일 디렉토리
│   ├── products_test_data.csv     # 샘플 제품 데이터 CSV
│   ├── products_test_data.db      # 생성된 SQLite DB 파일
│   └── products_test_data.sql     # 생성된 SQL 스크립트 파일
│
└── src/                           # 소스 코드 디렉토리
    ├── csv_converter.py           # CSV 변환 유틸리티
    ├── execute_query.py           # SQL 쿼리 실행 모듈
    ├── response_generator.py      # 자연어 응답 생성 모듈
    ├── schema_extractor.py        # 스키마 추출 유틸리티
    └── sql_generator.py           # SQL 생성 모듈
```

## 요구사항

- Python 3.8 이상
- boto3
- pandas
- langchain 및 langchain-community (LangChain 스키마 추출 사용 시 필요)
- AWS 계정 및 Bedrock 접근 권한
- AWS CLI 구성 및 적절한 자격 증명

## 설치 방법

1. 레포지토리 복제:
   ```bash
   git clone https://github.com/yourusername/lg-ensol-text2sql.git
   cd lg-ensol-text2sql
   ```

2. 가상 환경 설정:

   **Linux/macOS:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. 필수 패키지 설치:
   ```bash
   pip install -r requirements.txt
   ```

4. AWS 자격 증명 구성:
   ```bash
   aws configure
   ```
   AWS 자격 증명이 Amazon Bedrock에 접근할 수 있는지 확인하세요.

## 사용 방법

### CSV 기반 Text-to-SQL 전체 워크플로우 실행

이 시스템은 CSV 파일을 시작점으로 하여 완전한 Text-to-SQL 파이프라인을 실행합니다:

1. **CSV → SQL/DB 변환**: CSV 파일을 SQL 스크립트와 SQLite 데이터베이스로 변환
2. **스키마 추출**: 생성된 데이터베이스에서 테이블 구조 정보 추출
3. **자연어 → SQL 변환**: 사용자 질문을 SQL 쿼리로 변환
4. **쿼리 실행**: 생성된 SQL을 데이터베이스에서 실행
5. **자연어 응답 생성**: 쿼리 결과를 바탕으로 사용자 친화적인 응답 생성

#### 기본 사용법

```bash
# 전체 워크플로우 실행 (기본 products_test_data.csv 사용)
python main.py

# 사용자 지정 CSV 파일로 워크플로우 실행
python main.py --csv ./path/to/your_data.csv

# 특정 데이터베이스 파일 경로 지정
python main.py --csv ./data/my_data.csv --db ./data/my_database.db
```

#### 실행 과정

1. **데이터 변환 단계**:
   - CSV 파일 분석 및 데이터 타입 자동 감지
   - SQL 스크립트 파일(.sql) 생성
   - SQLite 데이터베이스 파일(.db) 생성

2. **스키마 분석 단계**:
   - 네이티브 SQLite 방식으로 스키마 추출
   - LangChain 방식으로 스키마 추출 (선택적)
   - 테이블 구조, 컬럼 정보, 데이터 타입 파악

3. **대화형 질의 단계** (향후 확장 가능):
   - 자연어 질문 입력
   - Amazon Bedrock을 통한 SQL 쿼리 생성
   - 쿼리 실행 및 결과 조회
   - 자연어 응답 생성

### 직접 모듈 사용

```python
from src.csv_converter import convert_csv_to_sql_and_db
from src.schema_extractor import get_schema_native, get_schema_langchain
from src.sql_generator import generate_sql
from src.execute_query import execute_and_display
from src.response_generator import generate_response

# CSV를 SQL 및 DB 파일로 변환
convert_csv_to_sql_and_db('data.csv', 'data.sql', 'data.db')

# 스키마 추출
schema = get_schema_native('data.db')
dialect, schema_langchain = get_schema_langchain('data.db')

# SQL 쿼리 생성
query = "가장 비싼 제품은 무엇인가요?"
sql_query = generate_sql(query, schema_langchain, dialect)

# 쿼리 실행
result = execute_and_display('data.db', sql_query)

# 응답 생성
response = generate_response(query, sql_query, result)
```

## 질문 예시

시스템은 다음과 같은 질문을 처리할 수 있습니다:

- "가격이 100만원 이상인 모든 제품을 보여줘"
- "가장 비싼 상위 5개 제품은?"
- "전자제품 카테고리의 모든 제품을 가격 순으로 정렬해서 보여줘"
- "각 카테고리별 제품 수를 계산해줘"
- "5개 이상의 제품이 있는 브랜드별 평균 가격을 찾아줘"
- "어떤 브랜드가 가장 높은 평균 평점을 가지고 있어?"
- "재고가 가장 많이 남은 제품 이름 10개 알려줘"

## 지원되는 Bedrock 모델

다음 모델을 사용할 수 있습니다 (AWS 계정에서 활성화되어 있어야 함):

- `apac.anthropic.claude-3-7-sonnet-20250219-v1:0` (기본값)
- `anthropic.claude-v2`
- `anthropic.claude-3-sonnet-20240229-v1:0`
- `anthropic.claude-3-haiku-20240307-v1:0`

## 스키마 추출 방식 선택

스키마 추출을 위한 두 가지 방법이 지원됩니다:

1. **네이티브** (기본): SQLite의 PRAGMA 명령을 사용하여 스키마 정보 추출
2. **LangChain**: LangChain의 SQLDatabase 유틸리티 사용

필요에 따라 적합한 방식을 선택하세요.
