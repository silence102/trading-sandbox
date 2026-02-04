# PyKRX 라이브러리 면책 및 주의사항

## 개요

- **라이브러리**: PyKRX
- **GitHub**: https://github.com/sharebook-kr/pykrx
- **용도**: 한국 증권시장(KRX, Naver)에서 주식·채권 데이터를 스크래핑하는 Python 라이브러리

---

## 면책 및 주의사항 (공식)

> 아래 내용은 PyKRX 공식 GitHub에서 발췌한 주의사항입니다.

### 1. 데이터 저작권
- 본 라이브러리는 **KRX(한국거래소) 및 Naver의 데이터를 스크래핑**하며, **데이터의 저작권은 각 제공처에 있습니다.**

### 2. API 호출 제한
- 도의적으로 **무분별한 API 호출을 자제**해 주시기 바랍니다.

### 3. 데이터 정확성
- 제공되는 데이터는 **공식 데이터와 차이가 있을 수 있으며**, 참고용으로만 사용해야 합니다.

### 4. 투자 손실 및 법적 책임
- **투자 손실이나 법적 책임은 사용자에게 있으며**, 상업적 용도 사용 시 데이터 제공처의 약관을 준수해야 합니다.

### 5. 후원 관련
- 후원은 데이터에 대한 대가가 아니며, **오픈소스 유지보수를 위한 개발자 응원** 목적으로만 사용됩니다.

---

## 본 프로젝트에서의 사용 현황

| 항목 | 내용 |
|------|------|
| 사용 목적 | 개인 학습 및 투자 분석 |
| 현재 수익화 여부 | **없음** (개인 프로젝트) |
| 향후 가능성 | 장기적으로 서비스화 검토 가능 |

---

## 수익화 시 고려사항

향후 상업적 서비스로 발전할 경우 다음 사항을 검토해야 합니다:

### 1. 데이터 출처별 이용약관 확인
- **KRX (한국거래소)**: 정보 이용 약관 확인 필요
- **Naver 금융**: 서비스 이용약관 확인 필요

### 2. 대안 검토
- **KRX OPEN API** (공식): https://openapi.krx.co.kr/
  - 공식 API로 상업적 이용 조건 명확
- **금융위원회 공공데이터**: https://www.data.go.kr/
  - 공공데이터로 상업적 이용 가능

### 3. 스크래핑 vs 공식 API
| 방식 | 장점 | 단점 |
|------|------|------|
| PyKRX (스크래핑) | 간편, 무료 | 저작권 불명확, 차단 위험 |
| KRX OPEN API | 공식, 안정적 | API 키 필요, 호출 제한 |

---

## 대안 API 상세 가이드

### 1. KRX OPEN API (한국거래소 공식)

**URL**: https://openapi.krx.co.kr/

**특징:**
- 한국거래소에서 공식 제공하는 API
- 상업적 이용 조건이 명확함
- REST API 방식

**가입 및 사용 방법:**
1. https://openapi.krx.co.kr/ 접속
2. 회원가입 (공인인증서 또는 휴대폰 인증)
3. API 키 신청 및 발급
4. 제공 데이터: 시세, 지수, 공시, 투자분석정보(SMILE) 등

**무료 플랜:**
- 일일 호출 제한 있음 (정확한 수치는 가입 후 확인)
- 개인/비상업적 용도는 무료

**코드 예시:**
```python
import requests

API_KEY = "your_krx_api_key"
url = "https://openapi.krx.co.kr/svc/v1/endpoint"
headers = {"Authorization": f"Bearer {API_KEY}"}

response = requests.get(url, headers=headers)
data = response.json()
```

---

### 2. 금융위원회 공공데이터 (data.go.kr)

**URL**: https://www.data.go.kr/

**주요 데이터셋:**
- 금융위원회_주식시세정보
- 금융위원회_KRX상장종목정보
- 금융위원회_기업기본정보

**특징:**
- 공공데이터로 상업적 이용 가능
- 무료
- REST API 방식

**가입 및 사용 방법:**
1. https://www.data.go.kr/ 회원가입
2. 원하는 데이터셋 검색 (예: "주식시세")
3. "활용신청" 클릭
4. API 키 즉시 발급 (자동 승인)

**코드 예시:**
```python
import requests

SERVICE_KEY = "your_data_go_kr_key"
url = "http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo"
params = {
    "serviceKey": SERVICE_KEY,
    "numOfRows": 10,
    "resultType": "json"
}

response = requests.get(url, params=params)
data = response.json()
```

---

### 3. KRX 정보데이터시스템 (수동 다운로드)

**URL**: http://data.krx.co.kr/

**특징:**
- API 없이 웹에서 직접 데이터 다운로드
- Excel, CSV 형식 제공
- 자동화하려면 스크래핑 필요 (권장하지 않음)

**사용 방법:**
1. http://data.krx.co.kr/ 접속
2. 원하는 데이터 카테고리 선택
3. 조건 설정 후 "조회" 클릭
4. Excel/CSV 다운로드

---

### 4. 대안별 비교 요약

| 대안 | 상업적 이용 | API 방식 | 비용 | 난이도 |
|------|------------|---------|------|--------|
| KRX OPEN API | ✅ 명확 | REST | 무료 (제한) | 중간 |
| 공공데이터포털 | ✅ 가능 | REST | 무료 | 낮음 |
| KRX 데이터시스템 | ⚠️ 확인필요 | 수동 | 무료 | 낮음 |
| PyKRX | ⚠️ 불명확 | 스크래핑 | 무료 | 매우 낮음 |

---

### 5. 전환 시 코드 수정 포인트

현재 프로젝트에서 PyKRX → 공식 API로 전환 시 수정이 필요한 파일:

```
scripts/collectors/krx_collector.py
```

**전환 방법:**
1. 새로운 collector 파일 생성 (예: `krx_official_collector.py`)
2. 기존 `KrxCollector` 클래스와 동일한 인터페이스 유지
3. `config/settings.py`에서 사용할 collector 선택 가능하도록 설정
4. 테스트 후 기존 코드 대체

---

## 결론

**현재 단계 (개인 학습):**
- PyKRX 사용에 법적 문제 없음
- 참고용으로 활용하며 투자 판단은 본인 책임

**향후 수익화 시:**
- KRX OPEN API 등 공식 API로 전환 검토
- 데이터 제공처 이용약관 준수 필수

---

## 참고 링크

- [PyKRX GitHub](https://github.com/sharebook-kr/pykrx)
- [KRX OPEN API](https://openapi.krx.co.kr/)
- [KRX 정보데이터시스템](http://data.krx.co.kr/)
- [금융위원회 공공데이터](https://www.data.go.kr/)

---

*기록일: 2026년 2월 4일*
