from downloader import download
from Google_with_related_search import download_images_google
from duckduckgo import download_images
import os
import logging
import csv

print("Choose an option:")
print("1. Download images using google images")
print("2. Download images using bing images")
print("3. Download images using duckduckgo")
choice = input("Enter your choice (1/2/3/4): ")


if choice == "1":
    query = input("Enter the search query: ")
    num_images = int(input("Enter the number of images to download: "))
    size_filter = input("Enter the size filter (e.g., 'large', 'medium', 'icon'): ")

    downloaded_images = download_images_google(query, num_images, size_filter)
    print(f"Downloaded {num_images} images.")


elif choice == "2":
    query=input("Enter your query:")
    limit = int(input("enter number of images required:"))
    filter = input("enter filter if required: ")
    # with open(r'C:\Users\Lenovo\OneDrive\Desktop\FWD\Web scraping\bing_image_downloader\Query.txt') as f:
    #     for line in f:
    #         query =(line.strip())
    download(query, limit=limit,filter=filter)
elif choice == "3":
    query = input("Enter the search query: ")
    num_images = int(input("Enter the number of images to download: "))
    size_filter = input("Enter the size filter (e.g., 'Large', 'Medium', 'Small', 'Wallpaper'): ")
    downloaded_images = download_images(query, num_images, size_filter)
else:
    print("Invalid choice. Please choose a valid option (1/2/3/4).")