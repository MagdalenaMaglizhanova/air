import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import asyncio
from playwright.async_api import async_playwright

st.set_page_config(page_title="Качество на въздуха – Пловдив", layout="wide")

st.title("Качество на въздуха в Пловдив (данни от ИАОС)")
st.markdown("Изтегляне в реално време на данни от [eea.government.bg/kav](https://eea.government.bg/kav/)")

@st.cache_data(show_spinner=True)
def get_data_sync():
    return asyncio.run(scrape_data())

async def scrape_data():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://eea.government.bg/kav/", timeout=60000)
        await page.wait_for_timeout(10000)

        content = await page.content()
        await browser.close()

        soup = BeautifulSoup(content, "lxml")
        tables = pd.read_html(str(soup))
        for df in tables:
            if df.astype(str).apply(lambda row: row.str.contains("Пловдив").any(), axis=1).any():
                return df
        return tables[0] if tables else None

if st.button("Изтегли данните"):
    with st.spinner("Зареждане на данни..."):
        df = get_data_sync()
        if df is not None:
            st.success("Данните са заредени успешно.")
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Свали като CSV", data=csv, file_name="plovdiv_air.csv", mime="text/csv")
        else:
            st.error("Не успяхме да заредим таблицата.")
