import streamlit as st
import random

# --- 초기 설정 및 잔액 관리 ---
INITIAL_BALANCE = 10000
BET_AMOUNT = 1000
WIN_AMOUNT = 2000

# 세션 상태 초기화
if 'balance' not in st.session_state:
    st.session_state.balance = INITIAL_BALANCE
if 'card_deck' not in st.session_state:
    # 4개의 카드를 준비합니다. (예: A, K, Q, J)
    st.session_state.card_deck = ['A', 'K', 'Q', 'J']
if 'secret_card' not in st.session_state:
    st.session_state.secret_card = random.choice(st.session_state.card_deck)
if 'game_message' not in st.session_state:
    st.session_state.game_message = "게임을 시작합니다! 카드를 선택하세요."

st.title('🃏 가상 포인트 카드 예측 게임')
st.write(f'현재 잔액: **{st.session_state.balance:,}** 포인트')
st.write(f'한 번 시도할 때마다 **{BET_AMOUNT:,}** 포인트가 차감되며, 맞추면 **{WIN_AMOUNT:,}** 포인트를 얻습니다.')

st.markdown('---')

# --- 잔액 확인 및 게임 시작 가능 여부 ---
if st.session_state.balance < BET_AMOUNT:
    st.error("잔액 부족! 최소 시도 금액 1,000 포인트가 필요합니다.")
    if st.button('잔액 충전 (10,000 포인트)'):
        st.session_state.balance = INITIAL_BALANCE
        st.session_state.game_message = "잔액이 충전되었습니다!"
        st.experimental_rerun()
    st.stop() 


### 1. 사용자 예측 (카드 선택)
user_choice = st.radio(
    '어떤 카드가 뽑힐까요?',
    st.session_state.card_deck,
    index=None # 기본 선택 없음
)

st.markdown('---')

### 2. 카드 예측 버튼
if st.button('카드 예측하기!'):
    if user_choice is None:
        st.warning('⚠️ 카드를 먼저 선택해 주세요.')
    else:
        # --- 게임 로직 시작 ---
        
        # 1. 잔액 차감 (베팅)
        st.session_state.balance -= BET_AMOUNT
        
        # 2. 결과 확인
        is_win = (user_choice == st.session_state.secret_card)

        st.subheader('결과 확인!')
        
        # 3. 결과에 따른 포인트 계산 및 메시지 업데이트
        if is_win:
            # 승리: 2000 포인트 획득 (차감된 1000포인트 + 1000포인트 이익)
            st.session_state.balance += WIN_AMOUNT
            st.session_state.game_message = (
                f'🎉 **정답입니다!** 뽑힌 카드는 **{st.session_state.secret_card}**! '
                f'{WIN_AMOUNT:,} 포인트를 획득했습니다.'
            )
            st.success(st.session_state.game_message)
            st.balloons()
        else:
            # 패배: 1000 포인트만 잃음 (추가 포인트 없음)
            st.session_state.game_message = (
                f'😭 **아쉽네요!** 뽑힌 카드는 **{st.session_state.secret_card}**였습니다. '
                f'{BET_AMOUNT:,} 포인트를 잃었습니다.'
            )
            st.error(st.session_state.game_message)

        # 4. 다음 라운드를 위해 비밀 카드 새로 뽑기
        st.session_state.secret_card = random.choice(st.session_state.card_deck)
        
        # 잔액 및 메시지 업데이트를 위해 재실행
        st.experimental_rerun()

else:
    # 버튼을 누르기 전에 마지막 메시지 표시
    st.info(st.session_state.game_message)
