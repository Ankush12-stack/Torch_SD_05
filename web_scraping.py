import requests
from bs4 import BeautifulSoup
import csv

def extract_product_info(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    products = []
    for product in soup.find_all("div", class_="s-result-item"):
        try:
            name = product.find("span", class_="a-text-normal").text.strip()
            price = product.find("span", class_="a-price-whole").text.strip()
            rating = product.find("span", class_="a-icon-alt").text.strip()
            products.append({"Name": name, "Price": price, "Rating": rating})
        except AttributeError:
            continue
    
    return products

def save_to_csv(products, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Price', 'Rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for product in products:
            writer.writerow(product)

if __name__ == "__main__":
    url = "https://www.amazon.com/s?k=laptop"
    products = extract_product_info(url)
    save_to_csv(products, "products.csv")
