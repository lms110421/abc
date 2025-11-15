import streamlit as st
import random

# --- 설정 및 초기화 ---

st.set_page_config(
    page_title="🎲 포인트 주사위 게임",
    layout="centered"
)

# 세션 상태에 포인트가 없으면 초기값(100)으로 설정
if 'points' not in st.session_state:
    st.session_state.points = 100
if 'game_result' not in st.session_state:
    st.session_state.game_result = "게임을 시작해 보세요!"

# --- 함수 정의 ---

def roll_dice(bet_amount, target_number):
    """주사위를 굴리고 포인트를 업데이트하는 핵심 게임 로직"""
    
    # 1. 포인트 차감 (성공/실패 여부와 관계없이 소모)
    st.session_state.points -= bet_amount
    
    # 2. 주사위 굴리기
    dice_roll = random.randint(1, 6)
    
    st.session_state.game_result = f"**주사위 결과: {dice_roll}**\n\n"
    
    # 3. 승리 조건 확인 (주사위 눈이 목표 숫자보다 크거나 같으면 승리)
    if dice_roll >= target_number:
        # 승리 시 획득 포인트 (건 금액의 2배)
        winnings = bet_amount * 2
        st.session_state.points += winnings
        st.session_state.game_result += f"🎉 **승리!** {winnings} 포인트를 획득했습니다. (현재 포인트: {st.session_state.points})"
    else:
        # 패배 시 (이미 포인트는 차감되었으므로 추가 작업 없음)
        st.session_state.game_result += f"😢 **실패...** 건 포인트 {bet_amount}를
