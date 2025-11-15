import streamlit as st
import random

# --- 설정 및 상수 정의 ---

st.set_page_config(
    page_title="⚔️ 검 강화 시뮬레이터",
    layout="centered"
)

# 상수 정의
INITIAL_POINTS = 5000 
MAX_LEVEL = 10
MIN_BET = 200 
CHARGE_AMOUNT = 2000

# 레벨별 강화 성공 확률 (%) - 10단계까지 확장
SUCCESS_RATES = {
    1: 90, 2: 75, 3: 60, 4: 45, 5: 30, 
    6: 20, 7: 15, 8: 10, 9: 5 
}

# 레벨별 고정 비용 (항상 소모됨) - 10단계까지 확장
FIXED_COSTS = {
    1: 100, 2: 200, 3: 400, 4: 600, 5: 800,
    6: 1200, 7: 1800, 8: 2500, 9: 3500
}

# 레벨별 검 이름
ITEM_NAMES = {
    1: "나무 검", 2: "동 검", 3: "철 검", 4: "강철 검", 
    5: "미스릴 검", 6: "오리하르콘", 7: "전설의 검", 
    8: "신화의 검", 9: "파괴의 검", 10: "⭐ 궁극의 검 ⭐"
}

# --- 세션 상태 초기화 함수 ---

def initialize_session_state():
    """모든 세션 상태 변수를 초기화합니다."""
    if 'points' not in st.session_state:
        st.session_state.points = INITIAL_POINTS
    if 'item_level' not in st.session_state:
        st.session_state.item_level = 1
    if 'game_result' not in st.session_state:
        st.session_state.game_result = f"최대 +{MAX_LEVEL} 검 강화에 도전하세요! 보유 포인트: {INITIAL_POINTS}P, 현재 검: +1"
    if 'last_bet' not in st.session_state:
        st.session_state.last_bet = MIN_BET
    if 'charge_count' not in st.session_state:
        st.session_state.charge_count = 0

initialize_session_state()

# --- 핵심 로직 함수 ---

def attempt_upgrade(bet_amount):
    """검 강화를 시도하고 포인트를 업데이트하는 로직"""
    
    current_level = st.session_state.item_level
    
    if current_level >= MAX_LEVEL:
        st.session_state.game_result = "✅ **최대 레벨**입니다! 더 이상 강화할 수 없습니다."
        return

    fixed_cost = FIXED_COSTS.get(current_level, 0)
    total_cost = bet_amount + fixed_cost
    
    # 1. 포인트 부족 확인 (UI에서 막지만, 로직에서 한 번 더 확인)
    if st.session_state.points < total_cost:
        st.session_state.game_result = f"⚠️ **오류:** 총 비용({total_cost}P) 지불에 포인트가 부족합니다. 베팅 금액을 다시 설정하거나 충전하세요."
        return
        
    # 2. 포인트 소모
    st.session_state.points -= total_cost
    
    # 3. 강화 판정
    success_rate = SUCCESS_RATES.get(current_level, 0)
    roll = random.randint(1, 100)
    is_successful = roll <= success_rate
    
    # 4. 결과 처리
    st.session_state.game_result = (
        f"**⚔️ 강화 시도 (+{current_level} {ITEM_NAMES.get(current_level, '')} → +{current_level + 1}...)** "
        f"(확률: {success_rate}%, 굴림: {roll})\n\n"
    )
    
    if is_successful:
        st.session_state.item_level += 1
        st.session_state.points += bet_amount # 베팅 포인트 환불
        
        st.session_state.game_result += (
            f"🟢 **[SUCCESS] 축하합니다!** 검이 **+{st.session_state.item_level} {ITEM_NAMES.get(st.session_state.item_level, '')}**이 되었습니다. "
            f"고정 비용 {fixed_cost}P만 소모되었습니다. (현재 포인트: {st.session_state.points}P)"
        )
    else:
        # 실패 시: 레벨 +1로 초기화 (격렬한 페널티)
        st.session_state.item_level = 1 
        st.session_state.game_result += (
            f"🔴 **[FAIL] 대실패!** 검의 레벨이 **+1 {ITEM_NAMES.get(1, '')}**로 초기화되었습니다. "
            f"총 비용 **{total_cost}P** 모두 소모되었습니다. (현재 포인트: {st.session_state.points}P)"
        )
    
    st.session_state.last_bet = bet_amount

def reset_state():
    """포인트와 검 레벨을 초기화합니다."""
    st.session_state.points = INITIAL_POINTS
    st.session_state.item_level = 1
    st.session_state.charge_count = 0
    st.session_state.game_result = f"시스템이 초기화되었습니다. **{INITIAL_POINTS}P**와 **+1 검**으로 다시 시작합니다."
    
