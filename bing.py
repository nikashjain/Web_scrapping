import posixpath
import re
import time
import urllib
import urllib.request
from pathlib import Path
from selenium import webdriver
import logging
import csv
import sys
import os
from datetime import datetime
import socket
import time
# import filetype


class Bing:
    def __init__(self, query: str, limit: int, output_dir: str, adult: bool, timeout: int, filter='', verbose=True):
        self.download_count = 0
        self.setup_logging()
        self.csv_file = os.path.join(output_dir, "image_data.csv")
        self.query = query
        self.output_dir = output_dir
        self.adult = adult
        self.filter = filter
        self.verbose = verbose
        self.seen = set()

        assert type(limit) == int, "limit must be an integer"
        self.limit = limit
        assert type(timeout) == int, "timeout must be an integer"
        self.timeout = timeout
        
        # logging.basicConfig(filename='download_log.txt', level=logging.INFO)

        self.page_counter = 0
        self.driver = webdriver.Chrome() # Initialize Chrome WebDriver
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
      'AppleWebKit/537.11 (KHTML, like Gecko) '
      'Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}
    def get_current_ip(self):
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        except socket.error:
            return None

    def setup_logging(self):
        name = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        if not os.path.exists("logs"):
            os.makedirs("logs")
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(os.path.join("logs", f"{name}.log"), mode="w",)])
                    #   logging.FileHandler(self.csv_file, mode="w", newline=""),
            # logging.StreamHandler(sys.stdout),  # Send logs to the console
    def write_csv(self, link: dict, download_count: int) -> None:
        """
        Writes a dictionary of data to a CSV file.
        """
        with open("image_data.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([download_count, link])
            for row in writer:
                print(row)

    def get_filter(self, shorthand: str) -> str:
            """
            # Apply filters
            """
            if shorthand == "line" or shorthand == "linedrawing":
                return "+filterui:photo-linedrawing"
            elif shorthand == "photo":
                return "+filterui:photo-photo"
            elif shorthand == "clipart":
                return "+filterui:photo-clipart"
            elif shorthand == "gif" or shorthand == "animatedgif":
                return "+filterui:photo-animatedgif"
            elif shorthand == "transparent":
                return "+filterui:photo-transparent"
            elif shorthand == "Large" or "large":
                return "+filterui:imagesize-large"
            elif shorthand == "Short" or "short":
                return "+filterui:imagesize-short"
            elif shorthand == "Medium" or "medium":
                return "+filterui:imagesize-medium"
            else:
                return ""
    def save_image(self, link: str, file_path: str):
        """
        saves/writes it in the file path.
        """
        request = urllib.request.Request(link, None, self.headers)
        image = urllib.request.urlopen(request, timeout=self.timeout).read()
        with open(str(file_path), 'wb') as f:
            f.write(image)
    def download_image(self, link:str):
        """
        Checks if the file is in image format and then saves it in the folder.
        """
        self.download_count += 1
        # Get the image link
        try:
            path = urllib.parse.urlsplit(link).path
            filename = posixpath.basename(path).split('?')[0]
            file_type = filename.split(".")[-1]
            if file_type.lower() not in ["jpe", "jpeg", "jfif", "exif", "tiff", "gif", "bmp", "png", "webp", "jpg","dwg","xcf", "apng","cr2","jxr","psd","ico","heic","avif"]:
                # file_type = "jpg"
                return
                
            if self.verbose:
                # Download the image
                print("[%] Downloading Image #{} from {}".format(self.download_count, link))
                
            self.save_image(link, self.output_dir.joinpath("Image_{}.{}".format(
                str(self.download_count), file_type)))
            if self.verbose:
                logging.info("[%] Downloaded Image #{} from {}".format(self.download_count, link))
                print("[%] File Downloaded !\n")
                

        except Exception as e:
            self.download_count -= 1
            print("[!] Issue getting: {}\n[!] Error:: {}".format(link, e))
    def log_image_data(self, link):
        """
        Logs image data to the CSV file.
        """
        with open(self.csv_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.download_count, link])
    def run(self):
        """
        constructs url, opens chrome and obtans html data to identify image links.
        """
        original_ip = self.get_current_ip()
        while self.download_count < self.limit and self.page_counter <=550:
            if self.verbose:
                print('\n\n[!!] Indexing page: {}\n'.format(self.page_counter + 1))

            # Construct the URL
            request_url = 'https://www.bing.com/images/search?q=' + urllib.parse.quote_plus(self.query) \
                          + '&first=' + str(self.page_counter) + '&count=' + str(self.limit) \
                          + '&adlt=' + self.adult + '&qft=' + ('' if self.filter is None else self.get_filter(self.filter))

            self.driver.get(request_url)  # Navigate to the URL
            while True:
                current_height = self.driver.execute_script("return document.body.scrollHeight")
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == current_height:
                    break

            # Wait for the page to load
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, 0);")
            # a= input("scroll and press enter: ")
            # Get the page source HTML
            html = self.driver.page_source

            if html.strip() == "":
                print("[%] No more images are available")
                break

            links = re.findall('murl&quot;:&quot;(.*?)&quot;', html)

            if self.verbose:
                print("[%] Indexed {} Images on Page {}.".format(len(links), self.page_counter + 1))
                print("\n===============================================\n")

            for i in range(1, len(links)):
                link = links[i]
                if self.download_count < self.limit + 1 and link not in self.seen:
                    self.seen.add(link)
                    self.download_image(link)
                    self.log_image_data(link)
            current_ip = self.get_current_ip()
            if current_ip != original_ip:
                print("IP address has changed. Stopping the program.")
                break

            self.page_counter += 1

        print("\n\n[%] Done. Downloaded {} images.".format(self.download_count))
        print()
        self.driver.quit()  # Close the WebDriver when done

