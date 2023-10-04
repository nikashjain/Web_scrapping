from os.path import exists, join
from os import makedirs
from logging import FileHandler, StreamHandler, basicConfig, info, warning, INFO, root
from datetime import datetime

from downloader import download
from duckduckgo import download_images
from Google_with_related_search import download_images_google


# def setup_logging():
#     name=datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
#     basicConfig(
#         level=INFO,
#         format="%(asctime)s - %(levelname)s - %(message)s",
#         handlers=[
#             StreamHandler(sys.stdout),  # Send logs to the console
#             FileHandler('my_log_file.log')  # Save logs to a file
#         ]
#     )
def log() -> None:
    """
    This function will store the all the logs
    for each time the program runs
    """
    name = datetime.now().strftime("%Y-%m-%d%H_%M_%S")
    if not exists("logs"):
        makedirs("logs")

    basicConfig(
        level=INFO,
        format="%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s",
        handlers=[FileHandler(join("logs", f"{name}.log"), mode="w"), StreamHandler()],
    )
    stream_handler = [h for h in root.handlers if isinstance(h, StreamHandler)][0]
    stream_handler.setLevel(INFO)


def menu():
    # setup_logging()
    # logging = logging.getLogger(__name__)
    info("Choose an option:")
    info("1. Download images using google images")
    info("2. Download images using bing images")
    info("3. Download images using duckduckgo")
    info("4. Download images with all search engines")
    info("5  Exit")
    choice = input("Enter your choice (1/2/3/4/5): ")
    while True:
        if choice == "1":
            query = input("Enter the search query: ")
            num_images = int(input("Enter the number of images to download: "))
            size_filter = input(
                "Enter the size filter (e.g., 'large', 'medium', 'icon'): "
            )

            downloaded_images = download_images_google(query, num_images, size_filter)
            info(f"Downloaded {num_images} images.")
            break

        elif choice == "2":
            query = input("Enter your query:")
            limit = int(input("enter number of images required:"))
            filter = input("enter filter if required: ")
            # with open(r'C:\Users\Lenovo\OneDrive\Desktop\FWD\Web scraping\bing_image_downloader\Query.txt') as f:
            #     for line in f:
            #         query =(line.strip())
            download(query, limit=limit, filter=filter)
            break
        elif choice == "3":
            query = input("Enter the search query: ")
            num_images = int(input("Enter the number of images to download: "))
            size_filter = input(
                "Enter the size filter (e.g., 'Large', 'Medium', 'Small', 'Wallpaper'): "
            )
            downloaded_images = download_images(query, num_images, size_filter)
            info(f"Downloaded {downloaded_images} images")
            break
        elif choice == "4":
            query = input("Enter the search query: ")
            num_images = int(input("Enter the number of images to download: "))
            size_filter = input(
                "Enter the size filter (e.g., 'large', 'medium', 'icon'): "
            )

            # Run the google image search
            downloaded_images_google = download_images_google(
                query, num_images, size_filter
            )
            info(f"Downloaded {downloaded_images_google} images from Google Images.")

            # Run the bing images with the same inputs
            downloaded_images_bing = download(
                query, limit=num_images, filter=size_filter
            )
            info(f"Downloaded {downloaded_images_bing} images from Bing Images.")

            # Run the duckduckgo with the same inputs
            downloaded_images_duckduckgo = download_images(
                query, num_images, size_filter
            )
            info(f"Downloaded {downloaded_images_duckduckgo} images from DuckDuckGo.")
            break
        elif choice == "5":
            info("Exiting the program. Goodbye!")
            break
        else:
            warning("Invalid choice. Please choose a valid option (1/2/3/4).")


if __name__ == "__main__":
    log()
    menu()
