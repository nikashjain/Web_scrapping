Python code to download bulk images form Bing, Google and duckduckgo.

```bash
pip install -r requirements.txt 
```
Usage:
Run ```python main.py``` Select the required Browser

Install chromedriver by visiting "https://chromedriver.chromium.org/downloads" ,based on your google chrome version.

Usage for Bing.py

`query` : String to be searched.
`limit` : Number of images to download.
`output_dir` : (optional, default is 'dataset') Name of output dir.
`adult_filter_off` : (optional, default is True) Enable of disable adult filteration.
`force_replace` : (optional, default is False) Delete folder if present and start a fresh download.
`timeout` : (optional, default is 60) timeout for connection in seconds.Change based on your internet speed.
`filter` : (optional, default is "") filter, choose from [line, photo, clipart, gif, transparent, Large, small, medium]
`verbose` : (optional, default is True) Enable downloaded message.

Usage for Google:
`query` : String to be searched.
`limit` : Number of images to download.
`filter`: Apply size filter

Usage for duckduckgo:
`query` : String to be searched.
`limit` : Number of images to download.
`filter`: Choose from [Large, Medium, Small, Wallpaper] 


