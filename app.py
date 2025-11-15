import streamlit as st
import random

# --- 설정 및 상수 정의 ---

st.set_page_config(
    page_title="⚽️ 강화 시뮬레이터 (MAX +8)",
    layout="centered"
)

# 상수
INITIAL_POINTS = 2000 # 시작 포인트 증가
MAX_LEVEL = 8
MIN_BET = 100 
CHARGE_AMOUNT = 1000 # 충전 금액 증가

# 레벨별 강화 성공 확률 (%) - 8단계까지 확장
SUCCESS_RATES = {
    1: 85, 2: 70, 3: 50, 4: 35, 
    5: 20, 6: 15, 7: 10
}

# 레벨별 고정 비용 (항상 소모됨) - 8단계까지 확장
FIXED_COSTS = {
    1: 100, 2: 150, 3: 200, 4: 300, 
    5: 400, 6: 600, 7: 800
}

# 레벨별 아이템 등급 이름
ITEM_NAMES = {
    1: "노멀", 2: "베이직", 3: "스페셜", 
    4: "레어", 5: "에픽", 6: "마스터", 
    7: "얼티밋", 8: "ICONIC 🌟"
}

# --- 세션 상태 초기화 ---

if 'points' not in st.session_state:
    st.session_state.points = INITIAL_POINTS
if 'item_level' not in st.session_state:
    st.session_state.item_level = 1
if 'game_result' not in st.session_state:
    st.session_state.game_result = f"MAX +{MAX_LEVEL} 강화에 도전하세요! 보유 포인트: {INITIAL_POINTS}P, 아이템 레벨: +1"
if 'last_bet' not in st.session_state:
    st.session_state.last_bet = MIN_BET
if 'charge_count' not in st.session_state:
    st.session_state.charge_count = 0

# --- 핵심 함수 ---

def attempt_upgrade(current_level, bet_amount):
    """강화를 시도하고 포인트를 업데이트하는 로직"""
    
    if current_level >= MAX_LEVEL:
        st.session_state.game_result = "✅ **최대 레벨**입니다! 더 이상 강화할 수 없습니다."
        return

    fixed_cost = FIXED_COSTS.get(current_level, 0)
    total_cost = bet_amount + fixed_cost
    
    if st.session_state.points < total_cost:
        st.session_state.game_result = f"⚠️ **오류:** 총 비용({total_cost}P) 지불에 포인트가 부족합니다."
        return
        
    # 포인트 소모
    st.session_state.points -= total_cost
    
    success_rate = SUCCESS_RATES.get(current_level, 0)
    roll = random.randint(1, 100)
    is_successful = roll <= success_rate
    
    # 강화 시도 로그
    st.session_state.game_result = (
        f"**✨ 강화 시도 (+{current_level} {ITEM_NAMES.get(current_level, '')} → +{current_level + 1}...)** "
        f"(확률: {success_rate}%, 굴림: {roll})\n\n"
    )
    
    if is_successful:
        st.session_state.item_level += 1
        st.session_state.points += bet_amount # 베팅 포인트 환불
        
        st.session_state.game_result += (
            f"🟢 **[SUCCESS] 축하합니다!** 아이템이 **+{st.session_state.item_level} {ITEM_NAMES.get(st.session_state.item_level, '')}**이 되었습니다. "
            f"고정 비용 {fixed_cost}P만 소모되었습니다. (현재 포인트: {st.session_state.points}P)"
        )
    else:
        # 실패 시 레벨 하락/유지 (+2 이상 실패 시 +1로 초기화)
        if current_level >= 2:
            st.session_state.item_level = 1 
            st.session_state.game_result += (
                f"🔴 **[FAIL] 대실패!** 아이템이 **+1 {ITEM_NAMES.get(1, '')}**로 초기화되었습니다. "
                f"총 비용 **{total_cost}P** 모두 소모되었습니다. (현재 포인트: {st.session_state.points}P)"
            )
        else:
            st.session_state.game_level = 1 
            st.session_state.game_result += (
                f"🟡 **[FAIL] 강화 실패...** 레벨은 유지됩니다. "
                f"총 비용 **{total_cost}P** 모두 소모되었습니다. (현재 포인트: {st.session_state.points}P)"
            )
    
    st.session_state.last_bet = bet_amount

