import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Hàm tính toán SJF
def calculate_sjf(processes):
    processes = sorted(processes, key=lambda x: (x[1], x[2]))
    time = 0
    schedule = []
    results = []
    for process in processes:
        pid, arrival, burst = process
        if time < arrival:
            time = arrival
        start_time = time
        finish_time = start_time + burst
        turnaround = finish_time - arrival
        waiting = turnaround - burst
        results.append((pid, arrival, burst, start_time, finish_time, turnaround, waiting))
        schedule.append((pid, start_time, finish_time))
        time = finish_time
    return results, schedule

# Hàm vẽ biểu đồ Gantt
def draw_gantt_chart(schedule):
    fig, ax = plt.subplots(figsize=(10, 4))
    for process_id, start, finish in schedule:
        ax.barh(0, finish - start, left=start, align='center', edgecolor='black', color='skyblue')
        ax.text((start + finish) / 2, 0, f"P{process_id}", ha='center', va='center', color='black', fontsize=10)
    ax.set_yticks([])
    ax.set_xlabel("Thời gian")
    ax.set_title("Biểu đồ Gantt")
    st.pyplot(fig)

# Giao diện Streamlit
st.title("Demo thuật toán SJF (Shortest Job First)")

# Hiển thị thông tin ở Sidebar
st.sidebar.header("Nhập thông tin tiến trình")
num_processes = st.sidebar.number_input("Số lượng tiến trình", min_value=1, max_value=20, value=3, step=1)

process_data = []
if num_processes > 0:
    for i in range(num_processes):
        arrival = st.sidebar.number_input(f"Thời điểm đến của P{i+1} (ms)", min_value=0, value=0, step=1, key=f"arrival_{i}")
        burst = st.sidebar.number_input(f"Thời gian sử dụng CPU của P{i+1} (ms)", min_value=1, value=1, step=1, key=f"burst_{i}")
        process_data.append((i + 1, arrival, burst))

# Nút tính toán
if st.sidebar.button("Tính toán"):
    if len(process_data) > 0:
        results, schedule = calculate_sjf(process_data)

        # Chuyển đổi kết quả thành DataFrame
        df = pd.DataFrame(results, columns=[
            "Tiến trình", "Thời điểm đến (ms)", "Thời gian sử dụng CPU (ms)", 
            "Thời gian bắt đầu (ms)", "Thời gian kết thúc (ms)", 
            "Thời gian lưu lại (ms)", "Thời gian chờ (ms)"
        ])

        # Hiển thị bảng kết quả
        st.subheader("Kết quả:")
        st.dataframe(df)

        # Hiển thị biểu đồ Gantt
        st.subheader("Biểu đồ Gantt:")
        draw_gantt_chart(schedule)
    else:
        st.warning("Chưa có tiến trình nào được nhập. Vui lòng nhập thông tin tiến trình.")
else:
    st.info("Vui lòng nhập thông tin tiến trình ở thanh bên trái và bấm 'Tính toán' để xem kết quả.")
