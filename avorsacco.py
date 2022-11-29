import streamlit as st
from PIL import Image
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

import database as db

from datetime import datetime
import calendar

# setting variable
page_title = "AVOR TRACKER"
page_icon = ":moneybag:"
layout = "centered"
contributions = ["katana", "hanny",  "edward"]
investments= ["rental", "gas", "farming"]
logo = Image.open("pic/avor.png")
currency = "ksh"

# setting page config

st.set_page_config(page_title = page_title, page_icon = page_icon, layout = layout)

with st.container():
    logo_column, title_column = st.columns((1, 2))
    with logo_column:
        st.image(logo)
    with title_column:
        st.header(page_title)
        st.write("where every cent makes sense")

# setting year and month

years= (datetime.today().year, datetime.today().year +1)
months= list(calendar.month_name[1:])

# --------DATABASE INTERFACE-------
def get_all_periods():
    items = db.fetch_all_periods()
    periods = [item["key"] for item in items]
    return periods


# hiding st style css
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# putting option menu
selected = option_menu(
    menu_title=None,
    options=["data entry", "data visualization"],
    orientation="horizontal"

)

# setting up form
if selected == "data entry":
    st.header(f"Data entry in {currency}")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        col1.selectbox("select month",  months,  key="month")
        col2.selectbox("select year", years, key="year")

        "___"

        with st.expander("contributions"):
            for contribution in contributions:
                st.number_input(f"{contribution}", min_value=0, format="%i", step=10, key=contribution)
        with st.expander("investment"):
            for investment in investments:
                st.number_input(f"{investment}", min_value=0, format="%i",  step=10, key=investment)
        with st.expander("comment"):
            comment = st.text_area(" ", placeholder="enter comment")


    # setting up submit button

        submitted = st.form_submit_button("save data")
        if submitted:
            period = str(st.session_state["year"]) + " -" + str(st.session_state["month"])
            contributions = {contribution: st.session_state[contribution] for contribution in contributions}
            investments = {investment: st.session_state[investment] for investment in investments}
            db.insert_period(period, contributions, investments, comment)
            st.success("data saved")

# plotting the data
if selected == "data visualization":
    st.header( "data visualisation")
    with st.form("saved_period"):
        period= st.selectbox("selected period", get_all_periods())
        submitted = st.form_submit_button("plot period")
        if submitted:
           period_data = db.get_period(period)
           comment = period_data.get("comment")
           investments = period_data.get("investments")
           contributions =period_data.get("contributions")

# create metric
           total_contributions = sum(contributions.values())
           total_investments = sum(investments.values())
           remaining_budget = (total_contributions - total_investments)
           col1, col2, col3, = st.columns(3)
           col1.metric("total contributions:", f"{total_contributions} {currency}")
           col2.metric(f" total investments:", f" { total_investments} {currency}")
           col3.metric(f" remaining budget:", f"{remaining_budget} {currency}")
           st.text(f"comment: {comment }")

    #creating the senky chart
    label = list(contributions.keys()) + ["total contribution"] + list(investments.keys())
    source = list(range(len(contributions))) +[len(contributions)] * len(investments)
    target = [len(contributions)] * len(contributions) + [label.index(investment) for investment in investments]
    value = list(contributions.values()) + list(investments.values())

    #data to dictionary, dictionary to sankey
    link = dict(source= source, target=target, value=value)
    node = dict(label=label, pad=20, thickness= 30, color="#00FF00")
    data = go.Sankey(link=link, node=node)

    #ploting it
    fig = go.Figure(data)
    fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
    st.plotly_chart(fig, use_container_width=True)