def reset_state():
    """포인트와 강화 레벨을 초기화합니다."""
    st.session_state.points = INITIAL_POINTS
    st.session_state.item_level = 1
    st.session_state.charge_count = 0
    st.session_state.game_result = f"시스템이 초기화되었습니다. **{INITIAL_POINTS}P**와 **+1 아이템**으로 다시 시작합니다."
    st.rerun()

def charge_points():
    """포인트를 충전합니다."""
    st.session_state.points += CHARGE_AMOUNT
    st.session_state.charge_count += 1
    st.session_state.game_result = f"⚡️ **{CHARGE_AMOUNT}P**가 충전되었습니다. (총 {st.session_state.charge_count}회 충전)"
    st.rerun() # 포인트 충전 후 UI를 즉시 업데이트

# --- Streamlit UI 구성 ---

st.title("🔥 FIFA 스타일 강화 시뮬레이터 (MAX +8)")
st.markdown("---")

### 📊 아이템 및 포인트 현황

col1, col2 = st.columns(2)
current_level = st.session_state.item_level
fixed_cost = FIXED_COSTS.get(current_level, 0)
current_item_name = ITEM_NAMES.get(current_level, "Unknown")

# 아이템 레벨 표시 (이름 포함)
col1.metric(
    label=f"아이템 강화 레벨 ({current_item_name})", 
    value=f"+{current_level}", 
    delta=f"최대 {MAX_LEVEL}" if current_level < MAX_LEVEL else "최대 달성",
    delta_color="normal" if current_level < MAX_LEVEL else "inverse"
)

# 현재 포인트 표시
col2.metric(label="현재 보유 포인트", value=f"{st.session_state.points} P")

st.markdown("---")

# 0. 최대 레벨 도달 처리
if current_level >= MAX_LEVEL:
    st.balloons()
    st.success("🏆 **축하합니다!** 아이템이 최대 강화 레벨에 도달했습니다. 더 이상의 강화는 불가능합니다.")
    if st.button("새로운 게임으로 초기화", key='reset_max', use_container_width=True):
        reset_state()
else:
    # 1. 강화에 필요한 최소 비용 계산 및 포인트 부족 처리
    min_total_cost = fixed_cost + MIN_BET
    
    if st.session_state.points < min_total_cost:
        # 포인트 부족 시 충전 및 초기화 옵션 제공
        st.error(f"⚠️ **포인트 부족:** 최소 강화 비용({min_total_cost}P)을 지불할 수 없습니다.")
        col_charge, col_reset = st.columns(2)
        
        with col_charge:
            if st.button(f"⚡️ {CHARGE_AMOUNT}P 충전", key='charge_low_point', use_container_width=True):
                charge_points()
        with col_reset:
            if st.button("게임 초기화", key='reset_low_point', use_container_width=True):
                reset_state()
    else:
        ### ⚙️ 강화 설정 및 확률 정보
        next_level = current_level + 1
        
        # 베팅 가능한 최대 금액: (현재 포인트 - 고정 비용)
        max_possible_bet = st.session_state.points - fixed_cost
        
        # 슬라이더 값 안정화
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
            f"**총 소모:** **{fixed_cost + bet} P**"
        )
        
        # 3. 강화 실행 버튼
        is_disabled = st.session_state.points < (bet + fixed_cost)
        
        if st.button(f"✨ +{current_level} 강화 시도 (총 비용 {fixed_cost + bet}P)", use_container_width=True, disabled=is_disabled):
            attempt_upgrade(current_level, bet)

### 📊 강화 결과 및 추가 옵션
st.markdown("---")

st.subheader("마지막 강화 결과")
st.markdown(st.session_state.game_result)

# 페이지 하단 충전/초기화 옵션
col_bottom_charge, col_bottom_reset = st.columns(2)

with col_bottom_charge:
    if st.session_state.points < INITIAL_POINTS * 2: # 포인트가 넉넉하지 않을 때만 표시
        if st.button(f"⚡️ {CHARGE_AMOUNT}P 추가 충전", key='charge_any_time', use_container_width=True):
            charge_points()

with col_bottom_reset:
    if st.session_state.points < INITIAL_POINTS or current_level > 1:
        if st.button(f"게임 초기화 ({INITIAL_POINTS}P, +1)", key='reset_any_time', use_container_width=True):
            reset_state()
