import streamlit as st
import random

# --- 설정 및 초기화 ---

st.set_page_config(
    page_title="⚽️ 강화 시뮬레이터",
    layout="centered"
)

# 상수 정의
INITIAL_POINTS = 500
MAX_LEVEL = 5
MIN_BET = 50

# 세션 상태 초기화
if 'points' not in st.session_state:
    st.session_state.points = INITIAL_POINTS
if 'item_level' not in st.session_state:
    st.session_state.item_level = 1  # 아이템 초기 레벨
if 'game_result' not in st.session_state:
    st.session_state.game_result = f"강화를 시작해 보세요! 보유 포인트: {INITIAL_POINTS}P, 아이템 레벨: +1"
if 'last_bet' not in st.session_state:
    st.session_state.last_bet = MIN_BET

# 강화 레벨별 성공 확률 (퍼센트)
# 레벨 +1 -> +2: 70%
# 레벨 +2 -> +3: 50%
# 레벨 +3 -> +4: 30%
# 레벨 +4 -> +5: 15%
SUCCESS_RATES = {
    1: 70, 
    2: 50, 
    3: 30, 
    4: 15
}

# --- 핵심 함수 ---

def attempt_upgrade(current_level, bet_amount):
    """강화를 시도하고 포인트를 업데이트하는 로직"""
    
    # 강화 단계가 최대치인지 확인
    if current_level >= MAX_LEVEL:
        st.session_state.game_result = "✅ **최대 레벨**입니다! 더 이상 강화할 수 없습니다."
        return

    # 1. 포인트 부족 여부 확인
    if st.session_state.points < bet_amount or bet_amount < MIN_BET:
        st.session_state.game_result = f"⚠️ **오류:** 베팅 금액({bet_amount}P)을 확인해주세요. 최소 {MIN_BET}P 이상, 보유 포인트 이하여야 합니다."
        return
        
    # 2. 포인트 소모 (실패해도 돌려받지 않음)
    st.session_state.points -= bet_amount
    
    # 현재 레벨에서 다음 레벨로 넘어갈 성공 확률
    success_rate = SUCCESS_RATES.get(current_level, 0)
    
    # 3. 강화 시도 (랜덤 확률 판정)
    roll = random.randint(1, 100)
    is_successful = roll <= success_rate
    
    st.session_state.game_result = f"🔮 **강화 시도 (+{current_level} → +{current_level + 1})**\n\n"
    
    if is_successful:
        # 성공 시: 레벨 증가 및 포인트 환불 (여기서는 100% 환불로 설정)
        st.session_state.item_level += 1
        st.session_state.points += bet_amount # 건 포인트를 돌려받음
        
        st.session_state.game_result += (
            f"🎉 **강화 성공!** 아이템이 **+{st.session_state.item_level}**이 되었습니다. "
            f"건 포인트 **{bet_amount}P**를 돌려받았습니다. (현재 포인트: {st.session_state.points}P)"
        )
    else:
        # 실패 시: 레벨 유지 및 포인트 소모 확정
        st.session_state.game_result += (
            f"💥 **강화 실패...** 확률 ({success_rate}%)을 넘지 못했습니다. "
            f"건 포인트 **{bet_amount}P**는 소모되었습니다. (현재 포인트: {st.session_state.points}P)"
        )
    
    st.session_state.last_bet = bet_amount

def reset_state():
    """포인트와 강화 레벨을 초기화합니다."""
    st.session
