import streamlit as st
import asyncio
from playwright.async_api import async_playwright

@st.cache_data(show_spinner=True)
def get_data_sync():
    return asyncio.run(scrape_data())

async def scrape_data():
    async with async_playwright() as p:
        # Път до Google Chrome (пример за Linux, смени ако е различно)
        chrome_path = "/usr/bin/google-chrome"

        browser = await p.chromium.launch(
            executable_path=chrome_path,
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        page = await browser.new_page()
        await page.goto("https://eea.government.bg/kav/", timeout=60000)
        await page.wait_for_timeout(10000)  # изчакване 10 секунди, ако е нужно

        # Пример: взимаме заглавието на страницата
        title = await page.title()

        await browser.close()

        import pandas as pd
        df = pd.DataFrame({"Page Title": [title]})
        return df

st.title("Пример с Playwright и Google Chrome")

if st.button("Изтегли данните"):
    with st.spinner("Зареждане на данни..."):
        df = get_data_sync()
        if df is not None:
            st.success("Данните са заредени успешно.")
            st.dataframe(df, use_container_width=True)
