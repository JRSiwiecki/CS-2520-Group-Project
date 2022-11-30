from mosaic import *
from bing_image_downloader import downloader
from bs4 import BeautifulSoup
import json
import urllib.request, urllib.error, urllib.parse

# default search words
word = "candy"
color = "green"

def get_soup(url,header):
    return BeautifulSoup(urllib.request.urlopen(
        urllib.request.Request(url,headers=header)),
        'html.parser')

try:
    url="http://www.bing.com/images/search?q=" + color + "%20AND%20" + word + "&FORM=HDRSC2"

    #provide directory name
    DIR="dataset"
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    soup = get_soup(url,header)

    ActualImages=[]# contains the link for Large original images, type of  image
    for a in soup.find_all("a",{"class":"iusc"}):
        print(a)
        m = json.loads(a["m"])
        murl = m["murl"]
        turl = m["turl"]

        image_name = urllib.parse.urlsplit(murl).path.split("/")[-1]
        print(image_name)

        ActualImages.append((image_name, turl, murl))

    print("total:" , len(ActualImages),"images")

    if not os.path.exists(DIR):
        os.mkdir(DIR)

    DIR = os.path.join(DIR, word.split()[0] + " AND " + color)
    if not os.path.exists(DIR):
        os.mkdir(DIR)

    #print images
    for i, (image_name, turl, murl) in enumerate(ActualImages):
        try:
            raw_img = urllib.request.urlopen(turl).read()

            cntr = len([i for i in os.listdir(DIR) if image_name in i]) + 1

            f = open(os.path.join(DIR, image_name),'wb')
            f.write(raw_img)
            f.close()
        except Exception as e:
            print("could not load : " + image_name)
            print(e)

    img = cv2.imread("rainbow2.png", cv2.IMREAD_COLOR)
    
    # scrape images from bing 💀
    # search_words = input("What would you like to generate your mosaic out of? ")
    # downloader.download(search_words, limit=30,  output_dir='dataset', adult_filter_off=False, force_replace=False, timeout=30, verbose=True)
except:
    print("Can't find that file")
    exit()    

mosaic = MosaicImage(ref_img=img, unit_size=60, enable_debug=True)
print(mosaic)
show_image(mosaic.resized_img)
#mosaic.set_sub_images()
#show_image(mosaic.generate_collage())
