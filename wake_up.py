import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wake_streamlit():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    url = "https://sense-ai.streamlit.app/" 
    
    try:
        print(f"Visiting {url}...")
        driver.get(url)
        
        # Wait up to 15 seconds to see if the "Wake Up" button appears
        # Streamlit's button usually contains the text "Yes, get this app back up!"
        wait = WebDriverWait(driver, 15)
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Yes, get this app back up')]")))
        
        button.click()
        print("App was asleep. Clicked the Wake Up button!")
        
    except Exception as e:
        print("App is already awake or button not found. All good!")
    finally:
        driver.quit()

if __name__ == "__main__":
    wake_streamlit()