def charge_points():
    """포인트를 충전합니다."""
    st.session_state.points += CHARGE_AMOUNT
    st.session_state.charge_count += 1
    st.session_state.game_result = f"⚡️ **{CHARGE_AMOUNT}P**가 충전되었습니다. (총 {st.session_state.charge_count}회 충전)"

# --- Streamlit UI 구성 ---

st.title("⚔️ 검 강화 시뮬레이터 (파괴 시스템)")
st.markdown("---")

### 📊 검 상태 및 포인트 현황

col1, col2 = st.columns(2)
current_level = st.session_state.item_level
fixed_cost = FIXED_COSTS.get(current_level, 0)
current_item_name = ITEM_NAMES.get(current_level, "Unknown")

# 검 레벨 표시
col1.metric(
    label=f"현재 검 레벨 ({current_item_name})", 
    value=f"+{current_level}", 
    delta=f"최대 {MAX_LEVEL}" if current_level < MAX_LEVEL else "MAX",
    delta_color="normal" if current_level < MAX_LEVEL else "inverse"
)

# 현재 포인트 표시
col2.metric(label="현재 보유 포인트", value=f"{st.session_state.points} P")

st.markdown("---")

# 0. 최대 레벨 도달 처리
if current_level >= MAX_LEVEL:
    st.balloons()
    st.success("🏆 **궁극의 검**을 얻었습니다! 더 이상의 강화는 불가능합니다.")
    if st.button("새로운 게임으로 초기화", on_click=reset_state, key='reset_max', use_container_width=True):
        st.rerun()
else:
    # 1. 강화에 필요한 최소 비용 계산 및 포인트 부족 처리
    min_total_cost = fixed_cost + MIN_BET
    
    if st.session_state.points < min_total_cost:
        st.error(f"⚠️ **포인트 부족:** 최소 강화 비용({min_total_cost}P)을 지불할 수 없습니다.")
        col_charge, col_reset = st.columns(2)
        
        with col_charge:
            if st.button(f"⚡️ {CHARGE_AMOUNT}P 충전", on_click=charge_points, key='charge_low_point', use_container_width=True):
                st.rerun()
        with col_reset:
            if st.button("게임 초기화", on_click=reset_state, key='reset_low_point', use_container_width=True):
                st.rerun()
    else:
        ### ⚙️ 강화 설정 및 실행
        next_level = current_level + 1
        
        # 베팅 가능한 최대 금액 계산 및 슬라이더 안정화
        max_possible_bet = st.session_state.points - fixed_cost
        max_bet_value = max(MIN_BET, max_possible_bet) 
        default_bet = min(st.session_state.last_bet, max_bet_value)
        default_bet = max(MIN_BET, default_bet)
        
        bet = st.slider(
            f"강화에 베팅할 포인트 금액을 선택하세요. (최소 {MIN_BET}P / 최대 {max_bet_value}P)", 
            min_value=MIN_BET, 
            max_value=max_bet_value, 
            step=MIN_BET, 
            value=default_bet,
            key='bet_slider'
        )

        success_rate = SUCCESS_RATES.get(current_level, 0)
        
        st.info(
            f"**강화 목표:** +{current_level} → +{next_level}\n\n"
            f"**성공 확률:** **{success_rate}%**\n"
            f"**고정 비용 (소모):** **{fixed_cost} P**\n"
            f"**베팅 포인트 (환불):** **{bet} P**\n"
            f"**총 비용:** **{fixed_cost + bet} P**"
        )
        
        # 3. 강화 실행 버튼 (on_click과 args를 사용해 안정성 확보)
        is_disabled = st.session_state.points < (bet + fixed_cost)
        
        st.button(f"⚔️ +{current_level} 강화 시도 (총 비용 {fixed_cost + bet}P)", 
                  on_click=attempt_upgrade, 
                  args=(bet,), 
                  use_container_width=True, 
                  disabled=is_disabled)

### 📊 강화 결과 및 추가 옵션
st.markdown("---")

st.subheader("마지막 강화 결과")
st.markdown(st.session_state.game_result)

# 페이지 하단 충전/초기화 옵션
col_bottom_charge, col_bottom_reset = st.columns(2)

with col_bottom_charge:
    if st.button(f"⚡️ {CHARGE_AMOUNT}P 추가 충전", on_click=charge_points, key='charge_any_time', use_container_width=True):
        st.rerun()

with col_bottom_reset:
    if st.session_state.points < INITIAL_POINTS * 2 or current_level > 1:
        if st.button(f"게임 초기화 ({INITIAL_POINTS}P, +1)", on_click=reset_state, key='reset_any_time', use_container_width=True):
            st.rerun()
