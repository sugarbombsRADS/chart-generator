import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
import io

# 让图表支持中文
matplotlib.rcParams['font.family'] = 'DFPHeiW7-GB Regular'  # 微软雅黑
matplotlib.rcParams['axes.unicode_minus'] = False  # 让负号正常显示

st.title("辅助能力数据表生成工具")
st.write("输入数据来生成图标折线图，并可导出为 PNG 图片。")

x = st.text_input("属性数值（逗号分隔）", "1, 15, 30, 60, 100")
y = st.text_input("效果数值（逗号分隔）", "10, 40, 65, 85, 100")

x_label = st.text_input("属性名称", "Strength")
y_label = st.text_input("效果名称", "Carry Weight")
title = st.text_input("辅助能力名称", "Strong Back")

# 转换字符串为数字列表
try:
    x_values = list(map(float, x.split(",")))
    y_values = list(map(float, y.split(",")))

    if len(x_values) != len(y_values):
        st.error("X 和 Y 的数值个数必须相等。")
    else:
        # 绘图
        fig, ax = plt.subplots()
        ax.plot(x_values, y_values, marker='o')
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        st.pyplot(fig)

        # 保存图像为 buffer
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)

        # 下载按钮
        st.download_button(
            label="📥 下载图表 PNG",
            data=buf,
            file_name="chart.png",
            mime="image/png"
        )

except ValueError:
    st.error("请输入有效的数字，使用英文逗号分隔。")
