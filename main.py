import streamlit as st
import streamlit.components.v1 as components
import zipfile


#pipreqs . --encoding=utf8 --force
st.sidebar.title("基于ANN神经网络的城市交通状态短时预测系统和可视化分析——以深圳市为例")
value_selected = st.sidebar.selectbox(
    'choose an option', options=["数据分析", "交通预测"])
if value_selected == "数据分析":
    st.success("此项目使用的数据主要为出租车 GPS 轨迹数据，主要包含车辆 ID、日期、时间、经度和纬度等字段。一般车载 GPS 定位时间间隔 3-10 秒不等，通过连续的点我们可以识别出车辆的运动轨迹、速度以及一个区域道路的交通流量等表征交通状态的一些特征。因此出租车数据是很好的交通状态预测数据源")
    st.markdown("下图是原始数据**部分预览**")
    f = open("原始数据.html", encoding="utf-8")
    html_data = f.read()
    f.close()
    st.components.v1.html(html_data, height=200, scrolling=True)
    st.write("下图是对深圳市出租车数据的动态可视化：")
    f = open("OD轨迹.html", encoding="utf-8")
    html_data = f.read()
    f.close()
    st.components.v1.html(html_data, height=400, scrolling=False)
    if st.checkbox('Show'):
        f = open("打车点分布.html", encoding="utf-8")
        html_data = f.read()
        f.close()
        st.components.v1.html(html_data, height=400, scrolling=False)
    f = open("特征.html", encoding="utf-8")
    html_data = f.read()
    f.close()
    st.components.v1.html(html_data, height=500, scrolling=True)
    f = open("交通状况.html", encoding="utf-8")
    html_data = f.read()
    f.close()
    st.components.v1.html(html_data, height=500, scrolling=False)

else:
    f = open("真实值.html", encoding="utf-8")
    html_data = f.read()
    f.close()
    st.components.v1.html(html_data, height=500, scrolling=False)
    f = open("预测值.html", encoding="utf-8")
    html_data = f.read()
    f.close()
    st.components.v1.html(html_data, height=500, scrolling=False)
    f = open("预测误差.html", encoding="utf-8")
    html_data = f.read()
    f.close()
    st.components.v1.html(html_data, height=500, scrolling=False)
    f = open("预测率.html", encoding="utf-8")
    html_data = f.read()
    f.close()
    st.components.v1.html(html_data, height=500, scrolling=False)
    f = open("准确率图示.html", encoding="utf-8")
    html_data = f.read()
    f.close()
    st.components.v1.html(html_data, height=500, scrolling=False)
