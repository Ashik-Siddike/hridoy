from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
from dotenv import load_dotenv
import time
from bs4 import BeautifulSoup
import json
from datetime import datetime

load_dotenv()

def scrape_website(url):
    try:
        # Chrome অপশন সেটআপ
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--lang=en-US')
        chrome_options.add_experimental_option('prefs', {
            'intl.accept_languages': 'en,en_US',
            'translate_whitelists': {},
            'translate': {'enabled': 'false'}
        })
        chrome_options.headless = False
        
        # Chrome WebDriver সেটআপ
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # URL লোড করা
        driver.get(url)
        print(f"Opening URL: {url}")
        
        # ব্রাউজার কিছুক্ষণ খোলা রাখা
        time.sleep(10)
        
        html_content = driver.page_source
        
        # ডেটা পার্স করা
        soup = BeautifulSoup(html_content, 'html.parser')
        cleaned_content = clean_body_content(str(soup))
        
        # ডেটা ফাইলে সেভ করা
        save_data(cleaned_content, url)
        
        driver.quit()
        return html_content
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

def save_data(content, url):
    # ফাইলের নাম তৈরি (তারিখ ও সময় সহ)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scraped_data_{timestamp}.txt"
    
    # ডেটা সেভ করা
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"URL: {url}\n")
        f.write("=" * 50 + "\n")
        f.write(content)
    
    print(f"Data saved to: {filename}")

def extract_body_content(html_content):
    if not html_content:
        return ""
        
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
