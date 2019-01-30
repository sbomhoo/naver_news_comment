# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup 
import requests 
import re 
import pandas as pd
'''
댓글 크롤링(JSON 활용)
네트워크 F5
'''
# 네이버 뉴스 url을 입력합니다.
url="https://news.naver.com/main/ranking/read.nhn?mid=etc&sid1=111&rankingType=popular_day&oid=018&aid=0004300484&date=20190128&type=1&rankingSeq=5&rankingSectionId=101"    #이부분만 원하는 기사로 수정!
RESULT_PATH = 'C:/Users/User/Desktop/python study/beautifulSoup_ws/crawling_result/'
    
oid=url.split("oid=")[1].split("&")[0] 
aid=url.split("aid=")[1] 

c_List=[] 
d_List=[]

# 여러 리스트들을 하나의 리스트로 만들어줌 
def contents_flat(c_List,d_List): 
    flatList = [] 
    d_flatList=[]
    #f = open("C:/Users/User/Desktop/python study/beautifulSoup_ws/crawling_result/comment_text.txt", 'w', encoding='utf-8')
    for elem in c_List: 
        # if an element of a list is a list 
        # iterate over this list and add elements to flatList  
        
        #elem=re.sub('"',' ',str(elem))
        if type(elem) == list: 
            for e in elem: 
                flatList.append(e) 
        else: 
            flatList.append(elem) 
           
    for elem in d_List: 
        if type(elem) == list: 
            for e in elem: 
                e=re.sub('\\+0900',' ',e)
                d_flatList.append(e) 
        else: 
            elem=re.sub('\\+0900',' ',elem)
            d_flatList.append(elem) 

    #f.write(str(flatList))
    excel_make(flatList,d_flatList)
       
        
def excel_make(flatList,d_flatList): 
    result= {"comments":flatList, "date":d_flatList}
    df = pd.DataFrame(result)  #df로 변환
    df.to_excel(RESULT_PATH+"comments_results.xlsx",sheet_name='sheet1')



def main():
    page=1    
    header = { 
        "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36", 
        "referer":url, 
         
    }
    while True : 
        #json api url
        c_url="https://apis.naver.com/commentBox/cbox/web_neo_list_jsonp.json?ticket=news&templateId=default_society&pool=cbox5&_callback=jQuery1707138182064460843_1523512042464&lang=ko&country=&objectId=news"+oid+"%2C"+aid+"&categoryId=&pageSize=20&indexSize=10&groupId=&listType=OBJECT&pageType=more&page="+str(page)+"&refresh=false&sort=FAVORITE"  
        # 파싱하는 단계입니다.
        r=requests.get(c_url,headers=header) 
        cont=BeautifulSoup(r.content,"html.parser")     
        total_comm=str(cont).split('comment":')[1].split(",")[0] 
        
        match=re.findall('"contents":"([^\*]*)","userIdNo"', str(cont))   #소괄호 안에 있는것을 크롤링해온다.
        date=re.findall('"modTime":"([^\*]*)","modTimeGmt"', str(cont)) 
        
    
        #print(type(match))
             
        # 댓글을 리스트에 중첩합니다.
        c_List.append(match)
        d_List.append(date)
        
        # 한번에 댓글이 20개씩 보이기 때문에 한 페이지씩 몽땅 댓글을 긁어 옵니다.
        if int(total_comm) <= ((page) * 20): 
            break 
        else :  
            page+=1
            
    contents_flat(c_List,d_List)   

    
main()


