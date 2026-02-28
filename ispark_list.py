import requests
import pandas as pd

park_url="https://api.ibb.gov.tr/ispark/Park"
park_detayli_url= "https://api.ibb.gov.tr/ispark/ParkDetay?id="

# Hata verir ve program durur.
response= requests.get(park_url)
if response.status_code!=200:
    print("Park listesi oluşturulamadı")
    exit() #

park= response.json() #API'den gelen cevabı Python listesine çevirir.
data=[] #Sonuçları saklayacağımız boş listeyi oluşturur.

# For ile her bir otopark için döngü başlar. 
for parklar in park:
    parklar_id= parklar.get("parkID")
    detayli_response=requests.get(park_detayli_url+ str(parklar_id))
    
    #API başarısızsa bu parkı atlar ve sonraki parkla devam eder.
    if detayli_response.status_code !=200:
        print(f"{parklar_id} için detay verisi oluşturulamadı")
        continue

    # Try, koddaki hata kontrolü sağlanır.
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
