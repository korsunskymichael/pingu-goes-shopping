import requests
import re


url = "https://www.shufersal.co.il/online/he/search?text=%D7%AA%D7%A4%D7%95%D7%97"

r = requests.get(url)

file_name = "C:\\Users\\mikor\\PycharmProjects\\shopsshupersal_output.txt"

with open(file_name, "w", encoding="utf-8") as f:
    for match in re.finditer(r'data-product-code="P_\d+">([^<]+).*?class="price">(.*?)<span\s+class="currency">.*?<span class="priceUnit">(.*?)</div', r.text, re.DOTALL|re.IGNORECASE):
        otput_str = f"name: {match.group(1)},  price: {match.group(2)}, units: {match.group(3)}"
        output_fixed_str = re.sub(r'\s+', ' ', re.sub(r'</?span[^>]*>', '', otput_str.replace('&quot;', '"')))


