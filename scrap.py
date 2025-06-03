import os
from lxml import etree
import requests

html = '''
'''


def extract_image_urls(html_content):
    # Parse the HTML content
    tree = etree.HTML(html_content)

    # Find the name of the directory to save images
    name = tree.xpath('//div[@class="mhy-emoji-square-banner__title"]/text()')[0].strip()

    # Find grid
    grid = tree.xpath('//div[@class="mhy-emoji-square__infos--nowrap"]')[0]

    # Use XPath to find all img elements with the specified attribute
    img_elements = grid.xpath('.//img[@imgblob]')

    # Extract the 'imgblob' attribute from each img element
    image_urls = [img.get('imgblob') for img in img_elements]

    return name, image_urls
def main():
    # Extract image URLs from the HTML content
    name, image_urls = extract_image_urls(html)
    # Create a directory to save the images
    os.makedirs(name, exist_ok=True)
    # Print the extracted image URLs
    count = 0
    for url in image_urls:
        if not url:
            continue
        count += 1
        url = url.split('?')[0]
        filename = os.path.join(name, os.path.basename(url))
        # Download the image
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download {url}: Status code {response.status_code}")
    print(f"Total images downloaded: {count}")

if __name__ == "__main__":
    main()
