
from bs4 import BeautifulSoup
import re
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta



def dict_data(html_file:Path):
    with open(html_file,'r',encoding="utf-8", errors="replace") as f:
        html=f.read()
    soup = BeautifulSoup(html,"html.parser")

    c=soup.find_all(class_='jJc9Ad')

    all_data=[]

    for iteam in c:
        temp={}
        content=BeautifulSoup(str(iteam),"html.parser")
        try:
            data_review_id=content.button['data-review-id']
            # print(f'data_review_id:{data_review_id}')
            temp['data_review_id']=data_review_id
        except:
            # print(f'data_review_id:None')
            temp['data_review_id']=None

        try:
            name=content.find(class_='d4r55').text
            # print(f'name:{name}')
            temp['name']=name
        except:
            # print(f'name:None')
            temp['name']=None


        try:
            title=content.find(class_='RfnDt').text
            # print(f'title:{title}')
            temp['title']=title

        except:
            # print(f'title:None')
            temp['name']=None


        try:
            star=content.find(class_='kvMYJc')['aria-label']
            # print(f'star:{star}')
            temp['star']=star

        except:
            # print(f'star:None')
            temp['star']=None


        try:
            review=content.find(class_='wiI7pd').text
            # print(f'review:{review}')
            temp['review']=review

        except:
            # print(f'review:None')
            temp['review']=None


        try:
            time_ago=content.find(class_='rsqaWe').text
            # print(f'time_ago:{time_ago}')
            temp['time_ago']=time_ago

        except:
            # print(f'time_ago:None')
            temp['time_ago']=time_ago


            
        try:
            MyEned=content.find(class_='MyEned').text
            jslog=content.find(class_='MyEned').div['jslog']
            end=content.find(jslog=jslog).find_all('span')
            end_=[]
            extra_attribute=''
            for index,i in enumerate(end):
                i=BeautifulSoup(str(i),'html.parser')
                if i.find(class_='RfDO5c'):
                    end_.append(i.text)
                    # print(i.text)
                    extra_attribute=extra_attribute+' '+i.text
            temp['extra_attribute']=extra_attribute.strip()
            text = temp['extra_attribute']

            # Regex pattern for Food, Service, Atmosphere (number after colon)
            pattern = r"(Food|Service|Atmosphere):\s*(\d+)"

            matches = re.findall(pattern, text)
            temp['aspect_rating']={key: int(value) for key, value in matches}

        except:
            pass

        all_data.append(temp)
    return all_data

def save_csv(data:list[dict],file_name):

    df = pd.DataFrame(data)
    df.to_csv(file_name, index=False, encoding="utf-8")

    print("CSV file created successfully!")


def relative_to_date(relative_time: str) -> datetime:
    relative_time = relative_time.lower()
    now = datetime.now()
    
    # Regex extract number and unit
    match = re.match(r"(\d+)\s+(\w+)", relative_time)
    if not match:
        return now  # default: today
    
    value, unit = int(match.group(1)), match.group(2)
    
    if "day" in unit:
        if value=='a':
            value=1
            return now - timedelta(days=value)
        return now - timedelta(days=value)
    elif "week" in unit:
        if value=='a':
            value=1
            return now - timedelta(weeks=value)
        return now - timedelta(weeks=value)
    elif "month" in unit:
        if value=='a':
            value=1
            return now - timedelta(days=30 * value)
        return now - timedelta(days=30 * value)  # approx
    elif "year" in unit:
        if value=='a':
            value=1
            return now - timedelta(days=365 * value)
        return now - timedelta(days=365 * value)  # approx
    else:
        return now


def generate_rating(text):
    match = re.search(r"(\d+)\s*stars?", text, re.IGNORECASE)
    if match:
        rating = int(match.group(1))
        return rating
