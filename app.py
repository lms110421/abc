import streamlit as st
import random

# --- 설정 및 초기화 (수정됨) ---

st.set_page_config(
    page_title="🎲 포인트 홀짝 주사위 게임 (3배 보상)",
    layout="centered"
)

# 세션 상태 초기값 정의
INITIAL_POINTS = 1000  # 1000P로 변경
MAX_BET_LIMIT = 500    # 500P로 변경
MIN_BET = 100          # 100P로 변경
WIN_MULTIPLIER = 3     # 승리 시 3배 획득

# 세션 상태 초기화
if 'points' not in st.session_state:
    st.session_state.points = INITIAL_POINTS
if 'game_result' not in st.session_state:
    st.session_state.game_result = f"게임을 시작해 보세요! **{INITIAL_POINTS}P**로 시작합니다."
if 'last_bet' not in st.session_state:
    st.session_state.last_bet = MIN_BET
if 'last_choice' not in st.session_state:
    st.session_state.last_choice = "짝수"
if 'last_roll_icon' not in st.session_state:
    st.session_state.last_roll_icon = ""

# 주사위 눈 아이콘 매핑 (시각적 개선)
DICE_ICONS = {
    1: "⚀", 2: "⚁", 3: "⚂", 
    4: "⚃", 5: "⚄", 6: "⚅"
}

# --- 핵심 함수 ---

def roll_dice_odd_even(bet_amount, user_choice):
    """홀짝 주사위를 굴리고 포인트를 업데이트하는 핵심 게임 로직"""
    
    # 1. 포인트 부족 여부 최종 확인
    if st.session_state.points < bet_amount or bet_amount < MIN_BET:
        st.session_state.game_result = f"⚠️ **오류:** 베팅 금액을 확인해주세요. 최소 **{MIN_BET}P** 이상, 보유 포인트 이하여야 합니다."
        return
        
    # 2. 포인트 차감 (소모)
    st.session_state.points -= bet_amount
    
    # 3. 주사위 굴리기
    dice_roll = random.randint(1, 6)
    
    # 주사위 결과 판정
    is_even = (dice_roll % 2 == 0)
    dice_result_text = "짝수" if is_even else "홀수"
    
    # 결과 아이콘 저장
    st.session_state.last_roll_icon = DICE_ICONS.get(dice_roll, "")

    st.session_state.game_result = (
        f"**{st.session_state.last_roll_icon} 주사위 결과: {dice_roll} ({dice_result_text})**\n\n"
    )
    
    # 4. 승리/패배 처리
    is_win = (user_choice == dice_result_text)
    
    if is_win:
        # 승리 시 3배 획득 (원금 포함)
        winnings = bet_amount * WIN_MULTIPLIER
        st.session_state.points += winnings
        st.session_state.game_result += (
            f"🎉 **대승!** 베팅 금액 **{bet_amount}P**의 {WIN_MULTIPLIER}배인 **{winnings}P**를 획득했습니다. "
            f"(현재 포인트: {st.session_state.points}P)"
        )
    else:
        st.session_state.game_result += (
            f"😢 **패배...** 건 포인트 **{bet_amount}P**를 모두 잃었습니다. "
            f"(현재 포인트: {st.session_state.points}P)"
        )
    
    # 5. 마지막 결과 저장
    st.session_state.last_bet = bet_amount
    st.session_state.last_choice = user_choice

def reset_points():
    """포인트를 초기화하고 페이지를 다시 로드합니다."""
    st.session_state.points = INITIAL_POINTS
    st.session_state.game_result = f"포인트가 **{INITIAL_POINTS}P**로 초기화되었습니다. 다시 시작하세요!"
    st.rerun()

# --- Streamlit UI 구성 ---

st.title("💰 홀짝 주사위 게임 (3배 찬스)")
st.markdown("---")

## 📈 현재 포인트 현황

col_metric, col_icon = st.columns([3, 1])

# 현재 포인트 표시
col_metric.metric(label="현재 보유 포인트", value=f"{st.session_state.points} P")

# 마지막 주사위 눈 아이콘 표시
col_icon.markdown(
    f"<h1 style='text-align: right; margin: 0;'>{st.session_state.last_roll_icon}</h1>", 
    unsafe_allow_html=True
)

st.markdown("
