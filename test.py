import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

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

def main():
    st.title("WaterSave 앱")

    menu = st.sidebar.selectbox(
        "메뉴 선택",
        ["물 사용량 기록", "사용량 시각화", "행동 기록", "절약 목표 설정", "수도 요금 계산"]
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

if __name__ == "__main__":
    main()