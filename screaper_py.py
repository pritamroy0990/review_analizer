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




from bs4 import BeautifulSoup
import re
with open('page.html','r',encoding="utf-8", errors="replace") as f:
    html=f.read()
soup = BeautifulSoup(html,"html.parser")

c=soup.find_all(class_='jJc9Ad')

all_data=[]

for iteam in c:
    temp={}
    content=BeautifulSoup(str(iteam),"html.parser")
    try:
        data_review_id=content.button['data-review-id']
        print(f'data_review_id:{data_review_id}')
        temp['data_review_id']=data_review_id
    except:
        print(f'data_review_id:None')
        temp['data_review_id']=None

    try:
        name=content.find(class_='d4r55').text
        print(f'name:{name}')
        temp['name']=name
    except:
        print(f'name:None')
        temp['name']=None


    try:
        title=content.find(class_='RfnDt').text
        print(f'title:{title}')
        temp['title']=title

    except:
        print(f'title:None')
        temp['name']=None


    try:
        star=content.find(class_='kvMYJc')['aria-label']
        print(f'star:{star}')
        temp['star']=star

    except:
        print(f'star:None')
        temp['star']=None


    try:
        review=content.find(class_='wiI7pd').text
        print(f'review:{review}')
        temp['review']=review

    except:
        print(f'review:None')
        temp['review']=None


    try:
        time_ago=content.find(class_='rsqaWe').text
        print(f'time_ago:{time_ago}')
        temp['time_ago']=time_ago

    except:
        print(f'time_ago:None')
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
                print(i.text)
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

    print('-'*30)
    # break



# print(len(c))
print(all_data)

# all_review=[]
# for i in all_data:
#     if i['review']!=None:
#         all_review.append(i['review'])
# print(all_review)

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

print(all_star)
print('total:',len(c))
print(one_star+two_star+three_star+four_star+five_star)
print('avarage rating',round(((1*one_star)+(2*two_star)+(3*three_star)+(4*four_star)+(5*five_star))/len(c),2))