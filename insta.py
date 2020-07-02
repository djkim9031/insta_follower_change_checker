#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 01:13:25 2020

@author: djkim9031
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from datetime import datetime

chrome_path = r'/usr/local/bin/chromedriver'

class InstaBot:
    def __init__(self):
        self.driver=webdriver.Chrome(executable_path=chrome_path)
        self.driver.get("https://instagram.com")
        
    def login(self,username,pw):
        
        sleep(2)
        self.username = username
        username_ = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input')
        username_.send_keys(username)
        
        self.pw = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input')
        self.pw.send_keys(pw)
        
        sleep(2)
        login = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[4]/button/div')
        login.click()
        
        popup = WebDriverWait(self.driver,20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button')))
        popup.click()
        
        popup = WebDriverWait(self.driver,20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div/div[3]/button[2]')))
        popup.click()
        
    def fetch_followers(self):
        
        profile = WebDriverWait(self.driver,20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/a/img')))
        profile.click()
        

        followers = WebDriverWait(self.driver,20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/followers')]")))
        num_ = followers.get_attribute('innerText').split()
        self.num_followers = int(num_[0])
        followers.click()      
        
        sleep(1)
        
        #find all li elements in list
        fBody  = self.driver.find_element_by_xpath("//div[@class='isgrP']")
        fList  = self.driver.find_elements_by_xpath("//div[@class='isgrP']//li")

        while len(fList)<self.num_followers: # scroll untill all followers are listed
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
            sleep(2)
            fList  = self.driver.find_elements_by_xpath("//div[@class='isgrP']//li")

            
        #fList  = self.driver.find_elements_by_xpath("//div[@class='isgrP']//li")
        #print("fList len is {}".format(len(fList)))

        prefix = '/html/body/div[4]/div/div/div[2]/ul/div/li['
        account_path = ']/div/div[1]/div[2]/div[1]/a'
        self.followers = []
        for i in range(self.num_followers):
            directory = prefix+str(i+1)+account_path
            follower = self.driver.find_element_by_xpath(directory).get_attribute('title')
            self.followers.append(follower)
            
        print(len(self.followers),self.followers)
        
    def save(self):
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        
        
        f = open("followers_on_"+day+"_"+month+"_"+year+".txt","w")
        f.write("Number of Followers = "+str(self.num_followers))
        f.write("\n")
        f.write("\n")
        for i in range(self.num_followers):
            f.write(self.followers[i])
            f.write("\n")
        f.close()
        
    def follower_change(self):
        prev_followers = [l.strip('\n\r') for i,l in enumerate(open("followers_on_02_07_2020.txt","r").readlines()) if i>1] #saved follower numbers at i=0, null at i=1
        
        print("\n")
        
        if len(self.followers) == len(prev_followers):
            print("Your follower number remains unchanged")
            print("Let's check there has been any changes to followers---")
            
            new, gone = self.calculate_change(prev_followers)
            
            print("new followers: ",new)
            print("unfollowed: ",gone)
                        
            
        elif len(self.followers) < len(prev_followers):
            print("You have lost {} followers".format((len(prev_followers)-len(self.followers))))
            print("Let's check who's come and gone---")
            
            new, gone = self.calculate_change(prev_followers)
            
            print("new followers: ",new)
            print("unfollowed: ",gone)
            
        else:
            print("You have gained {} followers".format((len(self.followers)-len(prev_followers))))
            print("Let's check who's come and gone---")
            
            new, gone = self.calculate_change(prev_followers)
            
            print("new followers: ",new)
            print("unfollowed: ",gone)
       
    def calculate_change(self,prev_followers):
        unchanged=[]
        new=[]
            
        for follower in self.followers:
            count=0
            for prev_follower in prev_followers:
                if follower == prev_follower:
                    unchanged.append(prev_follower)
                    break
                else:
                    count+=1
                if count==len(prev_followers):
                    new.append(follower)
            
        gone=[]
        for prev_follower in prev_followers:
            count=0
            for temp in unchanged:
                if prev_follower == temp:
                    break
                else:
                    count+=1
                if count==len(unchanged):
                    gone.append(prev_follower)
        return new,gone
        
            
        

        
myAccount = InstaBot()        
login = myAccount.login('Your Insta Account Username', 'Your Insta Account PW')  

print("login successful")
#print(inst.username)
myAccount.fetch_followers()
myAccount.save()
#myAccount.follower_change()


    