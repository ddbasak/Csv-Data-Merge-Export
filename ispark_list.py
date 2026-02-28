# Web servisinden (API) veri çekmemizi sağlar.
import requests
# Veriyi tablo (DataFrame) olarak işler ve Excel dosyasına yazar.
import pandas as pd

park_url="https://api.ibb.gov.tr/ispark/Park"
# ?id= ile sonuna park ID’si eklendi.
park_detayli_url= "https://api.ibb.gov.tr/ispark/ParkDetay?id="

# requests.get API’den veri ister. status_code != 200: Eğer yanıt başarılı değilse (200 OK değilse), 
# hata verir ve program durur.
response= requests.get(park_url)
if response.status_code!=200:
    print("Park listesi oluşturulamadı")
    exit() #

park= response.json() #API'den gelen cevabı Python listesine çevirir.
data=[] #Sonuçları saklayacağımız boş listeyi oluşturur.

# for ile her bir otopark için döngü başlar. park.get("parkID"), arkın benzersiz ID’sini alır. 
# detail_response detaylı bilgi almak için parkID ile yeni bir istek yapılır.
for parklar in park:
    parklar_id= parklar.get("parkID")
    detayli_response=requests.get(park_detayli_url+ str(parklar_id))
    
    #API başarısızsa bu parkı atlar ve sonraki parkla devam eder.
    if detayli_response.status_code !=200:
        print(f"{parklar_id} için detay verisi oluşturulamadı")
        continue

    # try: Kodun içinde hata olursa program çökmesin diye kullanılır.
    #isinstance(detail, list): Gelen veri listeyse ilk eleman alınır.
    #len(detail) > 0: Liste boşsa veri yoktur; bu durumda park atlanır.
    try:
        detayli= detayli_response.json()
     
        if isinstance(detayli,list) and len(detayli)>0:
            detayli= detayli[0]
        else:
            print(f"{parklar_id} için detay kısmı boş")
            continue    

        row= {
            "park_id":detayli.get("parkID"),
            "park_adi":detayli.get("parkName"),
            "latitude":detayli.get("lat"),
            "longitude":detayli.get("lng"),
            "kapasite":detayli.get("capacity"),
            "çalisma_saatleri":detayli.get("workHours"),
            "park_tipi":detayli.get("parkType"),
            "ucretsiz_sure_limiti":detayli.get("freeTime"),
            "adres":detayli.get("address"),
            "sehir":"İstanbul"
        }
        data.append(row)

    except Exception as e:
        print(f"Hata (parklar_id):",e)

#Liste tabloya çevrildi ve kaydedildi.
df=pd.DataFrame(data)
df.to_excel("ispark_detayli_otopark_listesi.xlsx", index=False)

print("Excel dosyası oluşturuldu")