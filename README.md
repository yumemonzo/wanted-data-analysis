# Wanted Data Analysis Project

이 프로젝트는 특정 직무에 대해 원티드로부터 데이터를 얻어, 해당 직무에 대한 채용 공고를 시각화하는 프로젝트입니다.

## Env setting

이 프로젝트는 Docker 환경에서 실행됩니다. 아래 명령어를 통해 Docker 이미지를 빌드하고, 컨테이너를 실행합니다.

```bash
docker build -t wanted_data_analysis:main .
docker run --net=host --ipc=host --name wanted_data_analysis -dit wanted_data_analysis:main /bin/bash
```

## Usage
데이터 수집 및 분석 서버 실행 방법은 다음과 같습니다.
1. 크롤링 실행  
데이터 수집을 위해 ```crawling.py``` 스크립트를 실행합니다. 이는 ```config/crawling.yaml``` 설정 파일을 참조하여 수집할 데이터를 설정합니다.
    ```bash
    python3 crawling.py
    ```
2. 시각자료 생성  
시각자료 생성을 위해 ```data_analysis.py``` 스크립트를 실행합니다. 이는 ```config/data_analysis.yaml``` 설정 파일을 참조하여 데이터 전처리를 진행합니다.
    ```bash
    python3 data_analysis.py
    ```
3. FastAPI 서버 실행  
분석된 데이터를 시각화하는 웹 애플리케이션을 실행합니다. uvicorn 명령을 통해 FastAPI 서버를 실행하여 분석 결과를 웹에서 확인할 수 있습니다.
    ```bash
    uvicorn app:app --reload
    ```

## Config

프로젝트는 다음 두 개의 YAML 설정 파일을 사용하여 유연하게 구성됩니다.

### 1. `data_analysis.yaml`

이 파일은 데이터 분석 과정에 필요한 설정을 정의합니다. 주로 텍스트 전처리와 관련된 설정이 포함되어 있으며, `stopwords`와 `keep_phrases` 설정을 통해 텍스트 분석 시 제외하거나 유지할 단어를 지정할 수 있습니다. 주요 섹션은 다음과 같습니다:

- **`main_job`** - 주요 업무 분석에 사용될 설정 (불용어, 유지할 구절 포함)
- **`check_list`** - 자격 요건 분석 설정
- **`good_list`** - 우대 사항 분석 설정

각 섹션은 분석하려는 텍스트의 **불용어(`stopwords`)**와 **유지할 구(`keep_phrases`)**를 정의하여, 분석 결과가 보다 정확하게 나타나도록 합니다.

### 2. `crawling.yaml`

이 파일은 크롤링 설정을 포함합니다. 크롤링 시 사용할 **검색어(`job_name`)**가 포함되어 있습니다.

- **`job_name`** - 크롤링할 직무 이름 (예: "데이터 분석가")

이 설정을 통해 특정 직무에 대한 데이터를 효율적으로 수집할 수 있습니다.
