import asyncio
import streamlit as st
from playwright.async_api import async_playwright

# Път до Chrome на Windows
chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

@st.cache_data(show_spinner=True)
def get_data_sync():
    # Тъй като Streamlit работи синхронно, използваме asyncio.run
    return asyncio.run(scrape_data())

async def scrape_data():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=chrome_path,
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        page = await browser.new_page()
        
        # Тук добави твоя scraping логика, пример:
        await page.goto("https://example.com")
        
        content = await page.content()
        await browser.close()
        
        # Върни някакви данни (примерно HTML или друга обработена информация)
        return content

st.title("Scraping с Playwright и Chrome")

if st.button("Изтегли данните"):
    with st.spinner("Зареждане на данни..."):
        data = get_data_sync()
        if data:
            st.success("Данните са заредени успешно.")
            st.text(data)
        else:
            st.error("Неуспешно зареждане на данни.")
