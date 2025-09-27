import streamlit as st
from streamlit_option_menu import option_menu
from utils.sentiment_analysis import sentiment
from utils.clean_data import dict_data,save_csv,relative_to_date,generate_rating
import pandas as pd
import re
from utils.statistic import total_review_num,all_review_list,star_count,pos_neg_num
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
import ast
from utils.discussion import top_streangth,top_weakness,top_compliment,top_complaint,actionable_recommendation,manu_item_insight
from save_html import save_html_file
nltk.download("stopwords")
from nltk.corpus import stopwords
import json

HTML_FILE='page.html'
RAW_DATA_FILE='raw_data.csv'
PROCESS_DATA_FILE='process_data.csv'

total_review=total_review_num(HTML_FILE)

one_star,two_star,three_star,four_star,five_star,all_star=star_count(HTML_FILE)
total_star=(1*one_star)+(2*two_star)+(3*three_star)+(4*four_star)+(5*five_star)
avarage_rating=round(total_star/total_review,2)


pos,neg=pos_neg_num(PROCESS_DATA_FILE)


Positive_Review_Percentage=round((pos/total_review)*100,2)
Negative_Review_Percentage=round((neg/total_review)*100,2)

# -------------------------------------
total_reviews = total_review
total_stars = total_star
total_positive_review = pos
total_negative_review = neg
avg_rating=avarage_rating
total_positive_review_percentage=Positive_Review_Percentage
total_negative_review_percentage=Negative_Review_Percentage



star_counts = {
    5: all_star['five_star'],
    4: all_star['four_star'],
    3: all_star['three_star'],
    2: all_star['two_star'],
    1: all_star['one_star']
}
# ---------------------------------------


st.title('Review Report')


with st.sidebar:
    st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", use_container_width=True)

    st.markdown("### 📂 Category")

    selected = option_menu(
        menu_title=None,  # No main title
        options=["Statistic", "Discussion", "Review", "Table"],
        icons=["bar-chart", "chat-dots", "star", "table"],  # Bootstrap icons
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px", },
            "icon": {"color": "orange", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"5px", "--hover-color": "#5c5c5f"},
            "nav-link-selected": {"background-color": "#ff4b4b", "color": "white"},
        }
    )
