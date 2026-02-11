# 개발 원칙 (CLAUDE.md)

이 파일은 Claude Code가 이 프로젝트에서 작업할 때 반드시 따르는 원칙을 정의합니다.

---

## 새 기능 개발 순서

1. `plan/` 폴더에 설계 문서 작성 (기존 템플릿: `plan/templates/feature-design.md` 참고)
2. 사용자 승인 후 구현 시작
3. 기존 관련 파일을 모두 읽은 뒤 수정 시작
4. 수정 완료 후 관련 `docs/` 문서 업데이트
5. GitHub 커밋

## 금지 사항

- `plan/` 없이 100줄 이상의 코드 변경 금지
- `config/settings.py` 변경 시 반드시 `.env.example`도 함께 확인
- `scripts/briefing_generator.py`의 AI 프롬프트 수정 시 `plan/` 선행 필수

---

## 프로젝트 구조 요약

```
trading-sandbox/
├── scripts/
│   ├── main.py                  # CLI 진입점 (--type morning/midday/aftermarket)
│   ├── briefing_generator.py    # 핵심 파이프라인 (수집 → AI 분석 → 저장)
│   └── collectors/
│       ├── dart_collector.py    # 공시 수집 (DART API)
│       ├── krx_collector.py     # 주가 수집 (pykrx)
│       ├── ecos_collector.py    # 거시경제 수집 (ECOS API + FRED)
│       └── news_collector.py    # 뉴스 수집 (RSS)
├── config/settings.py           # 중앙 설정 (환경변수 로드)
├── plan/                        # 개발 계획 문서 (작업 전 먼저 확인)
├── docs/                        # 학습 자료 및 참고 문서
├── hooks/                       # Claude Code 작업 지침 (자동화 코드 아님)
├── automation/                  # 로컬 자동화 스크립트
├── notes/daily_briefing/        # 생성된 브리핑 저장 위치
└── .github/workflows/           # GitHub Actions (실제 스케줄 자동화)
```

## 데이터 흐름

```
main.py --type [morning/midday/aftermarket]
  ↓
briefing_generator.py collect_all_data()
  ├── dart_collector  (순차 실행, Phase 2에서 병렬화 예정)
  ├── krx_collector
  ├── ecos_collector
  └── news_collector
  ↓
generate_with_ai() or generate_basic_briefing()
  ↓
notes/daily_briefing/YYYY-MM-DD_XX브리핑.md 저장
```

## 주요 설정값

- **관심 종목**: `WATCHLIST_STOCKS` (settings.py / .env / GitHub Actions)
- **AI 활성화**: `AI_ENABLED=true/false` (.env 또는 GitHub Actions Repository Variables)
- **AI 모델**: `AI_MODEL` (기본값: gpt-4o-mini)

## 진행 중인 계획

| 파일 | 주제 | 상태 |
|------|------|------|
| `plan/daily-briefing-expansion.md` | 일일 브리핑 자동화 확장 | 🔄 진행 중 |
| `plan/skills-insight-application.md` | Skills 인사이트 적용 | 🔄 진행 중 |
| `plan/ipo-system.md` | 공모주 일정 자동화 | 📝 계획 중 |
| `plan/pain-points-improvement.md` | 투자 불편 사항 개선 | 📝 계획 중 |
| `plan/kis-api-customization.md` | 증권사 API 커스터마이징 | 📝 계획 중 |

---

*마지막 업데이트: 2026년 2월 11일*
