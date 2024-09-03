import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import anthropic
import os

# Streamlit Cloud의 secrets에서 API 키를 가져오거나, 환경 변수에서 가져옵니다.
ANTHROPIC_API_KEY = st.secrets.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")

if not ANTHROPIC_API_KEY:
    st.error("Anthropic API 키가 설정되지 않았습니다. Streamlit Secrets 또는 환경 변수를 확인해주세요.")
    st.stop()

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# 가상의 데이터베이스 대신 사용할 전역 변수
water_usage_data = {}
user_behavior_data = {}

def record_water_usage():
    st.subheader("물 사용량 기록")
    date = st.date_input("날짜 선택")
    usage = st.number_input("물 사용량 (리터)", min_value=0.0, step=0.1)
    if st.button("기록"):
        water_usage_data[str(date)] = usage
        st.success("기록되었습니다!")

def visualize_water_usage():
    st.subheader("물 사용량 시각화")
    if water_usage_data:
        df = pd.DataFrame(list(water_usage_data.items()), columns=['Date', 'Usage'])
        df['Date'] = pd.to_datetime(df['Date'])
        fig = px.line(df, x='Date', y='Usage', title='일간 물 사용량')
        st.plotly_chart(fig)
    else:
        st.info("기록된 데이터가 없습니다.")

def record_user_behavior():
    st.subheader("물 사용 행동 기록")
    date = st.date_input("날짜 선택", key="behavior_date")
    shower_time = st.number_input("샤워 시간 (분)", min_value=0, step=1)
    laundry_loads = st.number_input("세탁 횟수", min_value=0, step=1)
    if st.button("행동 기록"):
        user_behavior_data[str(date)] = {"shower_time": shower_time, "laundry_loads": laundry_loads}
        st.success("행동이 기록되었습니다!")

def set_saving_goal():
    st.subheader("절약 목표 설정")
    current_avg = sum(water_usage_data.values()) / len(water_usage_data) if water_usage_data else 0
    goal = st.number_input("일일 물 사용 목표량 (리터)", min_value=0.0, step=0.1, value=current_avg * 0.9)
    if st.button("목표 설정"):
        st.session_state.saving_goal = goal
        st.success(f"목표가 {goal}리터로 설정되었습니다!")

def calculate_water_bill():
    st.subheader("가상 수도 요금 계산기")
    monthly_usage = st.number_input("월간 물 사용량 (리터)", min_value=0.0, step=1.0)
    # 가상의 요금 체계
    base_rate = 5000  # 기본 요금
    unit_price = 1000  # 1000리터당 가격
    bill = base_rate + (monthly_usage // 1000) * unit_price
    st.write(f"예상 수도 요금: {bill}원")

def ai_water_saving_assistant():
    st.subheader("AI 물 절약 어시스턴트")
    user_question = st.text_input("물 절약에 대해 질문해 주세요:")
    if user_question:
        prompt = f"""사용자 질문: {user_question}

        당신은 물 절약 전문가입니다. 위 질문에 대해 전문적이고 실용적인 조언을 제공해 주세요. 
        가능하다면 구체적인 수치와 함께 설명해 주시고, 실천하기 쉬운 팁도 함께 제공해 주세요."""

        try:
            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            st.write(response.content[0].text)
        except Exception as e:
            st.error(f"AI 응답 생성 중 오류가 발생했습니다: {str(e)}")

def ai_usage_pattern_analysis():
    st.subheader("AI 사용 패턴 분석")
    if water_usage_data:
        df = pd.DataFrame(list(water_usage_data.items()), columns=['Date', 'Usage'])
        df['Date'] = pd.to_datetime(df['Date'])
        average_usage = df['Usage'].mean()
        max_usage = df['Usage'].max()
        min_usage = df['Usage'].min()

        analysis_prompt = f"""다음은 사용자의 물 사용 데이터입니다:
        평균 사용량: {average_usage:.2f}L
        최대 사용량: {max_usage:.2f}L
        최소 사용량: {min_usage:.2f}L

        이 데이터를 바탕으로 사용자의 물 사용 패턴을 분석하고, 개선할 점과 절약 팁을 제공해주세요."""

        try:
            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": analysis_prompt}
                ]
            )
            st.write(response.content[0].text)
        except Exception as e:
            st.error(f"AI 분석 중 오류가 발생했습니다: {str(e)}")
    else:
        st.info("분석할 데이터가 충분하지 않습니다. 더 많은 데이터를 입력해 주세요.")

def ai_personalized_challenge():
    st.subheader("AI 맞춤형 절약 챌린지")
    if user_behavior_data:
        behavior_summary = ", ".join([f"{k}: {v}" for k, v in user_behavior_data.items()])
        challenge_prompt = f"""사용자의 물 사용 행동 데이터: {behavior_summary}

        위 데이터를 바탕으로 사용자에게 맞춤형 물 절약 챌린지를 제안해주세요. 
        챌린지는 구체적이고 측정 가능하며, 달성 가능한 목표여야 합니다."""

        try:
            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=300,
                messages=[
                    {"role": "user", "content": challenge_prompt}
                ]
            )
            st.write(response.content[0].text)
        except Exception as e:
            st.error(f"AI 챌린지 생성 중 오류가 발생했습니다: {str(e)}")
    else:
        st.info("맞춤형 챌린지를 생성하기 위한 데이터가 부족합니다. 먼저 물 사용 행동을 기록해 주세요.")

def main():
    st.title("WaterSave 앱")

    menu = st.sidebar.selectbox(
        "메뉴 선택",
        ["물 사용량 기록", "사용량 시각화", "행동 기록", "절약 목표 설정", "수도 요금 계산",
         "AI 물 절약 어시스턴트", "AI 사용 패턴 분석", "AI 맞춤형 절약 챌린지"]
    )

    if menu == "물 사용량 기록":
        record_water_usage()
    elif menu == "사용량 시각화":
        visualize_water_usage()
    elif menu == "행동 기록":
        record_user_behavior()
    elif menu == "절약 목표 설정":
        set_saving_goal()
    elif menu == "수도 요금 계산":
        calculate_water_bill()
    elif menu == "AI 물 절약 어시스턴트":
        ai_water_saving_assistant()
    elif menu == "AI 사용 패턴 분석":
        ai_usage_pattern_analysis()
    elif menu == "AI 맞춤형 절약 챌린지":
        ai_personalized_challenge()

if __name__ == "__main__":
    main()