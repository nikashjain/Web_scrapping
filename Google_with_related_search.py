import bs4
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import time
import socket
import logging
import csv

current_image_count = 0
logging.basicConfig(filename='images_info.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def get_current_ip():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.error:
        return None

def download_image(url: str, folder_name: str, num: int, num_images:int):
    # Write image to file
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(folder_name, f"{num}.jpg"), 'wb') as file:
            file.write(response.content)
        logging.info(f"Downloaded element {num} out of {num_images}. URL: {url}")

def search(driver, len_containers, num_images, folder_name):
    global current_image_count  # Access the global variable
    b = 1
    c = 51
    original_ip = get_current_ip()
    for i in range(1, len_containers + 1):
        if i == 25 or i == 50 or i == 75:
            continue
        if i == 100:
            xPath = f"""//*[@id="islrg"]/div[1]/div[51]/div[{100}]"""
            driver.find_element(By.XPATH, xPath).click()
            break
        if b % 25 == 0:
            b += 1
        if i <= 49:
            xPath = f"""//*[@id="islrg"]/div[1]/div[{i}]"""
        elif i > 49 and i <= 99:
            xPath = f"""//*[@id="islrg"]/div[1]/div[51]/div[{b}]"""
        driver.find_element(By.XPATH, xPath).click()
        time.sleep(0.3)
        if i <= 49:
            previewImageXPath = f"""//*[@id="islrg"]/div[1]/div[{i}]/a[1]/div[1]/img"""
        elif i > 49 and i <= 99:
            previewImageXPath = f"""//*[@id="islrg"]/div[1]/div[51]/div[{b}]/a[1]/div[1]/img"""
        page_html = driver.page_source
        previewImageElement = driver.find_element(By.XPATH, previewImageXPath)
        previewImageURL = previewImageElement.get_attribute("src")
        pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
        pageSoup.findAll('div', {'class': "isv-r PNCib ViTmJb BUooTd"})

        timeStarted = time.time()
        while True:
            imageElement = driver.find_element(By.XPATH, """//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img""")
            imageURL = imageElement.get_attribute('src')
            if imageURL != previewImageURL:
                break
            else:
                currentTime = time.time()
                if currentTime - timeStarted > 4:
                    print("Timeout! Will download a lower resolution image and move on to the next one")
                    break

        try:
            current_ip = get_current_ip()
            if current_ip != original_ip:
                print("IP address has changed. Stopping the program.")
                driver.quit()
                return images
            current_image_count += 1  # Increment the global current_image_count
            download_image(imageURL, folder_name, current_image_count,num_images)
            images.append(os.path.join(folder_name, f"{current_image_count + 1}.jpg"))
            print(f"Downloaded element {current_image_count} out of {num_images}. URL: {imageURL}")
            log_image_data(imageURL, folder_name)
        except:
            print(f"Downloaded element {current_image_count} out of {num_images}. URL: {imageURL}")
            log_image_data(imageURL, folder_name)
            # print(f"Couldn't download an image {current_image_count}, continuing downloading the next one")

        if i >= 50:
            b += 1
        elif i >= 100:
            c += 1
        if current_image_count >= num_images:
            break
def write_csv(imageURL: dict, download_count: int) -> None:
    """
    Writes a dictionary of data to a CSV file.
    """
    with open("image_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([download_count, imageURL])
        for row in writer:
            print(row)
def log_image_data(imageURL, folder_name):
    """
    Logs image data to the CSV file.
    """
    csv_file = os.path.join(folder_name, "image_data.csv")
    with open(csv_file, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([current_image_count, imageURL])

def download_images_google(query: str, num_images: int, size_filter: str):
    global images
    global current_image_count  # Access the global variable
    images = []
    page = 1

    folder_name = 'images'
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)

    driver = webdriver.Chrome()

    while current_image_count < num_images:
        search_URL = f"https://www.google.com/search?q={query}&tbm=isch&tbs=isz:{size_filter}&start={page * 200}"
        driver.get(search_URL)
        a = input("scroll down and press enter in terminal: ")
        while True:
            current_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == current_height:
                break

        # Scrolling all the way up
        driver.execute_script("window.scrollTo(0, 0);")
        page_html = driver.page_source
        pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
        containers = pageSoup.findAll('div', {'class': "isv-r PNCib ViTmJb BUooTd"})
        len_containers = len(containers)
        search(driver, len_containers, num_images, folder_name)
        while current_image_count < num_images - 1:
            print(current_image_count)
            search(driver, len_containers, num_images, folder_name)

    driver.quit()
    return images