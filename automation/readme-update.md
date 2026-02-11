# README.md 업데이트 자동화

> 프로젝트 구조나 기능이 변경될 때 README.md를 최신 상태로 유지하는 절차

## 트리거 요청

- "README 업데이트해줘"
- "README 최신화해줘"
- "프로젝트 구조 바뀐 거 README에 반영해줘"
- "아키텍처 문서 업데이트해줘"

---

## 업데이트가 필요한 상황

| 변경 유형 | 업데이트 대상 섹션 |
|----------|-----------------|
| 새 파일/폴더 추가 | `4. 프로젝트 구조` 트리 |
| 새 기능 구현 완료 | `1. 현재 단계` 완료 항목 체크 |
| 브리핑 유형 변경 | `6. 일일 마켓 브리핑` 브리핑 유형/구성 표 |
| GitHub Actions 스케줄 변경 | `5. 폴더별 상세` GitHub Actions 섹션 |
| plan 파일 추가/완료 | `5. 폴더별 상세` plan 목록 |
| 데이터 파이프라인 구조 변경 | `4-1. 아키텍처 시각화` 다이어그램 |
| API/데이터 소스 추가 | `3. 기술 스택` 데이터 수집 API 표 |
| 관심 종목 변경 | `notes/watchlist.md` (README.md 직접 수정 아님) |

---

## 실행 절차

### Step 1: 변경 범위 파악

```bash
cd "c:\Users\robin\OneDrive\바탕 화면\trading-sandbox\trading-sandbox"
git log --oneline -10
```

최근 커밋을 보고 어떤 변경이 있었는지 파악합니다.

### Step 2: 현재 폴더 구조 확인

```bash
ls -la scripts/
ls -la scripts/collectors/
ls -la plan/
ls -la docs/learning/
ls -la notes/
ls -la hooks/
ls -la automation/
```

실제 파일 목록을 확인하여 README의 트리와 비교합니다.

### Step 3: README.md 수정

수정이 필요한 섹션만 선택적으로 업데이트합니다.

**수정 원칙**:
- 섹션 4 (프로젝트 구조 트리): 실제 파일 구조와 일치하도록
- 섹션 4-1 (아키텍처 시각화): 데이터 흐름이나 레이어 구조가 바뀔 때만
- 섹션 1 (현재 단계): 기능 완료 시 `[ ]` → `[x]` 체크
- 마지막 업데이트 날짜: 항상 오늘 날짜로 갱신

**수정하지 않는 것**:
- 관심 종목 목록 → `notes/watchlist.md`에서 관리
- 프로젝트 목적/로드맵 (사용자 직접 업데이트)

### Step 4: 커밋

```bash
git add README.md
git commit -m "docs: README.md 구조 최신화 (YYYY-MM-DD)"
git push
```

---

## 체크리스트 (빠른 점검)

- [ ] 새로 생긴 파일이 트리에 없는 것 없나?
- [ ] 삭제된 파일이 트리에 남아있나?
- [ ] plan 파일명 (01~05) 최신 상태인가?
- [ ] GitHub Actions 스케줄 현행화?
- [ ] 완료된 기능이 `[x]` 체크 되어 있나?
- [ ] 마지막 업데이트 날짜 갱신했나?

---

*마지막 업데이트: 2026년 2월 11일*
