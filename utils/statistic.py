import pandas as pd
from bs4 import BeautifulSoup
import re
from utils.clean_data import dict_data


def total_review_num(html_file):
    with open(html_file,'r',encoding="utf-8", errors="replace") as f:
        html=f.read()
    soup = BeautifulSoup(html,"html.parser")
    reviewer=soup.find_all(class_='jJc9Ad')
    return len(reviewer)

def all_review_list(html_file):
    all_data=dict_data(html_file)

    all_review=[]
    for i in all_data:
        if i['review']!=None:
            all_review.append(i['review'])
    return all_review

def star_count(html_file):
    all_data=dict_data(html_file)

    one_star=0
    two_star=0
    three_star=0
    four_star=0
    five_star=0
    for i in all_data:
        if i['star']=='1 star':
            one_star+=1
        elif i['star']=='2 stars':
            two_star+=1
        if i['star']=='3 stars':
            three_star+=1
        if i['star']=='4 stars':
            four_star+=1
        if i['star']=='5 stars':
            five_star+=1
    all_star={
        'one_star':one_star,
        'two_star':two_star,
        'three_star':three_star,
        'four_star':four_star,
        'five_star':five_star,
    }
    return one_star,two_star,three_star,four_star,five_star,all_star

def pos_neg_num(process_data_file):
    df=pd.read_csv(process_data_file)
    sentiment=df['sentiment'].value_counts()
    try:
        pos=int(sentiment.pos)
    except:
        pos=0
    try:
        neg=int(sentiment.neg)
    except:
        neg=0
    return pos,neg

