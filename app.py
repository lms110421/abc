import streamlit as st
import random

# --- 설정 및 초기화 ---

st.set_page_config(
    page_title="⚽️ 강화 시뮬레이터 (파괴 시스템)",
    layout="centered"
)

# 상수 정의
INITIAL_POINTS = 1000
MAX_LEVEL = 5
MIN_BET = 100 # 베팅 최소 금액 상향

# 레벨별 강화 성공 확률 (%)
SUCCESS_RATES = {
    1: 80,  # +1 -> +2: 80% (첫 강화는 비교적 쉬움)
    2: 50,  # +2 -> +3: 50%
    3: 30,  # +3 -> +4: 30%
    4: 10   # +4 -> +5: 10% (최고 레벨은 극악)
}

# 레벨별 고정 비용 (강화 재료/수수료, 성공/실패와 무관하게 소모됨)
FIXED_COSTS = {
    1: 50, 
    2: 100, 
    3: 150, 
    4: 200
}

# 세션 상태 초기화
if 'points' not in st.session_state:
    st.session_state.points = INITIAL_POINTS
if 'item_level' not in st.session_state:
    st.session_state.item_level = 1
if 'game_result' not in st.session_state:
    st.session_state.game_result = f"강화를 시작해 보세요! 보유 포인트: {INITIAL_POINTS}P, 아이템 레벨: +1"
if 'last_bet' not in st.session_state:
    st.session_state.last_bet = MIN_BET

# --- 핵심 함수 ---

def attempt_upgrade(current_level, bet_amount):
    """강화를 시도하고 포인트를 업데이트하는 로직"""
    
    if current_level >= MAX_LEVEL:
        st.session_state.game_result = "✅ **최대 레벨**입니다! 더 이상 강화할 수 없습니다."
        return

    fixed_cost = FIXED_COSTS.get(current_level, 0)
    total_cost = bet_amount + fixed_cost
    
    # 1. 포인트 부족 여부 확인
    if st.session_state.
