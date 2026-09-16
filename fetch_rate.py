#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
달러 환율 수집 스크립트 (Frankfurter API)
- 유럽중앙은행(ECB) 기준 USD -> KRW 환율 수집
- 수집된 데이터를 rate.js (및 docs/rate.js)에 JavaScript 상수로 저장
"""

import json
import os
import sys
import urllib.request
from datetime import datetime

API_URL = "https://api.frankfurter.dev/v1/latest?from=USD&to=KRW"

def fetch_exchange_rate():
    req = urllib.request.Request(
        API_URL,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status != 200:
                print(f"환율 수집 실패: HTTP 응답 코드 {resp.status}")
                return False
            payload = resp.read().decode("utf-8")
            data = json.loads(payload)
    except Exception as e:
        print(f"환율 수집 실패: 연결 오류가 발생했습니다. ({e})")
        return False

    try:
        krw_rate = data["rates"]["KRW"]
        base_date = data["date"]
    except KeyError as e:
        print(f"환율 수집 실패: 응답 데이터 파싱 실패 (누락된 키: {e})")
        return False

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    js_content = (
        f'const RATE = {{ 원화: {krw_rate}, 기준일: "{base_date}", '
        f'출처: "Frankfurter(유럽중앙은행 기준환율)", 수집시각: "{now_str}" }};\n'
    )

    # 저장 대상 경로 결정 (루트 rate.js 및 docs/rate.js)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_files = [os.path.join(base_dir, "rate.js")]
    
    docs_dir = os.path.join(base_dir, "docs")
    if os.path.isdir(docs_dir):
        target_files.append(os.path.join(docs_dir, "rate.js"))

    for target_path in target_files:
        try:
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(js_content)
        except Exception as e:
            print(f"환율 수집 실패: 파일 저장 실패 ({target_path}: {e})")
            return False

    print(f"환율 수집 성공: 1 USD = {krw_rate} KRW")
    print(f"기준일: {base_date}")
    print(f"수집시각: {now_str}")
    return True

if __name__ == "__main__":
    success = fetch_exchange_rate()
    if not success:
        sys.exit(1)
