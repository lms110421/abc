import streamlit as st
import random

# --- 설정 및 초기화 ---

# 페이지 설정
st.set_page_config(
    page_title="🎲 홀짝 주사위 게임 (최종 수정)",
    layout="centered"
)

# 세션 상태 초기화 (초기값 설정)
if 'points' not in st.session_state:
    st.session_state.points = 100
if 'game_result' not in st.session_state:
    st.session_state.game_result = "게임을 시작해 보세요! 100P로 시작합니다."
if 'last_bet' not in st.session_state:
    st.session_state.last_bet = 10
if 'last_choice' not in st.session_state:
    st.session_state.last_choice = "짝수"

# --- 함수 정의 ---

def roll_dice_odd_even(bet_amount, user_choice):
    """홀짝 주사위를 굴리고 포인트를 업데이트하는 핵심 게임 로직"""
    
    # 1. 포인트 부족 여부 최종 확인
    if st.session_state.points < bet_amount:
        st.session_state.game_result = "⚠️ **오류:** 베팅할 포인트가 부족합니다! 금액을 조정하거나 포인트를 초기화하세요."
        return
        
    # 2. 포인트 차감 (성공/실패 여부와 관계없이 소모)
    st.session_state.points -= bet_amount
    
    # 3. 주사위 굴리기
    dice_roll = random.randint(1, 6)
    
    # 주사위 결과 판정
    is_even = (dice_roll % 2 == 0) # 짝수이면 True
    dice_result_text = "짝수" if is_even else "홀수"
    
    st.session_state.game_result = f"**🎲 주사위 결과: {dice_roll} ({dice_result_text})**\n\n"
    
    # 4. 승리 조건 확인
    is_win = (user_choice == dice_result_text)
    
    if is_win:
        # 승리 시 획득 포인트 (건 금액의 2배)
        winnings
