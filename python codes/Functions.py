# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 16:27:16 2023

@author: Rahul
"""
from urlextract import URLExtract
extractor = URLExtract()

import pandas as pd
from collections import Counter
from wordcloud import WordCloud

def fetch_stats(selected_user, df):
    
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
        
    Total_message = df.shape[0]
    
    words = []
    for i in df["message"]:
        words.extend(i.split())
        
            
    media = []
    for i in df["message"]:
        if i == "<Media omitted>\n":
            media.extend(i.split())
            
    links = []
    for message in df["message"]:
        links.extend(extractor.find_urls(message))
            
    return(Total_message, len(words), len(media), len(links))

def bar_plot(df):
    x = df["user"].value_counts().head()
    x_per = x_per = round((df["user"].value_counts().head()/df.shape[0])*100 ,2).reset_index().rename(columns={"index":"user" , "user":"percentage"})
       
    return x, x_per

def most_words_used(selected_user, df):
    
    f = open("C:\\Users\\Rahul\\Whatsapp-app-analyser\\stop_hinglish.txt", "r")
    stop_words = f.read()
    
    temp = df[df["message"] != "<Media omitted>\n"]
    temp = temp[temp["message"] != "This message was deleted\n"]
    temp = temp[temp["user"] != "Whatsapp notification"]
    
           
    words = []
    for message in temp["message"]:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
                
    
                    
    temp_data = pd.DataFrame(Counter(words).most_common(20))
    temp_data_wc = pd.DataFrame(Counter(words).most_common(temp_data.shape[0]))
    
    wc = WordCloud(width = 500, height = 500, min_font_size=5, background_color="white")
    word_cloud= wc.generate(str(temp_data_wc))

    return temp_data, word_cloud

def mon_year_msg(selected_user, df):
    df["month_num"] = df["date"].dt.month
    timeline = df.groupby(["year", "month_num", "month"]).count()["message"].reset_index()
    mon_year = []
    for i in range (timeline.shape[0]):
        mon_year.append((str(timeline["month"][i]) + "-" + str(timeline["year"][i])))
        
    return mon_year,timeline

def heat_map(selected_user, df):
    df["day_name"] = df["date"].dt.day_name()
    period = []
    for hour in df["hour"]:
        if hour == 23:
            period.append(str(hour) + "-" + "00")
        elif hour == 0:
            period.append(str("00") + "-" + str((hour) +1))
        else:
            period.append(str(hour) + "-" + str((hour) +1))
            
    df["period"] = period
    pivot_table = df.pivot_table(index = "day_name", columns = "period", values = "message", aggfunc = "count").fillna(0)
 
    return pivot_table

def activity_chart(selected_user,df):
    df["day_name"] = df["date"].dt.day_name()
    msg_day = df.groupby("day_name").count()["message"].reset_index()
    msg_month = df.groupby("month").count()["message"].reset_index()
    
    return msg_day, msg_month
    