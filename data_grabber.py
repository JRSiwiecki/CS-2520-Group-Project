from bing_image_downloader import downloader

colors = ["red", "orange", "yellow", "green", "cyan", "blue", "purple", "pink"]
values = ["dark", "", "bright"]
for c in colors:
    for v in values:
        downloader.download(v + " " + c, limit=2,  output_dir='dataset', adult_filter_off=True, force_replace=False, timeout=60, verbose=False)
    print(c + " completed")
print("DONE")