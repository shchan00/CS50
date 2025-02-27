from playwright.sync_api import sync_playwright, TimeoutError
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import time
def scroll_down(page):
    # Function to scroll down the page
    try:
        button = page.locator('[aria-label="Dismiss sign-in info."]', timeout=2000)
        button.click()
    except Exception as e:
        print(e)
    page.mouse.wheel(0, 15000)
    page.mouse.wheel(0, -300)
    page.wait_for_timeout(100000)  # Wait for content to load
def main():
    
    with sync_playwright() as p:
        
        # IMPORTANT: Change dates to future dates, otherwise it won't work
        pageNum = 1
        adultNum = 2
        child1Num = 0
        child2Num = 0
        child3Num = 0
        child4Num = 0
        child5Num = 0
        roomCrack = str(adultNum) + str(child1Num) + str(child2Num) + str(child3Num) + str(child4Num) + str(child5Num)
        stayYear = 2024
        stayMonth = 12
        stayDay = 27
        stayCount = 1
        checkin_date = '2024-12-27'
        checkout_date = '2024-12-28'
        dest = "Tokyo"
        #Fukuoka_City
        dest2 ="Hiroshima_Accommodation/Hiroshima_Miyajima"
        #Hiroshima_Accommodation/Hiroshima_Miyajima
        #Hokkaido_Accommodation/Otaru_Kiroro_Shakotan
        #Hokkaido_Accommodation/Jozankei
        #Hokkaido_Accommodation/Sapporo
        #Fukuoka_Accommodation/Fukuoka_City_Around_Hakata_Station_Around_Tenjin
        #Shizuoka_Accommodation/Gotenba_Fuji
        #Kanagawa_Accommodation/Hakone
        #Kanagawa_Accommodation/Yokohama
        #Aichi_Accommodation/Nagoya_Accommodation
        dict = []
        url2 = f'https://www.booking.com/searchresults.en-us.html?checkin={checkin_date}&checkout={checkout_date}&selected_currency=USD&ss={dest}&ssne={dest}&ssne_untouched={dest}&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_type=city&group_adults={adultNum}&no_rooms=1&group_children={child1Num}&sb_travel_purpose=leisure'
        url = f'https://www.jalan.net/en/japan_hotels_ryokan/Accommodation/{dest2}_Accommodation/?adultNum={adultNum}&child1Num={child1Num}&child2Num={child2Num}&child3Num={child3Num}&child4Num={child4Num}&child5Num={child5Num}&stayYear={stayYear}&stayMonth={stayMonth}&stayDay={stayDay}&stayCount={stayCount}&roomCrack={roomCrack}&scVal=02&pageNum='
        browser = p.chromium.launch(headless=False)
        print(url)
         # Making a GET request
        r = requests.get(url + str(pageNum))

        # check status code for response received
        # success code - 200

        # Parsing the HTML
        soup = BeautifulSoup(r.content, 'html.parser')
        s = soup.find_all('div', class_=['bread-crumb-cassette jsc-ellipsis-punkuzu-target','cassette-hotel-info', 'cassette-hotel-price'])
        counter = 0
        tag = {}
        for exp in s:
            #Means that the div is the location class
            if counter % 3 == 0:
                tag["location"] = exp.text.strip()
            #Means that the div is the info class
            elif counter % 3 == 1:
                tag["name"] = exp.find("h3").text
                #tag["desc"] = exp.find('p', class_= 'cassette-hotel-locate jsc-ellipsis-target').text
                tag["ratings"] = exp.find_all("span")[1].text + "/5"
                tag["href"] = 'https://www.jalan.net' + exp.find("a", href = True)['href']
                tag["source"] = "jalan"
            #Means that the div is the price class
            else:
                tryspan = exp.find_all("span")[0].text
                usd_pos = tryspan.find("USD")
                substring = tryspan[usd_pos + 4:]
                tag["price_usd"] = int(substring.replace(")", "").replace(",",""))
                dict.append(tag.copy())
            counter += 1
        dataframe = pd.DataFrame(dict)
        dataframe.to_excel("test.xlsx", index=False)

        page = browser.new_page()
        page.goto(url2, timeout=60000) 
                    
        hotels = page.locator('//div[@data-testid="property-card"]').all()
        print(f'There are: {len(hotels)} hotels.')
        

        hotels_list = []
        for hotel in hotels:
            hotel_dict = {}
            hotel_dict['name'] = hotel.locator('//div[@data-testid="title"]').inner_text()
            print(hotel_dict['name'])
            try: 
                hotel_dict['price_usd'] = int(re.sub(r"[^\d.]", "", hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text(timeout = 1000)))
            except TimeoutError:
                continue
            hotel_dict['location'] = hotel.locator('//span[@data-testid="address"]').inner_text()
            try:
                hotel_dict['ratings'] = re.search(r'\d+\.\d+', hotel.locator('//div[@data-testid="review-score"]/div[1]').inner_text(timeout = 1000)).group()  + "/10"
            except TimeoutError:
                hotel_dict['ratings'] = "-/10"
            hotel_dict['href'] = hotel.locator('a[data-testid="title-link"]').get_attribute('href') 
            hotel_dict["source"] = "booking.com"

            hotels_list.append(hotel_dict)
        hotels_list = sorted(hotels_list + dict, key=lambda x: x["price_usd"])
        df = pd.DataFrame(hotels_list)
        df.to_excel('hotels_list.xlsx', index=False) 
        df.to_csv('hotels_list.csv', index=False) 
        
        browser.close()

            
if __name__ == '__main__':
    main()