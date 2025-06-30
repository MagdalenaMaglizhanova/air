import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

def scrape_data():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get("https://eea.government.bg/kav/")
    time.sleep(10)  # По-добре с WebDriverWait

    # Тук трябва да добавиш код за кликване върху справки, избор на град, станция и параметри

    tables = pd.read_html(driver.page_source)
    driver.quit()

    return tables[0] if tables else None

st.title("Качество на въздуха в Пловдив")

if st.button("Изтегли данни"):
    df = scrape_data()
    if df is not None:
        st.dataframe(df)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Свали като CSV", csv, "plovdiv_air.csv", "text/csv")
    else:
        st.error("Не успях да заредя данните.")
