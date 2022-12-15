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
    f = open("深圳市出租车.html", encoding="utf-8")
    html_data = f.read()
    f.close()
    st.components.v1.html(html_data, height=200, scrolling=True)
    st.write("下图是")
    f = open("深圳市OD轨迹.html", encoding="utf-8")
    html_data = f.read()
    f.close()
    st.components.v1.html(html_data, height=400, scrolling=False)
    if st.checkbox('Show dataframe'):
        f = open("深圳市出租车打车点分布.html", encoding="utf-8")
        html_data = f.read()
        f.close()
        st.components.v1.html(html_data, height=400, scrolling=False)
    f = open("k_means_data.html", encoding="utf-8")
    html_data = f.read()
    f.close()
    st.components.v1.html(html_data, height=500, scrolling=True)
    f = open("timeline_pie.html", encoding="utf-8")
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