if selected=='Statistic':
    # Example stats (replace with your calculated values)
    

    st.markdown("## 📊 Statistics Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div style="background-color:#FF4B4B;padding:20px;border-radius:15px;text-align:center;box-shadow:2px 2px 10px rgba(0,0,0,0.2)">
                <h3 style="color:white;">Total Reviews</h3>
                <h2 style="color:white;">{total_reviews}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="background-color:#FFB703;padding:20px;border-radius:15px;text-align:center;box-shadow:2px 2px 10px rgba(0,0,0,0.2)">
                <h3 style="color:white;">Total Stars</h3>
                <h2 style="color:white;">{total_stars}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div style="background-color:#06D6A0;padding:20px;border-radius:15px;text-align:center;box-shadow:2px 2px 10px rgba(0,0,0,0.2)">
                <h3 style="color:white;">Total Positive Review</h3>
                <h2 style="color:white;">{total_positive_review}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div style="background-color:#118AB2;padding:20px;border-radius:15px;text-align:center;box-shadow:2px 2px 10px rgba(0,0,0,0.2)">
                <h3 style="color:white;">Total Negative Review</h3>
                <h2 style="color:white;">{total_negative_review}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("<br>", unsafe_allow_html=True)
    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.markdown(
            f"""
            <div style="background-color:#36454F;padding:20px;border-radius:15px;text-align:center;box-shadow:2px 2px 10px rgba(0,0,0,0.2)">
                <h3 style="color:white;">Positive Review Percentage</h3>
                <h2 style="color:white;">{total_positive_review_percentage}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col6:
        st.markdown(
            f"""
            <div style="background-color:#2F4F4F;padding:20px;border-radius:15px;text-align:center;box-shadow:2px 2px 10px rgba(0,0,0,0.2)">
                <h3 style="color:white;">Negative Review Percentage</h3>
                <h2 style="color:white;">{total_negative_review_percentage}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col7:
        st.markdown(
            f"""
            <div style="background-color:#4B0082;padding:20px;border-radius:15px;text-align:center;box-shadow:2px 2px 10px rgba(0,0,0,0.2)">
                <h3 style="color:white;">Average Rating</h3>
                <h2 style="color:white;">{avg_rating}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
    # with col8:
    #     st.markdown(
    #         f"""
    #         <div style="background-color:#191970;padding:20px;border-radius:15px;text-align:center;box-shadow:2px 2px 10px rgba(0,0,0,0.2)">
    #             <h3 style="color:white;">Star Count</h3>
    #             <h2 style="color:white;">{negative}</h2>
    #         </div>
    #         """,
    #         unsafe_allow_html=True
    #     )
    # Example frequency (replace with your real values from df)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## ⭐ Star Ratings Distribution")

    cols = st.columns(len(star_counts))  # one column per star

    colors = {
        5: "#06D6A0",  # Green
        4: "#118AB2",  # Blue
        3: "#FFD166",  # Yellow
        2: "#FFB703",  # Orange
        1: "#EF476F",  # Red
    }

    for i, (star, count) in enumerate(sorted(star_counts.items(), reverse=True)):
        with cols[i]:
            st.markdown(
                f"""
                <div style="background-color:{colors[star]};
                            padding:20px;
                            border-radius:15px;
                            text-align:center;
                            box-shadow:2px 2px 10px rgba(0,0,0,0.2)">
                    <h3 style="color:white;">{"⭐"*star}</h3>
                    <h2 style="color:white;">{count}</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

# ------------------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## Positive Negative Barchart")
    labels = ['Positive','Negative']
    sizes = [(pos/total_review)*100,(neg/total_review)*100]  # percentage values
    colors = ["#00753e","#ff0000"]

    # Create bar chart
    plt.figure(figsize=(5,4))
    plt.bar(labels, sizes, color=colors)

    # Add percentages on top of bars
    for i, v in enumerate(sizes):
        plt.text(i, v + 1, f"{v:.1f}%", ha='center', fontsize=12)

    plt.title("Positive and Negative Review Distribution")
    plt.ylabel("Percentage (%)")
    plt.ylim(0, 100)  # y-axis limit for percentage scale
    # plt.show()
    st.pyplot(plt)

# ------------------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## Star Count Barchart")
    labels = ['1 star','2 stars','3 stars','4 stars','5 stars']
    sizes = [(one_star/total_star)*100,(2*two_star/total_star)*100,(3*three_star/total_star)*100,(4*four_star/total_star)*100,(5*five_star/total_star)*100]  # percentage values
    # colors = ["#00753e","#ff0000"]

    # Create bar chart
    plt.figure(figsize=(7,4))
    plt.bar(labels, sizes)

    # Add percentages on top of bars
    for i, v in enumerate(sizes):
        plt.text(i, v + 1, f"{v:.1f}%", ha='center', fontsize=12)

    plt.title("Star Distribution")
    plt.ylabel("Percentage (%)")
    plt.ylim(0, 100)  # y-axis limit for percentage scale
    # plt.show()
    st.pyplot(plt)
# ------------------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## Emotion Barchart")
    df_emotion=pd.read_csv(PROCESS_DATA_FILE)
    data =[ast.literal_eval(i) for i in list(df_emotion['customer_emotions'])]
    df = pd.DataFrame(data)

    # Average percentage across all customers
    avg_emotions = df.mean().to_dict()

    labels = list(avg_emotions.keys())
    values = list(avg_emotions.values())

    plt.figure(figsize=(7,4))
    plt.bar(labels, values, color=['#4CAF50', '#2196F3', '#FF5722', '#9C27B0', '#9E9E9E'])

    for i, v in enumerate(values):
        plt.text(i, v + 1, f"{v:.1f}%", ha='center', fontsize=12)

    plt.title("Per Customer Average Emotion Distribution")
    plt.ylabel("Average Percentage (%)")
    plt.ylim(0, 100)
    # plt.show()
    st.pyplot(plt)
# -------------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## Cloud Word")
    get_all_review_list=all_review_list('page.html')
    reviews=' '
    for review in get_all_review_list:
        reviews+=review+' '

    # Sample text
    text = reviews.strip()

    # Generate word cloud
    # wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    stop_words = stopwords.words("english")
    wordcloud = WordCloud(
        width=1000,
        height=500,
        background_color="black",
        colormap="plasma",
        max_words=200,
        stopwords=stop_words
    ).generate(text)

    # Display it
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")  # Hide axes
    # plt.show()
    st.pyplot(plt)

# ---------------------------------------------------------------------------------
if selected=='Discussion':

    with open('discuss_db.json','r') as f:
        data=json.load(f)

    # --- UI ---
    st.markdown("## 💬 Discussion Overview")

    with st.expander("✅ Top Strengths", expanded=True):
        st.markdown(data["top_streangths"])

    with st.expander("⚠️ Top Weaknesses"):
        st.markdown(data["top_weaknesses"])

    with st.expander("🎉 Top Compliments"):
        st.info(data["top_compliments"])

    with st.expander("😟 Top Complaints"):
        st.error(data["top_complaints"])

    with st.expander("🛠 Actionable Recommendations"):
        st.success(data["actionable_recommendations"])

    # --- Insights Table ---
    st.markdown("### 🔍 Insights by Dish")

    df = pd.DataFrame(data["insights"]).T.reset_index()
    df.columns = ["Dish", "Positive Mentions", "Negative Mentions"]

    st.dataframe(df, use_container_width=True, height=200)


if selected=="Review":
    st.markdown("## Reviews")
    df=pd.read_csv('merged_output.csv')
    df_records = df.to_dict('records')
    
    # Sample data
    reviews = df_records

    # Custom CSS for attractive cards
    st.markdown("""
    <style>
    .review-card {
        background-color: #2f3237;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        transition: all 0.3s ease-in-out;
    }
    .review-card:hover {
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
        transform: translateY(-3px);
    }
    .review-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .reviewer-name {
        font-weight: 600;
        font-size: 18px;
    }
    .rating {
        color: #ffb400;
        font-size: 16px;
    }
    .review-text {
        margin-top: 10px;
        font-size: 20px;
        color: #ffffff;
    }
    .expander-key{
        display: flex; 
        font-size: 20px;
        color: rgb(255, 75, 75);
                }
    </style>
    """, unsafe_allow_html=True)

    st.title("🌟 Customer Reviews")

    for r in reviews:
        with st.container():
            st.markdown(f"""
            <div class="review-card">
                <div class="review-header">
                    <span class="reviewer-name">{r['name']}</span>
                    <span class="rating">{'⭐' * r['rating']}</span>
                </div>
                <small>{r['time_ago']}</small>
                <p class="review-text">{r['review']}</p>
            </div>
            """, unsafe_allow_html=True)

            # Expander for details (looks cleaner than a button)
            with st.expander("🔎 View Insights"):
                st.markdown(f"""<div class="expander-key">Keywords:</div>{r['key_themes']}""",unsafe_allow_html=True)
                st.markdown(f"""<div class="expander-key">Summary:</div>{r['summary']}""",unsafe_allow_html=True)
                st.markdown(f"""<div class="expander-key">Sentiment:</div>{r['sentiment']}""",unsafe_allow_html=True)
                st.markdown(f"""<div class="expander-key">Reply:</div>{r['reply']}""",unsafe_allow_html=True)
                st.markdown(f"""<div class="expander-key">Actionable Recommendation:</div>{r['actionable_recommendation']}""",unsafe_allow_html=True)
                st.markdown(f"""<div class="expander-key">Customer Emotion:</div>{r['customer_emotions']}""",unsafe_allow_html=True)
      


if selected=='Table':
        
    # Example CSV load (replace with your file path)
    df = pd.read_csv("merged_output.csv")

    st.markdown("## 📋 Data Table")

    # Show quick stats above the table
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", len(df))
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())

    # Add search filter
    search = st.text_input("🔍 Search in table")

    if search:
        df_filtered = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
    else:
        df_filtered = df

    # Show styled dataframe
    # st.dataframe(
    #     df_filtered.style.set_properties(**{
    #         'background-color': '#f9f9f9',
    #         'color': 'black',
    #         'border-color': 'gray'
    #     }).highlight_max(axis=0, color="#ffcccb"),
    #     use_container_width=True,
    #     height=400
    # )
    st.dataframe(
    df_filtered.style.highlight_max(
        axis=0, 
        color="#ffcccb", 
        subset=df_filtered.select_dtypes(include="number").columns
    ),
    # use_container_width=True,
    width='stretch',
    height=400
    )

    # Download button
    st.download_button(
        label="⬇️ Download CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="data_export.csv",
        mime="text/csv"
    )


st.write(f"You selected: {selected}")




