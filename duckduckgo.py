import bs4
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import os
import time
import logging
from datetime import datetime
from pathlib import Path
import socket

current_image_count = 0 # Declare current_image_count as a global variable
def get_current_ip() -> None:
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.error:
        return None
def setup_logging()-> None:
    name = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    if not os.path.exists("logs"):
        os.makedirs("logs")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(os.path.join("logs", f"{name}.log"), mode="w",)])
def create_csv(folder_name):
    with open(folder_name, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Image Count", "Image URL"])

def download_image(url: str, folder_name: str, num: int):
    # Write image to file
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(folder_name, f"{num}.jpg"), 'wb') as file:
            file.write(response.content)

def search(driver, len_containers: int, num_images: int, folder_name: str):
    global current_image_count  # Access the global variable
    original_ip = get_current_ip()
    for i in range(1, len_containers + 1):
        xPath = f"""//*[@id="zci-images"]/div[1]/div[2]/div[2]/div[{i}]"""
        driver.find_element(By.XPATH, xPath).click()
        time.sleep(0.3)
        previewImageXPath = f"""//*[@id="zci-images"]/div[1]/div[2]/div[2]/div[{i}]/div[1]/span/img"""
        page_html = driver.page_source
        previewImageElement = driver.find_element(By.XPATH, previewImageXPath)
        previewImageURL = previewImageElement.get_attribute("src")
        pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
        pageSoup.findAll('div', {'class': "tile--img__media"})

        timeStarted = time.time()
        while True:
            imageElement = driver.find_element(By.XPATH, """//*[@id="zci-images"]/div[2]/div/div[1]/div[2]/div/div[1]/div/a/img[2]""")
            imageURL = imageElement.get_attribute('src')
            if imageURL != previewImageURL:
                break
            else:
                currentTime = time.time()
                if currentTime - timeStarted > 10:
                    print("Timeout! Will download a lower resolution image and move on to the next one")
                    break

        try:
            current_ip = get_current_ip()
            if current_ip != original_ip:
                print("IP address has changed. Stopping the program.")
                driver.quit()
                return images
            download_image(imageURL, folder_name, current_image_count)
            images.append(os.path.join(folder_name, f"{current_image_count + 1}.jpg"))
            current_image_count += 1
            print(f"Downloaded element {current_image_count} out of {num_images}. URL: {imageURL}")
            logging.info(f"Downloaded element {current_image_count} out of {num_images}. URL: {imageURL}")
        except:
            print(f"Couldn't download an image {current_image_count}, continuing downloading the next one")
        if current_image_count >= num_images:
            break
        
def store_data_in_csv(file_path: str, current_image_count: int, imageURL: str):
    with open(file_path, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([current_image_count, imageURL])

def download_images(query: str, num_images: int, size_filter: str):
    global images
    global current_image_count # Access the global variable
    images = []

    output_dir = 'images'
    folder_name = Path(output_dir).joinpath(query).absolute()
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)

    driver = webdriver.Chrome()
    original_ip = get_current_ip()

    while current_image_count < num_images:
        search_URL = f"https://duckduckgo.com/?q={query}&va=n&iar=images&iax=images&ia=images&iaf=size%3A{size_filter}"
        driver.get(search_URL)
        # a = input("scroll down and press enter in terminal: ")
        current_ip = get_current_ip()
        if current_ip != original_ip:
            print("IP address has changed. Stopping the program.")
            driver.quit()
            return images
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
        containers = pageSoup.findAll('div', {'class': "tile--img__media"})
        len_containers = len(containers)
        search(driver, len_containers, num_images, folder_name)

    driver.quit()
    return images


    # setup_logging()
# folder_name = 'images'
# csv_file = os.path.join(folder_name, "image_data.csv")
# create_csv(csv_file)
# downloaded_images = download_images(query, num_images, size_filter)
# for i, imageURL in enumerate(downloaded_images, start=current_image_count):
#     store_data_in_csv(csv_file, i , imageURL)
# print(f"Downloaded {len(downloaded_images)} images.")
