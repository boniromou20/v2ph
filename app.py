import os
from time import sleep
from clicknium import clicknium as cc, locator, ui
import requests
import random
from tkinter import messagebox

tab = cc.chrome.open("https://www.v2ph.com/actor/Iori-Moe")
#tab = cc.chrome.open("https://www.v2ph.com")

#messagebox.askokcancel('Confirm', 'please do Human check')
elems = tab.find_elements(locator.chrome.v2ph.moe_list)
a = 0
for elem in elems:
    url = "https://www.v2ph.com{}".format(elem.get_property("href"))\
    
    album_name = 'album/' + elem.get_text() + str(a)
    album_name = album_name.replace('0', '')
    if os.path.isdir(album_name):
        a += 1
        continue
    else:
        os.makedirs(album_name)
        a = 0
    
    new_tab = tab.browser.new_tab(url)

    has_next_page = True
    while has_next_page:
        for _ in range(20):
            new_tab.scroll(0, 2000)
            sleep(0.5)
        new_tab.wait_appear(locator.chrome.v2ph.img_moe_sublist)
        imgs = new_tab.find_elements(locator.chrome.v2ph.img_moe_sublist)
        headers = {
            'referer': 'https://www.v2ph.com/actor/Iori-Moe',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'Content-Type': 'application/json'
        }

        for img in imgs:
            url = img.get_property("src")
            # file_name = url.split("/")[-1]
            img_name = img.get_property("alt").split(" ")[-1] + '.jpg'
            img_file = requests.get(url, headers=headers)
            temp_file = os.path.join(os.getcwd(), album_name, "{}".format(img_name))
            open(temp_file, 'wb').write(img_file.content)
            print("Saving image"+ img_name +"success.")
            sleep(random.randint(1,5))
        next = new_tab.wait_appear(locator.chrome.v2ph.a_nextpage)
        if next != None:
            next.click()
        else:
            has_next_page = False
            break
    new_tab.close()
    sleep(random.randint(1,5))
new_tab.close()
