import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import font_manager
import io
import os

# 🔤 加载中文字体
font_path = "fonts/DFPHeiW7-GB Regular.ttf"
if not os.path.exists(font_path):
    st.error("❌ 找不到字体文件，请确保它在 fonts 文件夹下")
else:
    font_prop = font_manager.FontProperties(fname=font_path)

    st.title("辅助能力数据生成工具（支持中文与参考线）")
    st.write("输入数据生成图表，可导出 PNG，支持添加参考线与中文显示")

    x = st.text_input("属性数值（逗号分隔）", "1, 15, 30, 60, 100")
    y = st.text_input("效果数值（逗号分隔）", "10, 40, 65, 85, 100")

    x_label = st.text_input("属性名称", "力量")
    y_label = st.text_input("效果名称", "负重")
    title = st.text_input("图表标题", "负重提升曲线")

    st.markdown("### ➕ 可选：添加参考线")
    add_hline = st.checkbox("添加横向参考线（Y）")
    hline_y = st.number_input("横向参考线 Y 值", value=80)
    hline_label = st.text_input("横向线标签", "负重预警线（80）")

    add_vline = st.checkbox("添加纵向参考线（X）")
    vline_x = st.number_input("纵向参考线 X 值", value=30)
    vline_label = st.text_input("纵向线标签", "力量阈值（30）")

    try:
        x_values = list(map(float, x.split(",")))
        y_values = list(map(float, y.split(",")))

        if len(x_values) != len(y_values):
            st.error("X 和 Y 的数值个数必须一致！")
        else:
            fig, ax = plt.subplots()
            ax.plot(x_values, y_values, marker='o')

            # 设置刻度
            ax.set_xticks([1, 15, 30, 60, 100])

            # 添加标签和标题（用中文字体）
            ax.set_xlabel(x_label, fontproperties=font_prop)
            ax.set_ylabel(y_label, fontproperties=font_prop)
            ax.set_title(title, fontproperties=font_prop)

            # 添加参考线
            if add_hline:
                ax.axhline(y=hline_y, color='r', linestyle='--', linewidth=1, label=hline_label)
            if add_vline:
                ax.axvline(x=vline_x, color='g', linestyle=':', linewidth=1, label=vline_label)

            # 图例
            if add_hline or add_vline:
                ax.legend(prop=font_prop)

            st.pyplot(fig)

            # 图片导出
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)
            st.download_button("📥 下载图表 PNG", data=buf, file_name="chart.png", mime="image/png")

    except ValueError:
        st.error("请输入有效的数字，使用英文逗号分隔。")
