# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 21:40:00 2023

@author: Rahul
"""
import re 
import pandas as pd

def preprocess(data):
    
    pattern = "\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{1,2}\s\w{2}\s-\s"
    messages = re.split(pattern, data)[1:]
    
    dates = re.findall(pattern, data)
    df = pd.DataFrame({"user messages":messages, "message date":dates})
    
    users = []
    messages = []

    for message in df["user messages"]:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("Whatsapp notification")
            messages.append(entry[0])
                
    df['message date'] = pd.to_datetime(df["message date"], format = "%m/%d/%y, %H:%M %p - ") 
    df.rename(columns = {"message date":"date"} , inplace=True)
    
    df["user"] = users
    df["message"] = messages
    df.drop(columns=["user messages"], inplace=True)
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month_name()
    df["day"] = df["date"].dt.day
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute
    
    return df