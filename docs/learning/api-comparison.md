# 한국투자증권 vs 키움증권 Open API 비교 분석

> 개인 사용자의 자동매매 서비스 개발 관점에서 두 증권사 API를 비교 분석합니다.

## 1. 개요

| 구분 | 한국투자증권 (KIS Developers) | 키움증권 (Open API+) |
|------|------------------------------|---------------------|
| API 방식 | **REST API** (서버사이드) | **OCX 컨트롤** + REST API (2025~) |
| HTS 접속 | **불필요** | 기존: 필요 / REST API: 불필요 |
| 운영체제 | Windows, Mac, Linux 모두 지원 | 기존: Windows 전용 / REST API: 모두 지원 |
| 출시 시기 | 2022년 | 기존: 오래됨 / REST API: 2025년 3월 |

## 2. 아키텍처 비교

### 한국투자증권 KIS Developers
```
[사용자 프로그램] → REST API 요청 → [한국투자증권 서버]
                 ← JSON 응답 ←
```
- **서버사이드 구조**: 증권사 최초
- OCX 객체 생성 불필요
- 어떤 프로그래밍 언어에서도 사용 가능

### 키움증권 Open API+
```
[사용자 프로그램] → OCX 컨트롤 → [키움증권 서버]
                 ← 이벤트 콜백 ←
```
- **클라이언트사이드 구조** (기존)
- Windows 환경 필수 (기존)
- 2025년 REST API 추가로 서버사이드도 지원

## 3. 주요 기능 비교

| 기능 | 한국투자증권 | 키움증권 |
|------|-------------|---------|
| 국내 주식 매매 | ✅ | ✅ |
| 해외 주식 매매 | ✅ | ✅ |
| 국내 파생상품 | ✅ | ✅ |
| 해외 파생상품 | ✅ | ❌ |
| 실시간 시세 | ✅ (WebSocket) | ✅ |
| 조건검색 | ❌ | ✅ (HTS 조건식 연동) |
| 금현물 거래 | ❌ | ✅ (2025년 9월~) |
| AI 코딩 어시스턴트 | ❌ | ✅ (2025년 5월~) |

## 4. 개발 환경 비교

