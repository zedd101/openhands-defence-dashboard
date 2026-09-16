// =============================================================
// 방산 구매·판매 관리 대시보드 : 가상 데이터
// -------------------------------------------------------------
// 이 파일의 모든 사업명·협력사명·금액·날짜·담당자는 교육용 가상 데이터입니다.
// 실제 계약·규격·기술 정보를 넣지 마십시오 (보안지침 별표 3 자가진단표 점검항목 참조).
// 담당자는 가상의 한국 이름으로 표기합니다.
// 기준일(TODAY)을 바꾸면 납기 레일·D-day·경고가 전부 다시 계산됩니다.
// =============================================================

const TODAY = "2026-09-09";

// 사업 분야 (필터 항목)
const CATEGORIES = ["레이더", "전자광학", "함정 전투체계", "전술통신", "항공전자"];

// -------------------------------------------------------------
// 1. 판매 계약 (수주·납품)
//    stage: 제안 → 협상 → 계약 → 생산 → 납품 → 검수완료
//    amount: 억원, delivery: 계약상 납기, plan: 현재 예상 납기
//    export: 해외 사업이면 true (수출허가 필요)
// -------------------------------------------------------------
const CONTRACTS = [
  { id: "S-2601", name: "해상감시레이더 2차 양산",       category: "레이더",      customer: "국내 해군",   region: "국내", stage: "생산",     amount: 842,  contractDate: "2025-11-20", delivery: "2026-09-25", plan: "2026-09-25", owner: "김도현", export: false, progress: 78 },
  { id: "S-2602", name: "차기 전술 단말 초도 납품",     category: "전술통신",    customer: "국내 육군",   region: "국내", stage: "납품",     amount: 415,  contractDate: "2025-08-04", delivery: "2026-09-18", plan: "2026-09-18", owner: "정민우", export: false, progress: 96 },
  { id: "S-2603", name: "함정 전투체계 성능개량 3척",   category: "함정 전투체계", customer: "국내 해군",   region: "국내", stage: "생산",     amount: 1_260, contractDate: "2025-06-12", delivery: "2026-10-30", plan: "2026-11-13", owner: "박준호",   export: false, progress: 61 },
  { id: "S-2604", name: "열상 조준경 해외 공급",         category: "전자광학",    customer: "고객국 A",    region: "해외", stage: "생산",     amount: 388,  contractDate: "2026-01-15", delivery: "2026-10-12", plan: "2026-10-12", owner: "이서연",   export: true,  progress: 70 },
  { id: "S-2605", name: "항공기 임무컴퓨터 2세트",       category: "항공전자",    customer: "국내 공군",   region: "국내", stage: "계약",     amount: 296,  contractDate: "2026-07-30", delivery: "2027-03-31", plan: "2027-03-31", owner: "한지수", export: false, progress: 12 },
  { id: "S-2606", name: "다기능 레이더 정비 부품 패키지", category: "레이더",      customer: "고객국 B",    region: "해외", stage: "협상",     amount: 174,  contractDate: null,         delivery: "2027-02-28", plan: "2027-02-28", owner: "김도현", export: true,  progress: 0 },
  { id: "S-2607", name: "함정 전투체계 신조 1척",        category: "함정 전투체계", customer: "고객국 C",    region: "해외", stage: "제안",     amount: 2_150, contractDate: null,         delivery: "2028-06-30", plan: "2028-06-30", owner: "박준호",   export: true,  progress: 0 },
  { id: "S-2608", name: "전술통신 중계기 후속 양산",     category: "전술통신",    customer: "국내 육군",   region: "국내", stage: "생산",     amount: 532,  contractDate: "2025-12-02", delivery: "2026-11-20", plan: "2026-11-20", owner: "정민우", export: false, progress: 55 },
  { id: "S-2609", name: "전자광학 추적장비 시험 납품",   category: "전자광학",    customer: "국내 해군",   region: "국내", stage: "납품",     amount: 128,  contractDate: "2026-02-10", delivery: "2026-09-12", plan: "2026-09-12", owner: "이서연",   export: false, progress: 100 },
  { id: "S-2610", name: "항공전자 정비 지원 계약",       category: "항공전자",    customer: "국내 공군",   region: "국내", stage: "검수완료", amount: 89,   contractDate: "2025-09-01", delivery: "2026-08-28", plan: "2026-08-28", owner: "한지수", export: false, progress: 100 },
  { id: "S-2611", name: "해안 감시레이더 해외 공급",     category: "레이더",      customer: "고객국 A",    region: "해외", stage: "계약",     amount: 640,  contractDate: "2026-08-21", delivery: "2027-05-15", plan: "2027-05-15", owner: "김도현", export: true,  progress: 8 },
  { id: "S-2612", name: "전술 데이터링크 단말 추가분",   category: "전술통신",    customer: "국내 합동부대", region: "국내", stage: "협상",     amount: 210,  contractDate: null,         delivery: "2027-01-31", plan: "2027-01-31", owner: "정민우", export: false, progress: 0 },
];

