import streamlit as st
import pandas as pd

def main():
    st.title("我的第一個Streamlit App")
    st.write("歡迎來到我的應用程式！")
    
    # Load the CSV file
    df = pd.read_csv("taiwan.csv")
    
    # Display the DataFrame
    st.write("以下是 'taiwan.csv' 的內容：")
    st.dataframe(df)

if __name__ == "__main__":
    main()
