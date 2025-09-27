import builtins

def custom_print(*args, **kwargs):
    # Use the original print for console output
    builtins.print(*args, **kwargs)
    
    # Convert arguments to string (like print does)
    text = " ".join(str(arg) for arg in args)
    
    # Append to file
    with open("output.log", "a", encoding="utf-8") as f:
        f.write(text + "\n")

# Replace built-in print with custom version
print = custom_print



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
import json

url='''https://www.google.com/maps/place/Pancake's+Rangpur/@25.7596478,89.2313226,15.37z/data=!4m18!1m9!3m8!1s0x39e331a88dec61d9:0x89ca82231e9e0dd7!2sSignature+Cuisine!8m2!3d25.7570142!4d89.2386145!9m1!1b1!16s%2Fg%2F11rv9tbk3m!3m7!1s0x39e333006e8d331f:0xe4c87b4b213cc6f2!8m2!3d25.7491644!4d89.2333836!9m1!1b1!16s%2Fg%2F11w4p8dmy8?hl=en&entry=ttu&g_ep=EgoyMDI1MDkyMi4wIKXMDSoASAFQAw%3D%3D'''

save_html_file(url)
print("Google Review page downloaded..")


nltk.download("stopwords")
from nltk.corpus import stopwords


HTML_FILE='page.html'
RAW_DATA_FILE='raw_data.csv'
PROCESS_DATA_FILE='process_data.csv'

data=dict_data(HTML_FILE)
save_csv(data=data,file_name=RAW_DATA_FILE)
df=pd.read_csv(RAW_DATA_FILE)
df['time_stamp']=df['time_ago'].apply(relative_to_date)
df['rating']=df['star'].apply(generate_rating)
df.to_csv(RAW_DATA_FILE)
print("Screaped Data saved in csv")


print("This step will take huge time for analyzing review by AI")
# for process data
list_result=[]
for d in data:

    review_text=d['review']
    reviewer_name=d['name']
    customer_rating=d['star']
    try:
        aspect_rating=d['aspect_rating']
    except:
        aspect_rating=None

    result=dict(sentiment(review_text=review_text,reviewer_name=reviewer_name,customer_rating=customer_rating,aspect_rating=aspect_rating))
    list_result.append(result)

save_csv(data=list_result,file_name=PROCESS_DATA_FILE)
print("Successfully Analyzed and saved information..")







# statistic
total_review=total_review_num(HTML_FILE)
# print('Total Review:',total_review)

one_star,two_star,three_star,four_star,five_star,all_star=star_count(HTML_FILE)
total_star=(1*one_star)+(2*two_star)+(3*three_star)+(4*four_star)+(5*five_star)
# print('Total Star:',total_star)
# print('Star Count:',all_star)
# print('avarage rating',round(total_star/total_review,2))


pos,neg=pos_neg_num(PROCESS_DATA_FILE)
# print('Total Positive Review:',pos)
# print('Total Negative Review:',neg)

# print('Positive Review Percentage:',(pos/total_review)*100)
# print('Negative Review Percentage:',(neg/total_review)*100)




# get_all_review_list=all_review_list('page.html')
# reviews=' '
# for review in get_all_review_list:
#     reviews+=review+' '

# # Sample text
# text = reviews.strip()

# # Generate word cloud
# # wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
# stop_words = stopwords.words("english")
# wordcloud = WordCloud(
#     width=1000,
#     height=500,
#     background_color="black",
#     colormap="plasma",
#     max_words=200,
#     stopwords=stop_words
# ).generate(text)

# # Display it
# plt.figure(figsize=(10, 5))
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")  # Hide axes
# plt.show()


# # ----------------------------------------------------------------------
# # Data
# labels = ['Positive','Negative']
# sizes = [(pos/total_review)*100,(neg/total_review)*100]  # percentage values
# colors = ["#00753e","#ff0000"]