// -------------------------------------------------------------
// 2. 구매 발주 (협력사 조달)
//    status: 발주 → 제작중 → 입고예정 → 입고완료 / 지연
//    due: 발주서상 납기, eta: 협력사가 알려온 현재 입고 예정일
//    forContract: 이 부품이 들어가는 판매 계약 ID
//    longLead: 장납기 품목이면 true
// -------------------------------------------------------------
const PURCHASE_ORDERS = [
  { id: "P-4101", item: "송수신 모듈(TRM) 240식",      supplier: "협력사 가",  category: "레이더",      status: "지연",     amount: 96,  ordered: "2026-04-02", due: "2026-09-05", eta: "2026-09-19", forContract: "S-2601", owner: "김도현", longLead: true,  itar: false },
  { id: "P-4102", item: "안테나 방열판 가공품",         supplier: "협력사 나",  category: "레이더",      status: "입고예정", amount: 14,  ordered: "2026-06-10", due: "2026-09-15", eta: "2026-09-15", forContract: "S-2601", owner: "김도현", longLead: false, itar: false },
  { id: "P-4103", item: "군용 배터리 팩 1,200개",       supplier: "협력사 다",  category: "전술통신",    status: "입고완료", amount: 22,  ordered: "2026-05-20", due: "2026-08-30", eta: "2026-08-27", forContract: "S-2602", owner: "정민우", longLead: false, itar: false },
  { id: "P-4104", item: "전투체계 콘솔 디스플레이 18식", supplier: "협력사 라",  category: "함정 전투체계", status: "지연",     amount: 71,  ordered: "2026-03-14", due: "2026-09-30", eta: "2026-10-28", forContract: "S-2603", owner: "박준호",   longLead: true,  itar: false },
  { id: "P-4105", item: "냉각 적외선 검출기 60식",       supplier: "해외 협력사 A", category: "전자광학", status: "입고예정", amount: 118, ordered: "2026-02-25", due: "2026-09-20", eta: "2026-09-22", forContract: "S-2604", owner: "이서연",   longLead: true,  itar: true  },
  { id: "P-4106", item: "광학 렌즈 조립체",             supplier: "협력사 마",  category: "전자광학",    status: "제작중",   amount: 33,  ordered: "2026-07-01", due: "2026-10-01", eta: "2026-10-01", forContract: "S-2604", owner: "이서연",   longLead: false, itar: false },
  { id: "P-4107", item: "임무컴퓨터 보드 세트",         supplier: "해외 협력사 B", category: "항공전자", status: "발주",     amount: 54,  ordered: "2026-08-25", due: "2027-01-15", eta: "2027-01-15", forContract: "S-2605", owner: "한지수", longLead: true,  itar: true  },
  { id: "P-4108", item: "중계기 하우징 320식",          supplier: "협력사 바",  category: "전술통신",    status: "제작중",   amount: 19,  ordered: "2026-06-30", due: "2026-10-20", eta: "2026-10-20", forContract: "S-2608", owner: "정민우", longLead: false, itar: false },
  { id: "P-4109", item: "RF 증폭기 모듈 320식",         supplier: "협력사 가",  category: "전술통신",    status: "입고예정", amount: 48,  ordered: "2026-05-08", due: "2026-10-05", eta: "2026-10-05", forContract: "S-2608", owner: "정민우", longLead: true,  itar: false },
  { id: "P-4110", item: "추적장비 짐벌 구동부",         supplier: "협력사 사",  category: "전자광학",    status: "입고완료", amount: 27,  ordered: "2026-04-18", due: "2026-08-20", eta: "2026-08-18", forContract: "S-2609", owner: "이서연",   longLead: false, itar: false },
  { id: "P-4111", item: "전투체계 서버 랙 6식",         supplier: "협력사 아",  category: "함정 전투체계", status: "입고예정", amount: 41,  ordered: "2026-06-05", due: "2026-09-28", eta: "2026-09-28", forContract: "S-2603", owner: "박준호",   longLead: false, itar: false },
  { id: "P-4112", item: "레이더 신호처리 보드",         supplier: "협력사 나",  category: "레이더",      status: "발주",     amount: 62,  ordered: "2026-09-01", due: "2027-02-10", eta: "2027-02-10", forContract: "S-2611", owner: "김도현", longLead: true,  itar: false },
  { id: "P-4113", item: "함정용 케이블 하네스",         supplier: "협력사 자",  category: "함정 전투체계", status: "제작중",   amount: 9,   ordered: "2026-08-12", due: "2026-10-15", eta: "2026-10-15", forContract: "S-2603", owner: "박준호",   longLead: false, itar: false },
  { id: "P-4114", item: "항전 장비 커넥터 세트",         supplier: "협력사 차",  category: "항공전자",    status: "입고완료", amount: 6,   ordered: "2026-05-30", due: "2026-08-10", eta: "2026-08-09", forContract: "S-2610", owner: "한지수", longLead: false, itar: false },
];

