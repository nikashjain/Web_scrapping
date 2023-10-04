from bing_image_downloader.downloader import download
from Google_with_related_search import download_images
if __name__ == "__main__":
    query = input("Enter the search query: ")
    num_images = int(input("Enter the number of images to download: "))
    size_filter = input("Enter the size filter (e.g., 'large', 'medium', 'icon'): ")

    downloaded_images = download_images(query, num_images, size_filter)
    print(f"Downloaded {len(downloaded_images)} images.")


if __name__=="__main__":
    # query=input("Enter your query:")
    limit = int(input("enter number of images required:"))
    filter = input("enter filter if required: ")
    with open(r'C:\Users\Lenovo\OneDrive\Desktop\FWD\Web scraping\bing_image_downloader\Query.txt') as f:
        for line in f:
            query =(line.strip())
            download(query, limit=limit,filter=filter)
    
        # def image_link_csv()-> None:
    #     """
    #     This function is responsible for generating the csv file,
    #     with the intervals of image sizes.
    #     """
    #     image_folder = DATASET_PATH
    #     interval_size = 100
    #     image_intervals