import streamlit as st
import streamlit.components.v1 as components
#pipreqs . --encoding=utf8 --force
value_selected = st.sidebar.selectbox(
    'choose an option', options=["数据分析", "交通预测"])
st.sidebar.write("dfafd")
if value_selected == "数据分析":
    with st.sidebar.expander("See explanation"):
        st.write("""
            The chart above shows some numbers I picked for you.
            I rolled actual dice for these, so they're *guaranteed* to
            be random.
        """)
    f = open("原始数据.html", encoding="utf-8")
    html_data = f.read()
    f.close()
    st.components.v1.html(html_data, height=200, scrolling=True)
    st.write("下图是")
    f = open("OD轨迹.html", encoding="utf-8")
    html_data = f.read()
    f.close()
    st.components.v1.html(html_data, height=400, scrolling=False)
    if st.checkbox('Show dataframe'):
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
    with st.sidebar.expander("See explanation"):
        st.write("""
            The chart above shows some numbers I picked for you.
            I rolled actual dice for these, so they're *guaranteed* to
            be random.
        """)
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
