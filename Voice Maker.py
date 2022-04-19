# coding: utf-8
from Detail import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
import re

download_path = Download_path
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option("prefs",{"download.default_directory" : download_path})



driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()),options=options)
driver.implicitly_wait(5)
driver.maximize_window()
driver.get("https://voicemaker.in/")

old_files = len([i for i in os.listdir(download_path) if i.endswith(".mp3")])

def LogIn():
    try:
        login_page = driver.find_element(By.XPATH, '//*[@id="registerModal"]/div/div/div/div/div[2]')
        if login_page.is_displayed():
            driver.find_element(By.XPATH,'//*[@id="registerModal"]/div/div/div/div/div[2]/div/div[2]/p/a').click()
        if driver.find_element(By.XPATH,'//*[@id="loginModal"]/div/div/div').is_displayed():
            email = driver.find_element(By.ID, "loginEmail")
            email.clear()
            email.send_keys(Email)
            password = driver.find_element(By.ID,"loginPassword")
            password.clear()
            password.send_keys(Password)
            if driver.find_element(By.ID,"basic_checkbox_1").is_selected():
                driver.find_element(By.ID,"basic_checkbox_1").click()
            driver.find_element(By.ID, "btnLogin").click()
    except:
        pass
        #print("Either Page not avalible or invalid Id,Password")

        

def download_one(Text):
    wait = WebDriverWait(driver,5)
    text_field = driver.find_element(By.ID, "main-textarea")
    text_field.clear()
    text_field.send_keys(Text)

    neural_tts = driver.find_element(By.ID,"neural")
    if not neural_tts.is_selected():
        neural_tts.click()

    voice = wait.until(EC.presence_of_element_located((By.ID, "ai1-Joanna")))
    if not voice.is_selected():
        voice.click()

    convert = driver.find_element(By.XPATH, '//*[@id="buttons-box"]/button[1]')
    convert.click()

    c = wait.until(EC.element_to_be_clickable(convert))
    c = wait.until(EC.element_to_be_clickable(convert))
    
    try:
        LogIn()
    except:
        pass
    try:
        driver.find_element(By.ID,"download-format").click()
    except:
        time.sleep(5)
        download_one(Text)


# spliting the text to proper format
def format_download_all(Text):
    rx = r"\s*\.\s*"
    Text = re.sub(rx, ". ", Text).rstrip()
    Text.rstrip()
    Last_index = len(Text)-1
    i = 0
    count = 0
    if Last_index >= 250:
        dot_idx = Text[:250].rindex(". ")
    else:
        dot_idx = Last_index
    while True:
        sub_text = Text[i:i+dot_idx+1]
        download_one(sub_text)
        print("File downloading")
        count+=1
        i = i+dot_idx+2

        try:
            temp = Text[i:i+(250 if Last_index>i+250 else Last_index)]
            if temp == "":
                break
            dot_idx = temp.rindex(". ")
        except ValueError:
            dot_idx = Text[i:i+(250 if Last_index>i+250 else Last_index)].rindex(".")
        except:
            break
    return count


# Merge file
def merge_file():
    files = [i for i in os.listdir(download_path) if not i.startswith("VM_")]
    files.sort()
    file_name = "VM_"+time.strftime("%y%m%d%H%M%S", time.localtime())
    with open(os.path.join(download_path,file_name)+".mp3","wb") as output:
        for i in files:
            with open(os.path.join(download_path,i),"rb") as read_file:
                output.write(read_file.read())
            with open(os.path.join(download_path,"VM_Space.mp3"),"rb") as space:
                output.write(space.read())
            os.remove(os.path.join(download_path,i))
        with open(os.path.join(download_path,"VM_Space.mp3"),"rb") as space:
                output.write(space.read())


if __name__ == "__main__":
    number_of_files = format_download_all(Text)
    while len([i for i in os.listdir(download_path) if i.endswith(".mp3")]) != number_of_files + old_files:
        continue                                                                                        # Wait for download
    print("All Files downloaded.\nMerginng...")
    time.sleep(2)
    merge_file()
    print("Done")

