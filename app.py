import streamlit as st
import random

# --- 설정 및 초기화 ---

st.set_page_config(
    page_title="🎲 포인트 주사위 게임 (수정됨)",
    layout="centered"
)

# 세션 상태에 포인트가 없으면 초기값(100)으로 설정
if 'points' not in st.session_state:
    st.session_state.points = 100
if 'game_result' not in st.session_state:
    st.session_state.game_result = "게임을 시작해 보세요!"
if 'last_bet' not in st.session_state:
    st.session_state.last_bet = 10
if 'last_target' not in st.session_state:
    st.session_state.last_target = 3

# --- 함수 정의 ---

def roll_dice(bet_amount, target_number):
    """주사위를 굴리고 포인트를 업데이트하는 핵심 게임 로직"""
    
    # 1. 포인트 부족 여부 최종 확인
    if st.session_state.points < bet_amount:
        st.session_state.game_result = "⚠️ **오류:** 베팅할 포인트가 부족합니다! 금액을 조정해주세요."
        return
        
    # 2. 포인트 차감 (성공/실패 여부와 관계없이 소모)
    st.session_state.points -= bet_amount
    
    # 3. 주사위 굴리기
    dice_roll = random.randint(1, 6)
    
    st.session_state.game_result = f"**🎲 주사위 결과: {dice_roll}**\n\n"
    
    # 4. 승리 조건 확인 (주사위 눈이 목표 숫자보다 크거나 같으면 승리)
    if dice_roll >= target_number:
        # 승리 시 획득 포인트 (건 금액의 2배)
        winnings = bet_amount * 2
        st.session_state.points += winnings
        st.session_state.game_result += f"🎉 **승리!** {winnings} 포인트를 획득했습니다. (현재 포인트: {st.session_state.points})"
    else:
        # 패배 시
        st.session_state.game_result += f"😢 **실패...** 건 포인트 {bet_amount}를 잃었습니다. (현재 포인트: {st.session_state.points})"
    
    # 5. 마지막 결과 저장
    st.session_state.last_roll = dice_roll
    st.session_state.last_bet = bet_amount
    st.session_state.last_target = target_number

# --- Streamlit UI 구성 ---

st.title("🎲 포인트 주사위 굴리기 게임 (수정 버전)")
st.markdown("---")

### 💰 현재 포인트

st.metric(label="현재 보유 포인트", value=f"{st.session_state.points} P")

if st.session_state.points <= 0:
    st.error("포인트가 부족하여 더 이상 게임을 할 수 없습니다! 😥")
    
    # 포인트 초기화 버튼을 명확히 분리
    if st.button("포인트 초기화 (100P)", key='reset_zero', use_container_width=True):
        st.session_state.points = 100
        st.session_state.game_result = "포인트가 초기화되었습니다. 다시 시작하세요!"
        st.rerun()
else:
    ### ⚙️ 게임 설정
    
    # 베팅 금액의 최대값을 가진 포인트 또는 50P 중 작은 값으로 설정 (오류 방지)
    max_bet = min(st.session_state.points, 50)
    
    # 기본 베팅 값 설정. 현재 최대 베팅 금액보다 크지 않게 조정.
    default_bet = min(st.session_state.last_bet, max_bet) if max_bet >= 10 else max_bet
    
    # 1. 베팅 금액 입력
    bet = st.slider(
        "베팅할 포인트 금액을 선택하세요. (최대 50P 또는 현재 포인트)", 
        min_value=10, 
        max_value=max_bet, 
        step=10, 
        value=default_bet,
        disabled=(max_bet < 10) # 포인트가 10 미만이면 비활성화
    )
    
    # 2. 성공 조건 선택
    target = st.select_slider(
        "주사위 눈이 이 숫자 '이상'이 나와야 성공합니다.",
        options=[2, 3, 4, 5, 6],
        value=st.session_state.last_target
    )

    st.info(f"성공 조건: 주사위 눈이 **{target} 이상**\n\n베팅 금액: **{bet} P**\n\n승리 시 획득: **{bet * 2} P**")
    
    ### 🕹️ 게임 실행
    
    # 버튼 클릭 시 게임 실행 및 로직 호출
    if st.button("🔥 주사위 굴리기", use_container_width=True, disabled=(st.session_state.points < bet)):
        roll_dice(bet, target)

### 📊 게임 결과
st.markdown("---")

# 마지막 게임 결과 표시
st.subheader("마지막 게임 결과")
st.markdown(st.session_state.game_result)

# 개발/디버깅을 위한 '포인트 초기화' 버튼 (포인트가 0 초과일 때만 표시)
if st.session_state.points > 0 and st.session_state.points < 100:
    if st.button("포인트 초기화 (100P)", key='reset_normal'):
        st.session_state.points = 100
        st.session_state.game_result = "포인트가 초기화되었습니다. 다시 시작하세요!"
        st.rerun()
