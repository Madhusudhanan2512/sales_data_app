
import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import ttest_ind
import difflib

st.set_page_config(page_title="Sales Data Analysis", layout="wide")

# Background styling
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("streamlit_background.png");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 Sales Data Analysis & Behavioral Insights")

# Detailed Description
st.markdown("""<small>
<h4>📘 Project Overview</h4>
<b>Objectives</b><br>
<ul>
<li>Plot daily sales for all 50 weeks to understand trends.</li>
<li>Detect and verify statistically significant changes in sales patterns.</li>
<li>Analyze gender influence on sales.</li>
<li>Calculate sales distribution across dayparts: Night, Morning, Afternoon, Evening.</li>
</ul>
<b>Methodology</b><br>
<ul>
<li>Used Python libraries (Pandas, Plotly, SciPy) for data processing and visualization.</li>
<li>Statistical test: t-test for pre- and post-change sales distribution.</li>
<li>Interactive charts used for enhanced exploration.</li>
</ul>
</small>""", unsafe_allow_html=True)

# Directly load built-in dataset
df = pd.read_csv("sales_data_cleaned.csv", parse_dates=["sale_time"])
df["sale_date"] = df["sale_time"].dt.date
df["sale_hour"] = df["sale_time"].dt.hour

def get_daypart(hour):
    if 0 <= hour < 6:
        return "Night"
    elif 6 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 18:
        return "Afternoon"
    else:
        return "Evening"

df["daypart"] = df["sale_hour"].apply(get_daypart)

# Daily sales trend
st.subheader("📅 Daily Sales Trend")
daily_sales = df.groupby("sale_date").size().reset_index(name="sales_count")
fig1 = px.line(daily_sales, x="sale_date", y="sales_count", title="Daily Sales Over Time")
st.plotly_chart(fig1, use_container_width=True)

# Change point detection (basic)
st.subheader("🚨 Change Detection in Sales")
sales_list = daily_sales["sales_count"].values
mid_point = len(sales_list) // 2
group1 = sales_list[:mid_point]
group2 = sales_list[mid_point:]
stat, p = ttest_ind(group1, group2)
change_date = daily_sales["sale_date"].iloc[mid_point]

st.write(f"**Detected change around:** `{change_date}`")
st.write(f"**P-value:** `{p:.5f}`")

if p < 0.05:
    st.success("✅ The change is statistically significant.")
else:
    st.info("ℹ️ No significant change detected.")

# Gender breakdown
st.subheader("👥 Sales by Gender")
gender_sales = df["purchaser_gender"].value_counts().reset_index()
gender_sales.columns = ["Gender", "Count"]
fig2 = px.bar(gender_sales, x="Gender", y="Count", title="Sales by Gender", text_auto=True)
st.plotly_chart(fig2, use_container_width=True)

# Daypart breakdown
st.subheader("🕒 Sales by Daypart")
daypart_sales = df["daypart"].value_counts().reset_index()
daypart_sales.columns = ["Daypart", "Count"]
fig3 = px.pie(daypart_sales, values="Count", names="Daypart", title="Sales Distribution by Daypart")
st.plotly_chart(fig3, use_container_width=True)

# FAQ chatbot logic
faq = {
    "What is the objective of this project?": "To analyze daily sales, detect significant changes, and understand patterns based on gender and time of day.",
    "What is the detected change date?": f"The model detected a significant change in sales around {change_date}.",
    "What is the p-value?": f"The p-value is {p:.5f}, which indicates the statistical significance of the change.",
    "What does a low p-value mean?": "A low p-value (< 0.05) means the change in sales is statistically significant and unlikely due to random chance.",
    "What is daypart analysis?": "It breaks each day into segments like Morning, Afternoon, Evening, and Night to observe time-based patterns in sales.",
    "What is the gender distribution in sales?": "The bar chart shows how sales are distributed across male and female customers."
}

def get_faq_response(user_question):
    matches = difflib.get_close_matches(user_question, faq.keys(), n=1, cutoff=0.4)
    if matches:
        return faq[matches[0]]
    else:
        return "Sorry, I couldn't find a matching answer. Try rephrasing your question."

st.markdown("---")
st.subheader("💬 Ask a Question About This Project")
st.caption("Try asking questions like: *What is the p-value?*, *What does daypart analysis mean?*, or *What is the objective of this project?*")
question = st.text_input("What do you want to know?")
if question:
    st.write("🔍 Searching for the best answer...")
    response = get_faq_response(question)
    st.info(f"🤖 {response}")
