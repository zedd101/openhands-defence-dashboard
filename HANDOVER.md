# 📋 프로젝트 업무 인수인계서 (Handover Document)

---

## 1. 기본 정보 및 문서 개요

* **프로젝트명 :** 방산 구매·납기 통합 관리 대시보드 (Defense Procurement & Delivery Integrated Dashboard)
* **저장소 위치 :** `C:\workspace\04-dashboard`
* **GitHub 저장소 :** [https://github.com/zedd101/openhands-defence-dashboard](https://github.com/zedd101/openhands-defence-dashboard)
* **기준 작성일 :** 2026년 9월 16일 (최신 버전 기준)
* **인수인계 대상 :** 프로젝트 담당자, 운영 관리자, 현업 팀장 및 후속 개발자
* **핵심 목적 :** 협력사 부품 조달 지연과 군납 계약 일정을 통합 모니터링하고, 방위사업청 공개 조달 트렌드 분석 및 팀원 간 실시간 클라우드 협업(Supabase DB)을 지원하는 웹 대시보드의 운영·유지보수 가이드 전달

---

## 2. 시스템 아키텍처 및 기술 환경

```text
[사용자 환경] Chrome / Edge 최신 브라우저 (PC 및 모바일 반응형 지원)
     │
     ├─▶ [로컬 실행] docs/index.html 더블클릭 (file:/// 프로토콜 100% 무장애 구동)
     └─▶ [웹 클라우드 배포] Vercel Hosting (https://*.vercel.app, vercel.json 라우팅)
            │
            ├─▶ [정적 데이터 로드] HTML <script src="..."> 태그를 통한 표준 전역 변수 로드
            │     ├── docs/data.js   : 가상 방산 계약(12건), 부품발주(14건), 수출허가(7건)
            │     ├── docs/rate.js   : 유럽중앙은행 기준 USD/KRW 실시간 환율
            │     └── docs/public.js : 방위사업청 실제 계약 체결 내역 (1,870건)
            │
            ├─▶ [동적 데이터 연동] Supabase BaaS (PostgreSQL 클라우드 DB)
            │     ├── localStorage 기반 Project URL & Anon Key 보관 (보안 격리)
            │     ├── contracts 테이블     : 실시간 판매 계약 조회 및 신규 등록
            │     └── public_notes 테이블  : 공공데이터 실무 검토 메모 & 대응 상태 연동
            │
            └─▶ [데이터 수집 파이썬 ETL]
                  ├── fetch_rate.py   : 유럽중앙은행(Frankfurter) API 환율 자동 수집
                  └── fetch_public.py : 공공데이터포털 방위사업청 계약 내역 자동 수집
```

### 📌 핵심 기술적 제약 및 준수 원칙
1. **외부 의존성 제로 (No External Libraries) :**  
   Bootstrap, Tailwind, jQuery, Chart.js, React 등 외부 라이브러리와 CDN 링크를 일체 사용하지 않고 **100% 바닐라 HTML5, CSS3, JavaScript**로만 구현되었습니다. (보안망 차단 및 네트워크 지연 원천 차단)
2. **`fetch()` 파일 호출 금지 :**  
   로컬 파일(`file:///`) 환경에서 브라우저 CORS 보안 에러를 유발하는 `fetch()` 대신 표준 `<script>` 태그 로드 방식을 엄수합니다.
3. **무장애 자동 폴백 (Graceful Degradation) :**  
   인터넷이 끊기거나 Supabase DB가 연결되지 않은 상태에서도 에러 창 없이 기존 로컬 가상 데이터로 100% 정상 작동합니다.

---

## 3. 구현 기능 상세 내역 (완료 작업 요약)

### ① 탭 1 : 방산 구매·납기 통합 관리 (샘플 대시보드)
* **4대 핵심 KPI 카드 :** 수주잔고(4,501억원), 납기위협(적신호), 지연/리스크(황신호), 90일 내 납품 건수 실시간 집계
* **환율 연동 해외 수출액 환산 :** 실시간 USD/KRW 환율을 적용하여 해외 수출 사업 건에 대해 미화($) 환산 금액 병기
* **주간 보고 요약 복사 :** 현재 집계 수치 및 리스크 품목을 기반으로 5줄 정형화된 임원 보고 텍스트 자동 생성 및 원클릭 클립보드 복사
* **계약-발주-허가 다차원 연계 :** 계약 선택 시 하단에 종속된 협력사 조달 품목 및 수출허가 상태가 동적으로 상호작용

### ② 탭 2 : 공개 조달 동향 (방위사업청 공공데이터)
* **빅데이터 적재 :** 실제 방위사업청 계약 체결 내역 **1,870건** 탑재
* **육각 지표 카드 (Hexagon KPI) :** 총 계약액(1조 1,481억원), 평균 계약액, 최대 계약, 수의계약 비중(89.5%), 주력 품목 분석
* **순수 SVG 인터랙티브 차트 4종 :** 월별 계약 추이, 상위 5대 조달 품목, 계약 체결 방식 파이 차트, TOP 10 협력사 순위 차트
* **고속 검색 및 페이지네이션 :** 다중 조건 필터(계약방법, 금액대) 및 20건 단위 고성능 페이징 테이블

### ③ 클라우드 백엔드 연동 (Supabase)
* **[⚙️ DB 설정] UI 모달 :** 화면 우측 상단에서 URL과 Key를 입력받아 브라우저 `localStorage`에 암호화 보관
* **데이터 원클릭 마이그레이션 :** 기존 12건 가상 계약을 Supabase `contracts` 테이블로 원클릭 DB 업로드
* **[➕ 새 계약 등록] 실시간 추가 :** 모달을 통해 입력 시 Supabase에 즉시 Insert 및 대시보드 실시간 반영
* **공공데이터 실무 메모 & 대응 상태 연동 :** 1,870건 각 행에 **[📝 메모]** 버튼 구현, 5대 대응 상태(`검토중`, `입찰참여`, `제안서작성`, `패스`, `낙찰성공`) 및 실무 메모를 Supabase `public_notes` 테이블에 실시간 Upsert

### ④ Vercel 클라우드 웹 배포
* 프로젝트 루트에 `vercel.json`을 구성하여 `docs/` 디렉터리가 웹 서비스 루트로 정적 배포되도록 라우팅 완료
* GitHub `main` 브랜치 연동으로 커밋 푸시 시 자동 빌드/배포 환경 구축

---

## 4. 데이터베이스 스키마 및 설정 명세 (Supabase)

운영 환경에서 Supabase 프로젝트를 생성할 때 필요한 테이블 구조입니다:

### 1) `contracts` 테이블 (판매 계약)
| 컬럼명 | 데이터 타입 | 기본키(PK) | 설명 |
| :--- | :--- | :---: | :--- |
| `id` | `int8` (자동증가) | ✅ (또는 name) | 고유 식별자 |
| `contract_name` | `text` | - | 계약명 |
| `contractor` | `text` | - | 계약업체 / 수요기관 |
| `amount` | `int8` | - | 계약금액 (억원 단위) |
| `contract_date` | `date` | - | 계약 체결일자 |
| `contract_method` | `text` | - | 계약방법 (수의계약, 일반경쟁 등) |

### 2) `public_notes` 테이블 (공공데이터 실무 메모)
| 컬럼명 | 데이터 타입 | 기본키(PK) | 설명 |
| :--- | :--- | :---: | :--- |
| `contract_name` | `text` | ✅ (Primary) | 공공데이터 계약명 (공고 고유 식별) |
| `status` | `text` | - | 대응 상태 (검토중, 입찰참여, 제안서작성 등) |
| `memo` | `text` | - | 실무 검토 의견 및 한 줄 메모 |
| `updated_at` | `timestamptz` | - | 최종 수정 시각 (선택) |

### ⚠️ 중요 : Row Level Security (RLS) 설정 안내
* 교육 및 간이 실습 환경에서는 브라우저의 `anon` 키로 직접 읽기/쓰기가 가능해야 하므로, Supabase Table Editor에서 **`Enable Row Level Security (RLS)` 체크를 해제**하거나 아래 SQL을 실행해야 합니다:
  ```sql
  ALTER TABLE contracts DISABLE ROW LEVEL SECURITY;
  ALTER TABLE public_notes DISABLE ROW LEVEL SECURITY;
  ```

---

## 5. 디렉토리 및 주요 파일 역할 정의

```text
C:\workspace\04-dashboard\
│
├── docs/                      # [배포 루트] 브라우저 및 Vercel에서 서빙되는 정적 웹 디렉토리
│   ├── index.html             # 대시보드 메인 HTML (UI 레이아웃, 인라인 CSS 스타일, 바닐라 JS 엔진)
│   ├── data.js                # 가상 방산 데이터셋 (수정 금지, Fallback 원본)
│   ├── rate.js                # 최신 환율 정보 (RATE 전역 상수)
│   └── public.js              # 방사청 공공데이터 (PUBLIC_CONTRACTS 전역 배열)
│
├── fetch_rate.py              # 유럽중앙은행 환율 수집 파이썬 스크립트
├── fetch_public.py            # 방위사업청 계약 체결 내역 수집 파이썬 스크립트
├── vercel.json                # Vercel 배포 설정 (docs 디렉터리 지정)
│
├── AGENTS.md                  # AI 에이전트 작업 지침 및 절대 규칙 (인코딩, 커밋 지침 포함)
├── PRD.md                     # 제품 기획서 및 단계별 요구사항 명세
├── README.md                  # GitHub 및 사용자용 프로젝트 소개서
└── HANDOVER.md                # 본 업무 인수인계서
```

---

## 6. 운영 및 유지보수 작업 매뉴얼

### Q1. 환율 데이터를 최신으로 업데이트하려면?
```bash
python fetch_rate.py
```
* 실행 즉시 `docs/rate.js`가 최신 환율로 갱신되며, 이를 Git에 커밋하고 푸시하면 Vercel 배포 사이트에 10초 만에 반영됩니다.

### Q2. 방위사업청 공공데이터를 추가로 수집하려면?
```bash
# 기본 수집 (최근 1페이지)
python fetch_public.py

# 정밀 대량 수집 (수천 건 계약 수집)
python fetch_public.py --deep
```
* 수집 완료 시 `docs/public.js`가 자동으로 생성 및 교체됩니다.

### Q3. Git 커밋 작성 시 주의사항
* Windows PowerShell 환경에서 `git commit -m "한글"` 사용 시 인코딩 문제로 한글이 깨져 기록될 수 있습니다.
* `AGENTS.md` 지침에 따라 **반드시 UTF-8 인코딩 파일(`COMMIT_MSG`)을 생성한 후 `git commit -F COMMIT_MSG` 방식으로 커밋**해야 합니다.

---

## 7. 향후 개선 및 추천 과제 (Backlog)

1. **GitHub Actions 환율 자동화 활성화 :**
   * `.github/workflows/update-rate.yml`을 배포하여 매일 평일 09:00에 `fetch_rate.py`가 자동 실행되고 푸시되도록 구성
2. **Supabase 사용자 인증 (Auth) 연동 :**
   * 실무 메모 작성 시 로그인한 사용자의 이메일이나 이름을 `author` 컬럼에 자동 기록
3. **데이터 내보내기 (Export to Excel) :**
   * 공공데이터 원장 표에서 필터링된 계약 목록을 CSV 또는 Excel 파일로 즉시 다운로드하는 기능

---

**인수인계 완료 확인자 :** AI Agent (OpenHands)  
**소속 :** 한화시스템 팀장 대상 교육 과정 대시보드 개발 지원팀
