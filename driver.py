from mosaic import *
from bing_image_downloader import downloader

# default search words
search_words = "Red Fruit"

try:
    img = cv2.imread("rainbow.png", cv2.IMREAD_COLOR)
    
    # scrape images from bing 💀
    # search_words = input("What would you like to generate your mosaic out of? ")
    # downloader.download(search_words, limit=30,  output_dir='dataset', adult_filter_off=False, force_replace=False, timeout=30, verbose=True)
except:
    print("Can't find that file")
    exit()    

mosaic = MosaicImage(ref_img=img, unit_size=90, enable_debug=True)
print(mosaic)
show_image(mosaic.generate_collage())