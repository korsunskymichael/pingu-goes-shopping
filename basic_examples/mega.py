import requests

url = "https://www.mega.co.il/v2/retailers/1182/branches/1390/products?appId=15&filters=%7B%22must%22:%7B%22exists%22:%5B%22family.id%22,%22family.categoriesPaths.id%22,%22branch.regularPrice%22%5D,%22term%22:%7B%22branch.isActive%22:true,%22branch.isVisible%22:true%7D%7D,%22mustNot%22:%7B%22term%22:%7B%22branch.regularPrice%22:0%7D%7D%7D&from=12&isSearch=true&languageId=1&query=%D7%AA%D7%A4%D7%95%D7%97&size=100"
r = requests.get(url)

products = (r.json())['products']

file_name = "C:\\Users\\korsu\\PycharmProjects\\shops\\outputs\\mega_output.txt"

with open(file_name, "w", encoding="utf-8") as f:
    for product in products:
        name = product.get('names').get('1').get("short")
        price = product.get('branch').get('regularPrice')
        f.write(f"name: {name}, price: {price}\n")