### 한국투자증권
| 항목 | 내용 |
|------|------|
| 지원 언어 | Python, Java, Kotlin, 엑셀 VBA 등 모든 언어 |
| 인증 방식 | AppKey + AppSecret → OAuth Token |
| 실시간 데이터 | WebSocket |
| 공식 라이브러리 | [open-trading-api](https://github.com/koreainvestment/open-trading-api) |
| 커뮤니티 라이브러리 | [python-kis](https://github.com/Soju06/python-kis), [kt_kisopenapi](https://github.com/devngho/kt_kisopenapi) |
| AI 연동 | ChatGPT, Claude 등 LLM 환경 연동 지원 |

### 키움증권
| 항목 | 내용 |
|------|------|
| 지원 언어 | 기존: VB, MFC, 엑셀 (Windows) / REST API: 모든 언어 |
| 인증 방식 | 기존: 로그인 이벤트 / REST API: OAuth Token |
| 실시간 데이터 | 이벤트 콜백 |
| 공식 라이브러리 | 없음 |
| 커뮤니티 라이브러리 | [pykiwoom](https://wikidocs.net/book/1173), [KOAPY](https://github.com/elbakramer/koapy) |
| AI 연동 | AI 코딩 어시스턴트 (자연어 → 코드 생성) |

## 5. 장단점 분석

### 한국투자증권 KIS Developers

#### 장점
1. **크로스플랫폼**: Mac, Linux에서도 개발 가능
2. **REST API 기본 제공**: 현대적인 API 설계
3. **HTS 불필요**: 순수 서버 통신만으로 동작
4. **해외 파생상품 지원**: 해외 선물/옵션 거래 가능
5. **공식 GitHub 지원**: 샘플 코드 및 문서 충실
6. **LLM 친화적**: AI 에이전트와 연동 용이

#### 단점
1. **조건검색 미지원**: HTS 조건식 연동 불가
2. **금현물 거래 미지원**: KRX 금시장 거래 불가
3. **상대적으로 짧은 역사**: 2022년 출시로 레퍼런스 적음

### 키움증권 Open API+

#### 장점
1. **조건검색 기능**: HTS에서 만든 조건식 활용 가능
2. **금현물 거래**: KRX 금시장 자동매매 지원
3. **AI 코딩 어시스턴트**: 자연어로 코드 생성 가능
4. **오랜 역사**: 풍부한 레퍼런스와 커뮤니티
5. **REST API 추가**: 2025년부터 크로스플랫폼 지원

#### 단점
1. **기존 API Windows 전용**: OCX 컨트롤 방식의 한계
2. **해외 파생상품 미지원**: 해외 선물/옵션 불가
3. **조건검색 제한**: 실시간 조건검색 10개, 100종목 제한
4. **호출 제한**: 조건검색 1초 5회, 1분 1회 제한

## 6. 사용 시나리오별 추천

### 🏆 한국투자증권 KIS Developers 추천

| 시나리오 | 이유 |
|---------|------|
| Mac/Linux 개발 환경 | REST API 기본 지원 |
| 해외 파생상품 거래 | 해외 선물/옵션 지원 |
| AI 에이전트 연동 | LLM 친화적 설계 |
| 서버 기반 자동매매 | 순수 REST API로 구현 가능 |
| 클라우드 배포 | HTS 불필요로 서버 환경에 적합 |

### 🏆 키움증권 Open API+ 추천

| 시나리오 | 이유 |
|---------|------|
| HTS 조건검색 활용 | 조건식 연동 기능 |
| 금현물 자동매매 | KRX 금시장 API 지원 |
| 프로그래밍 비전문가 | AI 코딩 어시스턴트 활용 |
| 기존 키움 사용자 | 익숙한 환경, 풍부한 레퍼런스 |

## 7. 결론 및 권장 사항

### 개인 사용자 자동매매 서비스 개발 기준

| 우선순위 | 추천 증권사 | 이유 |
|---------|------------|------|
| **1순위** | **한국투자증권** | REST API 기본 제공, 크로스플랫폼, AI 연동 용이, 서버 배포 친화적 |
| 2순위 | 키움증권 (REST API) | 조건검색 필요 시, 금현물 거래 필요 시 |

### 최종 권장

**한국투자증권 KIS Developers**를 1순위로 권장합니다.

**이유:**
1. 현대적인 REST API 설계로 개발 진입 장벽이 낮음
2. Mac, Linux 환경에서도 개발 가능하여 유연성 확보
3. HTS 없이 순수 API만으로 동작하여 서버 환경 배포 용이
4. 공식 GitHub에서 ChatGPT, Claude 등 AI 연동 샘플 제공
5. 해외 파생상품까지 지원하여 확장성 우수

단, **HTS 조건검색 기능이 필수**이거나 **금현물 거래**가 필요한 경우 키움증권을 고려해야 합니다.

---

## 참고 자료

### 한국투자증권
- [KIS Developers 공식 사이트](https://apiportal.koreainvestment.com/intro)
- [GitHub - open-trading-api](https://github.com/koreainvestment/open-trading-api)
- [WikiDocs - 오픈API 트레이딩 가이드](https://wikidocs.net/159296)
- [python-kis 라이브러리](https://github.com/Soju06/python-kis)

### 키움증권
- [키움 Open API+ 공식 안내](https://www.kiwoom.com/h/customer/download/VOpenApiInfoView)
- [WikiDocs - 퀀트투자를 위한 키움증권 API](https://wikidocs.net/book/1173)
- [KOAPY 라이브러리](https://github.com/elbakramer/koapy)
- [키움증권 AI+API 기사](https://www.g-enews.com/article/Securities/2025/09/202509210936232372edf69f862c_1)

---

*마지막 업데이트: 2026년 2월 1일*
