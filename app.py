import streamlit as st
import random

# --- 설정 및 초기화 (수정 없음) ---

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

# --- 핵심 함수 (수정 없음) ---

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

st.markdown("---")

## ⚙️ 게임 설정 및 실행

# 0. 포인트 부족 처리
if st.session_state.points < MIN_BET:
    st.error(f"포인트가 **{MIN_BET}P** 미만입니다! 더 이상 게임을 할 수 없습니다. 😥")
    if st.button(f"포인트 초기화 ({INITIAL_POINTS}P)", key='reset_zero', use_container_width=True):
        reset_points()
    # 포인트가 부족하면 아래 게임 설정 섹션은 건너뜀
else:
    # 1. 베팅 금액 설정
    max_bet = min(st.session_state.points, MAX_BET_LIMIT)
    
    # 슬라이더 기본값 설정 (마지막 베팅 값과 현재 최대 베팅 금액 비교)
    default_bet = min(st.session_state.last_bet, max_bet)
    
    # 👇👇👇 이 부분이 보완되었습니다. 👇👇👇
    # MIN_BET(100)보다 포인트가 많은 경우에만 이 블록에 진입하므로,
    # 슬라이더의 최소값은 MIN_BET으로 고정하는 것이 논리적입니다.
    
    bet = st.slider(
        f"베팅할 포인트 금액을 선택하세요. (최소 **{MIN_BET}P** / 최대 **{max_bet}P**)", 
        min_value=MIN_BET, # min_slider 대신 MIN_BET으로 고정
        max_value=max_bet, 
        step=MIN_BET, 
        value=default_bet,
        key='bet_slider'
    )
    # 👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆

    
    # 2. 홀짝 선택
    choice = st.radio(
        "주사위 눈이 **홀수**일까요, **짝수**일까요?",
        options=["홀수", "짝수"],
        index=0 if st.session_state.last_choice == "홀수" else 1,
        horizontal=True,
        key='choice_radio'
    )

    st.info(f"선택: **{choice}** | 베팅 금액: **{bet} P** | 승리 시 획득: **{bet * WIN_MULTIPLIER} P**")
    
    # 3. 게임 실행 버튼
    # 버튼 비활성화 조건: 선택된 베팅 금액보다 보유 포인트가 적거나, 최소 베팅 금액 미만일 경우
    # (슬라이더 min_value 고정으로 'bet < MIN_BET' 조건은 사실상 불필요하지만 안전을 위해 유지)
    is_disabled = (st.session_state.points < bet) or (bet < MIN_BET)
    
    if st.button("🔥 주사위 굴리기 실행", use_container_width=True, disabled=is_disabled):
        roll_dice_odd_even(bet, choice)

## 📊 게임 결과
st.markdown("---")

st.subheader("마지막 게임 결과")
st.markdown(st.session_state.game_result)

# 포인트 충전 (초기화) 버튼
# 초기 포인트(1000P) 미만이고 0P 이상일 때만 버튼 표시
if st.session_state.points < INITIAL_POINTS and st.session_state.points >= MIN_BET:
    if st.button(f"포인트 충전 ({INITIAL_POINTS}P로 초기화)", key='reset_normal', use_container_width=True):
        reset_points()