# # Create bar chart
# plt.figure(figsize=(6,6))
# plt.bar(labels, sizes, color=colors)

# # Add percentages on top of bars
# for i, v in enumerate(sizes):
#     plt.text(i, v + 1, f"{v:.1f}%", ha='center', fontsize=12)

# plt.title("Positive and Negative Review Distribution")
# plt.ylabel("Percentage (%)")
# plt.ylim(0, 100)  # y-axis limit for percentage scale
# plt.show()

# # ----------------------------------------------------------------
# labels = ['1 star','2 stars','3 stars','4 stars','5 stars']
# sizes = [(one_star/total_star)*100,(2*two_star/total_star)*100,(3*three_star/total_star)*100,(4*four_star/total_star)*100,(5*five_star/total_star)*100]  # percentage values
# # colors = ["#00753e","#ff0000"]

# # Create bar chart
# plt.figure(figsize=(6,6))
# plt.bar(labels, sizes)

# # Add percentages on top of bars
# for i, v in enumerate(sizes):
#     plt.text(i, v + 1, f"{v:.1f}%", ha='center', fontsize=12)

# plt.title("Positive and Negative Review Distribution")
# plt.ylabel("Percentage (%)")
# plt.ylim(0, 100)  # y-axis limit for percentage scale
# plt.show()

# # -----------------------------------

# df_emotion=pd.read_csv(PROCESS_DATA_FILE)

# # Example dataframe
# data =[ast.literal_eval(i) for i in list(df_emotion['customer_emotions'])]
# df = pd.DataFrame(data)

# # Average percentage across all customers
# avg_emotions = df.mean().to_dict()

# labels = list(avg_emotions.keys())
# values = list(avg_emotions.values())

# plt.figure(figsize=(7,5))
# plt.bar(labels, values, color=['#4CAF50', '#2196F3', '#FF5722', '#9C27B0', '#9E9E9E'])

# for i, v in enumerate(values):
#     plt.text(i, v + 1, f"{v:.1f}%", ha='center', fontsize=10)

# plt.title("Average Customer Emotion Distribution")
# plt.ylabel("Average Percentage (%)")
# plt.ylim(0, 100)
# plt.show()

# ------------------------------------------------------------

print("plz wait, LLM analysis and extracting important information..")
discuss_obj={}

top_streangths=top_streangth(r'F:\projects\review_analyzer\ra_offline\page.html')
print(top_streangths)
discuss_obj['top_streangths']=top_streangths

top_weaknesses=top_weakness(r'F:\projects\review_analyzer\ra_offline\page.html')
print(top_weaknesses)
discuss_obj['top_weaknesses']=top_weaknesses


top_compliments=top_compliment(r'F:\projects\review_analyzer\ra_offline\page.html')
print(top_compliments)
discuss_obj['top_compliments']=top_compliments


top_complaints=top_complaint(r'F:\projects\review_analyzer\ra_offline\page.html')
print(top_complaints)
discuss_obj['top_complaints']=top_complaints


actionable_recommendations=actionable_recommendation(r'F:\projects\review_analyzer\ra_offline\page.html')
print(actionable_recommendations)
discuss_obj['actionable_recommendations']=str(actionable_recommendations)


insights = manu_item_insight(r"F:\projects\review_analyzer\ra_offline\page.html")
print(insights)
discuss_obj['insights']=insights


with open('discuss_db.json','w') as f:
    json.dump(discuss_obj,f)

# ------------------------------------------------------------------


df1 = pd.read_csv('raw_data.csv')
df2 = pd.read_csv('process_data.csv')
df2['data_review_id']=df1['data_review_id']
df3=df1.merge(df2,how='inner',on='data_review_id')
try:
    df3 = df3.drop(['Unnamed: 0.1', 'Unnamed: 0'], axis=1)
except:
    print('unnamed column not removed.')
df3.to_csv('merged_output.csv')

print('Analysing successfully completed and information saved.')