// -------------------------------------------------------------
// 3. 수출허가·규제 (해외 판매, 해외 부품 도입)
//    type: 전략물자 수출허가 / 최종사용자 증명(EUC) / 해외 부품 재수출 승인
//    status: 준비중 → 신청 → 심사중 → 승인 / 만료임박
// -------------------------------------------------------------
const LICENSES = [
  { id: "L-311", type: "전략물자 수출허가",   forContract: "S-2604", status: "승인",     applied: "2026-03-02", expires: "2026-11-30", owner: "이서연"   },
  { id: "L-312", type: "최종사용자 증명(EUC)", forContract: "S-2604", status: "승인",     applied: "2026-02-20", expires: "2026-12-31", owner: "이서연"   },
  { id: "L-313", type: "해외 부품 재수출 승인", forContract: "S-2604", status: "심사중",   applied: "2026-08-05", expires: null,         owner: "이서연"   },
  { id: "L-314", type: "전략물자 수출허가",   forContract: "S-2611", status: "신청",     applied: "2026-09-03", expires: null,         owner: "김도현" },
  { id: "L-315", type: "최종사용자 증명(EUC)", forContract: "S-2611", status: "준비중",   applied: null,         expires: null,         owner: "김도현" },
  { id: "L-316", type: "전략물자 수출허가",   forContract: "S-2606", status: "준비중",   applied: null,         expires: null,         owner: "김도현" },
  { id: "L-317", type: "해외 부품 재수출 승인", forContract: "S-2605", status: "승인",     applied: "2026-06-11", expires: "2026-10-05", owner: "한지수" },
];

// -------------------------------------------------------------
// 4. 협력사 납기 준수율 (최근 12개월, %)
// -------------------------------------------------------------
const SUPPLIERS = [
  { name: "협력사 가",     onTime: 74, orders: 19 },
  { name: "협력사 나",     onTime: 91, orders: 12 },
  { name: "협력사 다",     onTime: 97, orders: 31 },
  { name: "협력사 라",     onTime: 68, orders: 8  },
  { name: "협력사 마",     onTime: 88, orders: 14 },
  { name: "협력사 바",     onTime: 93, orders: 22 },
  { name: "협력사 사",     onTime: 95, orders: 9  },
  { name: "협력사 아",     onTime: 90, orders: 11 },
  { name: "협력사 자",     onTime: 92, orders: 7  },
  { name: "협력사 차",     onTime: 96, orders: 15 },
  { name: "해외 협력사 A", onTime: 82, orders: 6  },
  { name: "해외 협력사 B", onTime: 79, orders: 5  },
];

// 납기 준수율 기준선 (이 값 아래는 관리 대상)
const ONTIME_TARGET = 90;
