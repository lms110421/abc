import streamlit as st
import random

# --- 게임 설정 ---
INITIAL_BALANCE = 10000
BET_AMOUNT = 1000

# 슬롯 심볼 및 배당 설정
SYMBOLS = ['🍒', '🔔', '⭐', '💎']
PAYOUTS = {
    3: 5000,  # 트리플 일치 시 5,000 포인트 획득
    2: 1500   # 더블 일치 시 1,500 포인트 획득
}

# --- 세션 상태 초기화 ---
if 'balance' not in st.session_state:
    st.session_state.balance = INITIAL_BALANCE
if 'reels' not in st.session_state:
    st.session_state.reels = ['❓', '❓', '❓']
if 'slot_message' not in st.session_state:
    st.session_state.slot_message = "아래 버튼을 눌러 슬롯을 돌리세요!"

st.title('🎰 이모티콘 슬롯 머신')
st.write(f'현재 잔액: **{st.session_state.balance:,}** 포인트')
st.write(f'한 번 돌릴 때마다 **{BET_AMOUNT:,}** 포인트가 베팅됩니다.')

st.markdown('---')

# --- 잔액 확인 및 게임 가능 여부 ---
if st.session_state.balance < BET_AMOUNT:
    st.error("잔액 부족! 최소 시도 금액 1,000 포인트가 필요합니다.")
    if st.button('잔액 충전 (10,000 포인트)'):
        st.session_state.balance = INITIAL_BALANCE
        st.session_state.slot_message = "잔액이 충전되었습니다!"
        st.experimental_rerun()
    st.stop() 


### 1. 현재 슬롯 상태 표시
st.markdown(
    f"<h1 style='text-align: center; font-size: 80px; margin: 20px 0;'>{' '.join(st.session_state.reels)}</h1>", 
    unsafe_allow_html=True
)

st.markdown('---')

### 2. 슬롯 돌리기 버튼
if st.button('릴 돌리기! 🔄'):
    # 1. 잔액 차감 (베팅)
    st.session_state.balance -= BET_AMOUNT
