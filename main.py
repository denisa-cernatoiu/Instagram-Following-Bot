from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv
import time

load_dotenv()

class InstaFollower:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        login_url = "https://www.instagram.com/accounts/login/"
        self.driver.get(login_url)
        
        # handling cookie pop-up 1
        self._handleFirstCookiePopup()
        
        #handle username and Passoword input
        self._handleUsernameAndPasswordInput()

        # handling save info pop-up
        self._handleSaveInfoPopup()
        
        # handling cookie pop-up 2
        self._handleSecondCookiePopup()
        
        

    
    def find_followers(self):
        account_url = f"https://www.instagram.com/{os.getenv("SIMILAR_ACCOUNT")}"
        self.driver.get(account_url)

        followers_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/followers/') and contains(., 'followers')]"))
        )

        # scrollind down a bit
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", followers_link)
        time.sleep(0.5)

        # opening the followers list
        self.driver.execute_script("arguments[0].click();", followers_link)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Followers')]"))
        )

    
    def follow(self):
        while True:
            follow_buttons = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, "//button[normalize-space()='Follow']"))
            )

            if not follow_buttons:
                print("Followers list completed.")
                break

            for btn in follow_buttons:
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
                    time.sleep(0.5)
                    self.driver.execute_script("arguments[0].click();", btn)
                    time.sleep(1.37)

                except Exception as e:
                    print("Error:", e)
                    continue
    
    def _handleFirstCookiePopup(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h2[contains(text(),'Allow the use of cookies')]")))

            cookie_pop_up = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Decline optional cookies')]")
            cookie_pop_up.click()

        except Exception as e:
            print("Error:", e)

    def _handleUsernameAndPasswordInput(self):
        fill_username = self.driver.find_element(By.XPATH, value='//*[@id="loginForm"]/div[1]/div[1]/div/label/input')
        fill_username.clear()
        fill_username.send_keys(os.getenv("INSTA_USERNAME"), Keys.ENTER)

        fill_password = self.driver.find_element(By.XPATH, value='//*[@id="loginForm"]/div[1]/div[2]/div/label/input')
        fill_password.clear()
        fill_password.send_keys(os.getenv("PASSWORD"), Keys.ENTER)
                
    def _handleSaveInfoPopup(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Save your login info')]")))

           
            not_now_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and text()='Not now']"))
                )

            not_now_button.click()

        
        except Exception as e:
            print("Error:", e)

    def _handleSecondCookiePopup(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Allow the use of cookies')]")))

            cookie_pop_up =  WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and text()='Decline optional cookies']"))
            )
            cookie_pop_up.click()

        except Exception as e:
            print("Error:", e)

insta_bot = InstaFollower()
insta_bot.login()
insta_bot.find_followers()
insta_bot.follow()
