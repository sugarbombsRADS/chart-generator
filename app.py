import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager
import io
import os

# 📌 加载自带字体，用于中文显示
font_path = "DFPHeiW7-GB Regular.ttf"
if os.path.exists(font_path):
    font_prop = font_manager.FontProperties(fname=font_path)
    matplotlib.rcParams['font.family'] = font_prop.get_name()
else:
    matplotlib.rcParams['font.family'] = 'SimHei'  # 默认尝试黑体
matplotlib.rcParams['axes.unicode_minus'] = False

st.title("辅助能力数据图表生成工具")
st.write("输入数据来生成图表，并可导出为 PNG 图片。支持添加参考线和中文显示。")

x = st.text_input("属性数值（逗号分隔）", "1, 15, 30, 60, 100")
y = st.text_input("效果数值（逗号分隔）", "10, 40, 65, 85, 100")

x_label = st.text_input("属性名称", "力量")
y_label = st.text_input("效果名称", "负重")
title = st.text_input("图表标题", "负重提升曲线")

# 🧩 参考线功能
st.markdown("### ➕ 可选：添加参考线")
add_hline = st.checkbox("添加横向参考线（Y）")
hline_y = st.number_input("横向参考线 Y 值", value=80)
hline_label = st.text_input("横向线标签", "负重预警线（80）")

add_vline = st.checkbox("添加纵向参考线（X）")
vline_x = st.number_input("纵向参考线 X 值", value=30)
vline_label = st.text_input("纵向线标签", "力量阈值（30）")

# 🚀 图表绘制部分
try:
    x_values = list(map(float, x.split(",")))
    y_values = list(map(float, y.split(",")))

    if len(x_values) != len(y_values):
        st.error("X 和 Y 的数值个数必须一致！")
    else:
        fig, ax = plt.subplots()
        ax.plot(x_values, y_values, marker='o')

        # 固定 X 轴刻度
        ax.set_xticks([1, 15, 30, 60, 100])

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)

        # 添加横线
        if add_hline:
            ax.axhline(y=hline_y, color='r', linestyle='--', linewidth=1, label=hline_label)

        # 添加竖线
        if add_vline:
            ax.axvline(x=vline_x, color='g', linestyle=':', linewidth=1, label=vline_label)

        # 图例
        if add_hline or add_vline:
            ax.legend()

        st.pyplot(fig)

        # 导出按钮
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)

        st.download_button("📥 下载图表 PNG", data=buf, file_name="chart.png", mime="image/png")

except ValueError:
    st.error("请输入有效的数字，使用英文逗号分隔。")
