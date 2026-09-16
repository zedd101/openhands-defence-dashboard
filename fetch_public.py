#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
방위사업청 국내계약정보 수집 스크립트 (공공데이터포털 OpenAPI)
- 엔드포인트: https://apis.data.go.kr/1690000/CntrctInfoService/getDmstcCntrctInfoList
- 환경변수 DATA_GO_KR_KEY 또는 .env 파일에서 인증키를 로드
- 최근 1개월간의 국내 계약 데이터를 수집하여 public.js에 저장
- 보안 주의: 인증키는 절대 로그, 화면, 채팅, 코드에 노출하지 않음
"""

import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

API_BASE_URL = "https://apis.data.go.kr/1690000/CntrctInfoService/getDmstcCntrctInfoList"

def get_api_key():
    """
    환경변수 또는 .env 파일에서 API 키를 읽어옵니다.
    키는 절대 화면이나 로그에 출력하지 않습니다.
    """
    # 1. 시스템 환경변수 우선 확인
    key = os.environ.get("DATA_GO_KR_KEY")
    if key and key.strip():
        return key.strip()

    # 2. .env 파일 확인
    base_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(base_dir, ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if line.startswith("DATA_GO_KR_KEY="):
                        val = line.split("=", 1)[1].strip()
                        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                            val = val[1:-1].strip()
                        if val:
                            return val
        except Exception:
            pass

    return None

def normalize_date(raw_date):
    """YYYYMMDD 형식 날짜를 YYYY-MM-DD 형식으로 정규화"""
    if not raw_date:
        return ""
    s = str(raw_date).strip().replace("-", "").replace(".", "").replace("/", "")
    if len(s) == 8 and s.isdigit():
        return f"{s[:4]}-{s[4:6]}-{s[6:8]}"
    return str(raw_date).strip()

def normalize_amount(raw_amt):
    """금액을 숫자(원 단위 int)로 변환"""
    if raw_amt is None or raw_amt == "":
        return 0
    try:
        s = str(raw_amt).replace(",", "").strip()
        return int(float(s))
    except (ValueError, TypeError):
        return 0

def normalize_rate(raw_rate, amt=0, plan_amt=0):
    """낙찰률(%)을 float로 변환 또는 계산"""
    if raw_rate is not None and str(raw_rate).strip() != "":
        try:
            val = float(str(raw_rate).replace(",", "").strip())
            return round(val, 2)
        except (ValueError, TypeError):
            pass
    if plan_amt > 0 and amt > 0:
        return round((amt / plan_amt) * 100, 2)
    return None

def extract_contract_fields(item):
    """
    계약 정보 항목에서 요구된 주요 필드 전수 정제 추출:
    - cntrctNm (계약명), cntrctEntrpsNm (계약업체), cntrctAmnt (계약금액, 원)
    - cntrctPlanaAmnt (예정금액, 원) -> 예산 대비 절감률 산출용
    - cntrctBidnRate (낙찰률, %) -> 경쟁도 및 가격 적정성 분석용
    - cntrctDate (계약일, YYYY-MM-DD 변환)
    - cntrctMth (계약방법: 수의계약, 일반경쟁, 제한경쟁, 2단계경쟁, 협상 등)
    - cntrctDivs (계약구분: 물품, 용역, 공사 등)
    - bidMth (입찰방법), cntrctNo (계약번호)
    """
    # 1. 계약명
    name = (
        item.get("cntrctNm") or item.get("bsnsNm") or item.get("cntrctCn")
        or item.get("pblancNm") or item.get("itemNm") or item.get("계약명") or ""
    )

    # 2. 계약업체
    corp = (
        item.get("cntrctEntrpsNm") or item.get("corpNm") or item.get("entrpsNm")
        or item.get("cprNm") or item.get("bcncNm") or item.get("cmpnyNm")
        or item.get("계약업체") or ""
    )

    # 3. 계약금액 (원 단위 정수)
    raw_amt = (
        item.get("cntrctAmnt") or item.get("cntrctAmt") or item.get("totCntrctAmt")
        or item.get("amt") or item.get("cntrctAmount") or item.get("bsnsAmt") or item.get("계약금액")
    )
    amt = normalize_amount(raw_amt)

    # 4. 예정금액 (원 단위 정수)
    raw_plan_amt = (
        item.get("cntrctPlanaAmnt") or item.get("planaAmnt") or item.get("bsnsPlanaAmt")
        or item.get("cntrctPlanAmt") or item.get("예정금액")
    )
    plan_amt = normalize_amount(raw_plan_amt)
    if plan_amt == 0 and amt > 0:
        plan_amt = amt  # 수의계약 등 예정금액 미기재 시 최소 계약금액으로 방어

    # 5. 낙찰률 (%)
    raw_bid_rate = item.get("cntrctBidnRate") or item.get("bidnRate") or item.get("낙찰률")
    bid_rate = normalize_rate(raw_bid_rate, amt, plan_amt)

    # 6. 계약일
    raw_date = (
        item.get("cntrctDate") or item.get("cntrctDe") or item.get("cntrctDt")
        or item.get("cntrctDttm") or item.get("계약일") or ""
    )
    date_val = normalize_date(raw_date)

    # 7. 계약방법
    method = (
        item.get("cntrctMth") or item.get("cntrctMthNm") or item.get("cntrctMthCd")
        or item.get("cntrctMthod") or item.get("계약방법") or ""
    )

    # 8. 계약구분
    divs = (
        item.get("cntrctDivs") or item.get("cntrctDivsNm") or item.get("divs")
        or item.get("계약구분") or ""
    )

    # 9. 입찰방법
    bid_mth = (
        item.get("bidMth") or item.get("bidMthNm") or item.get("입찰방법") or ""
    )

    # 10. 계약번호
    cntrct_no = (
        item.get("cntrctNo") or item.get("cntrctNum") or item.get("계약번호") or ""
    )

    return {
        "계약명": str(name).strip(),
        "계약업체": str(corp).strip(),
        "계약금액": amt,
        "예정금액": plan_amt,
        "낙찰률": bid_rate,
        "계약일": date_val,
        "계약방법": str(method).strip(),
        "계약구분": str(divs).strip(),
        "입찰방법": str(bid_mth).strip(),
        "계약번호": str(cntrct_no).strip(),
    }

def fetch_contracts():
    api_key = get_api_key()
    if not api_key:
        print("[오류] 환경변수 DATA_GO_KR_KEY 가 설정되지 않았습니다.")
        print("프로젝트 루트의 .env 파일에 DATA_GO_KR_KEY=<서비스키> 를 입력하시거나")
        print("터미널에서 $env:DATA_GO_KR_KEY='<서비스키>' 환경변수를 설정해 주십시오.")
        return False

    today = datetime.now().date()
    start_date = today - timedelta(days=30)
    cntrct_date_begin = start_date.strftime("%Y%m%d")
    cntrct_date_end = today.strftime("%Y%m%d")

    print(f"방위사업청 국내 계약정보 수집 시작 (조회기간: {cntrct_date_begin} ~ {cntrct_date_end})")

    # API 키 URL 인코딩 (이미 인코딩된 키와 디코딩된 키 모두 안전 처리)
    unquoted_key = urllib.parse.unquote(api_key)
    encoded_key = urllib.parse.quote(unquoted_key, safe="")

    page_no = 1
    num_of_rows = 1000
    all_contracts = []

    while True:
        query_params = (
            f"serviceKey={encoded_key}"
            f"&_type=json"
            f"&numOfRows={num_of_rows}"
            f"&pageNo={page_no}"
            f"&cntrctDateBegin={cntrct_date_begin}"
            f"&cntrctDateEnd={cntrct_date_end}"
        )
        url = f"{API_BASE_URL}?{query_params}"

        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                if resp.status != 200:
                    print(f"[오류] API 호출 실패: HTTP 상태 코드 {resp.status}")
                    return False
                payload = resp.read().decode("utf-8")
        except Exception as e:
            # 보안: URL이나 키가 에러에 포함되지 않도록 마스킹
            print(f"[오류] API 네트워크 연결 실패 ({type(e).__name__})")
            return False

        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            print("[오류] 응답이 JSON 형식이 아닙니다.")
            # XML 오류 응답 여부 확인 (SERVICE_KEY 오류 등)
            if "OpenAPI_ServiceResponse" in payload or "cmmMsgHeader" in payload:
                print("[안내] 공공데이터포털 오류 응답: 서비스키 등록 상태를 확인해 주십시오.")
            return False

        # 응답 헤더 확인
        header = data.get("response", {}).get("header", {})
        result_code = str(header.get("resultCode", ""))
        result_msg = header.get("resultMsg", "")

        if result_code and result_code not in ("00", "0", "NORMAL SERVICE"):
            print(f"[오류] API 결과 오류 (코드: {result_code}, 메시지: {result_msg})")
            return False

        body = data.get("response", {}).get("body", {})
        total_count = body.get("totalCount", 0)

        # 항목 목록 추출 (배열, 단일 객체, 누락 등 대응)
        items = []
        raw_items = body.get("items")
        if isinstance(raw_items, list):
            items = raw_items
        elif isinstance(raw_items, dict):
            sub = raw_items.get("item", [])
            if isinstance(sub, list):
                items = sub
            elif isinstance(sub, dict):
                items = [sub]

        if not items:
            break

        for item in items:
            contract = extract_contract_fields(item)
            all_contracts.append(contract)

        print(f"페이지 {page_no} 수집 완료 (현재 누적: {len(all_contracts)}건 / 총 {total_count}건)")

        # 종료 조건: 총 건수 도달 또는 마지막 페이지
        if len(items) < num_of_rows:
            break
        if total_count and len(all_contracts) >= total_count:
            break

        page_no += 1

    # public.js 저장 형식 구성
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    public_obj = {
        "수집시각": now_str,
        "건수": len(all_contracts),
        "계약": all_contracts
    }

    js_content = f"const PUBLIC = {json.dumps(public_obj, ensure_ascii=False, indent=2)};\n"

    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_paths = [os.path.join(base_dir, "public.js")]
    docs_dir = os.path.join(base_dir, "docs")
    if os.path.isdir(docs_dir):
        target_paths.append(os.path.join(docs_dir, "public.js"))

    for path in target_paths:
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(js_content)
        except Exception as e:
            print(f"[오류] 파일 저장 실패 ({os.path.basename(path)}: {e})")
            return False

    print(f"\n[수집 완료] 총 {len(all_contracts)}건의 국내 계약 정보를 정상 저장하였습니다.")
    print(f"수집시각: {now_str}")
    print("저장 위치: public.js, docs/public.js")
    return True

if __name__ == "__main__":
    success = fetch_contracts()
    if not success:
        sys.exit(1)
