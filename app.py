# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 21:39:16 2023

@author: Rahul
"""

import streamlit as st
import preprocessor, Functions




st.sidebar.title("Whatsapp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf - 8")
    
    
    df = preprocessor.preprocess(data)
    #st.dataframe(df)
    
    user_list = df["user"].unique().tolist()
    
    user_list.remove("Whatsapp notification")
    user_list.sort()
    user_list.insert(0, "Overall")
    
    
 
    
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
        
    if st.sidebar.button("Show analysis"): 
        Total_message, words, media, links = Functions.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1,col2,col3,col4 = st.columns(4)
         
        with col1:
            st.header("Total messages")
            st.title(Total_message) 
            
        with col2:
            st.header("Total words")
            st.title(words)
    
        with col3:
            st.header("Media shared")
            st.title(media)
            
        with col4:
            st.header("Links shared")
            st.title(links)
            
        import matplotlib.pyplot as plt
        if selected_user == "Overall":
            
            x, x_per = Functions.bar_plot(df)
            
            
            fig, ax = plt.subplots()
                
            col1, col2 = st.columns(2)
                
            with col1:
                st.title("Top 5 busy users")    
                ax.bar(x.index, x.values, color="orange")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
                
               
            with col2:
                st.title("Percentage of busy users")
                st.dataframe(x_per)
            
           
              
            temp_data, word_cloud = Functions.most_words_used(selected_user, df)
            st.title("Word Cloud")
            fig, ax =plt.subplots()
            ax.imshow(word_cloud)
            st.pyplot(fig)
            
            st.title("Most used top 20 words")
            fig,ax = plt.subplots()
            ax.barh(temp_data[0], temp_data[1])
            plt.xticks(rotation = "vertical")
            st.pyplot(fig)
            
            mon_year,timeline = Functions.mon_year_msg(selected_user, df)
            st.title("Monthly Timeline")
            fig, ax =plt.subplots()
            ax.plot(mon_year, timeline["message"])
            plt.xticks(rotation = "vertical")
            st.pyplot(fig)
            
            msg_day, msg_month = Functions.activity_chart(selected_user, df)
            st.title("Activity Graph")
            col1, col2 = st.columns(2)
            
            with col1:
                st.header("Most busy day")
                fig, ax =plt.subplots()
                ax.bar(msg_day["day_name"], msg_day["message"], color="green")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.header("Most busy month")
                fig, ax =plt.subplots()
                ax.bar(msg_month["month"], msg_month["message"], color="yellow")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            
            import seaborn as sns
            pivot_table = Functions.heat_map(selected_user, df)
            st.title("Hour-wise weekly activity map")
            plt.figure(figsize = (16,8))
            fig, ax = plt.subplots()
            ax =sns.heatmap(pivot_table)
            st.pyplot(fig)
            
           
            
            
           
            
            
                
               
            
        
            
        
    
   
    
 
                 
            