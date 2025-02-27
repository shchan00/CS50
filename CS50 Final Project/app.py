from flask import Flask, render_template, request, flash, send_file
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
from io import BytesIO
app = Flask(__name__, template_folder='templates')
app.secret_key = 'sjfgnjsenf'
options = ["Tokyo", "Osaka", "Kyoto", "Nagoya", "Yokohama", "Hakone", "Gotenba, Fuji","Fukuoka City", "Sapporo", "Jozankei", "Otaru, Kiroro, Shakotan", "Hiroshima, Miyajima"]
jalanlookup = {"Tokyo": "Tokyo", "Osaka": "Osaka", "Kyoto": "Kyoto", "Nagoya": "Aichi_Accommodation/Nagoya", "Yokohama": "Kanagawa_Accommodation/Yokohama", "Hakone": "Kanagawa_Accommodation/Hakone", 
               "Gotenba, Fuji": "Shizuoka_Accommodation/Gotenba_Fuji", "Fukuoka City": "Fukuoka_Accommodation/Fukuoka_City_Around_Hakata_Station_Around_Tenjin", "Sapporo": "Hokkaido_Accommodation/Sapporo", 
               "Jozankei": "Hokkaido_Accommodation/Jozankei", "Otaru, Kiroro, Shakotan": "Hokkaido_Accommodation/Otaru_Kiroro_Shakotan", "Hiroshima, Miyajima": "Hiroshima_Accommodation/Hiroshima_Miyajima"}
bookinglookup = {"Tokyo": "Tokyo", "Osaka": "Osaka", "Kyoto": "Kyoto", "Nagoya": "Nagoya", "Yokohama": "Yokohama", "Hakone": "Hakone", 
               "Gotenba, Fuji": "Gotenba", "Fukuoka City": "Fukuoka_City", "Sapporo": "Sapporo", 
               "Jozankei": "Jozankei", "Otaru, Kiroro, Shakotan": "Otaru_Kiroro_Shakotan", "Hiroshima, Miyajima": "Hiroshima_Miyajima"}
child2Num = 0
child3Num = 0
child4Num = 0
child5Num = 0


@app.route('/')
def hello_world():
    return render_template('index.html', list=options)

@app.route('/search', methods = ["POST"])
def search():
    pageNum = 1
    dict = []
    checkin = request.form.get("checkin")
    checkout = request.form.get("checkout")
    try:
        adultNum = int(request.form.get("adults"))
    except Exception:
        flash("Adult Number is not integer")
        return render_template('index.html', list=options)
    try:
        child1Num = request.form.get("children")
    except Exception:
        flash("Child Number is not integer")
        return render_template('index.html', list=options)
    
    loc = request.form.get("options")
    if loc not in options:
        flash("Location not in the options!")
        return render_template('index.html', list=options)
    dest = bookinglookup[loc]
    dest2 = jalanlookup[loc]
    if not (dest and dest2):
        flash("Website error cannot find location")
        return render_template('index.html', list=options)
    date_format = '%Y-%m-%d'
    try:
        date1 = datetime.strptime(checkin, date_format)
    except Exception:
        flash("Check in date is not datetime")
        return render_template('index.html', list=options)
    stayYear =date1.year
    stayMonth =date1.month
    stayDay = date1.day
    try:
        date2 = datetime.strptime(checkout, date_format)
    except Exception:
        flash("Check in date is not datetime")
        return render_template('index.html', list=options)
    stayCount = (date2 - date1).days
    if stayCount < 0:
        flash("Checkout date is before checkin date.")
        return render_template('index.html', list=options)
    elif stayCount == 0:
        flash("Please do not choose the same checkin and checkout date.")
    roomCrack = str(adultNum) + str(child1Num) + str(child2Num) + str(child3Num) + str(child4Num) + str(child5Num)
    url2 = f'https://www.booking.com/searchresults.en-us.html?checkin={checkin}&checkout={checkout}&selected_currency=USD&ss={dest}&ssne={dest}&ssne_untouched={dest}&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_type=city&group_adults={adultNum}&no_rooms=1&group_children={child1Num}&sb_travel_purpose=leisure'
    url = f'https://www.jalan.net/en/japan_hotels_ryokan/Accommodation/{dest2}_Accommodation/?adultNum={adultNum}&child1Num={child1Num}&child2Num={child2Num}&child3Num={child3Num}&child4Num={child4Num}&child5Num={child5Num}&stayYear={stayYear}&stayMonth={stayMonth}&stayDay={stayDay}&stayCount={stayCount}&roomCrack={roomCrack}&scVal=02&pageNum='

    #Credits to Amin Boutarfi for the youtube tutorial: https://www.youtube.com/watch?v=u08_es8UZhI&t=459s
    #Github: https://github.com/amineboutarfi/booking_scraper
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
 
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

        page = browser.new_page()
        page.goto(url2, timeout=60000) 
        hotels_list = []            
        hotels = page.locator('//div[@data-testid="property-card"]').all()
        for hotel in hotels:
            hotel_dict = {}
            hotel_dict["name"] = hotel.locator('//div[@data-testid="title"]').inner_text()
            try: 
                hotel_dict["price_usd"] = int(re.sub(r"[^\d.]", "", hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text(timeout = 1000)))
            except TimeoutError:
                continue
            hotel_dict["location"] = hotel.locator('//span[@data-testid="address"]').inner_text()
            try:
                hotel_dict["ratings"] = re.search(r'\d+\.\d+', hotel.locator('//div[@data-testid="review-score"]/div[1]').inner_text(timeout = 1000)).group()  + "/10"
            except Exception:
                hotel_dict["ratings"] = "-/10"
            hotel_dict["href"] = hotel.locator('a[data-testid="title-link"]').get_attribute('href') 
            hotel_dict["source"] = "booking.com"

            hotels_list.append(hotel_dict)
        hotels_list = sorted(hotels_list + dict, key=lambda x: x["price_usd"])
        browser.close()
        return render_template('search.html', hotels=hotels_list)
    flash("There is error trying to load the search result.")
    return render_template('index.html', list=options)

@app.route('/deepsearch', methods = ["POST", "GET"])
def deepsearch():
    if request.method == "GET":
        return render_template('deepsearch.html', list=options)
    pageNum = 1
    dict = []
    checkin = request.form.get("checkin")
    checkout = request.form.get("checkout")
    try:
        adultNum = int(request.form.get("adults"))
    except Exception:
        flash("Adult Number is not integer")
        return render_template('index.html', list=options)
    try:
        child1Num = request.form.get("children")
    except Exception:
        flash("Child Number is not integer")
        return render_template('index.html', list=options)
    
    loc = request.form.get("options")
    if loc not in options:
        flash("Location not in the options!")
        return render_template('index.html', list=options)
    dest = bookinglookup[loc]
    dest2 = jalanlookup[loc]
    if not (dest and dest2):
        flash("Website error cannot find location")
        return render_template('index.html', list=options)
    date_format = '%Y-%m-%d'
    try:
        date1 = datetime.strptime(checkin, date_format)
    except Exception:
        flash("Check in date is not datetime")
        return render_template('index.html', list=options)
    stayYear =date1.year
    stayMonth =date1.month
    stayDay = date1.day
    try:
        date2 = datetime.strptime(checkout, date_format)
    except Exception:
        flash("Check in date is not datetime")
        return render_template('index.html', list=options)
    stayCount = (date2 - date1).days
    if stayCount < 0:
        flash("Checkout date is before checkin date.")
        return render_template('index.html', list=options)
    elif stayCount == 0:
        flash("Please do not choose the same checkin and checkout date.")
    roomCrack = str(adultNum) + str(child1Num) + str(child2Num) + str(child3Num) + str(child4Num) + str(child5Num)
    url = f'https://www.jalan.net/en/japan_hotels_ryokan/Accommodation/{dest2}_Accommodation/?adultNum={adultNum}&child1Num={child1Num}&child2Num={child2Num}&child3Num={child3Num}&child4Num={child4Num}&child5Num={child5Num}&stayYear={stayYear}&stayMonth={stayMonth}&stayDay={stayDay}&stayCount={stayCount}&roomCrack={roomCrack}&scVal=02&pageNum='

    while True:
        # Making a GET request
        r = requests.get(url + str(pageNum))

        # check status code for response received
        # success code - 200

        # Parsing the HTML
        soup = BeautifulSoup(r.content, 'html.parser')
        s = soup.find_all('div', class_=['bread-crumb-cassette jsc-ellipsis-punkuzu-target','cassette-hotel-info', 'cassette-hotel-price'])
        if len(s) == 0:
            break
        counter = 0
        tag = {}
        for exp in s:
            #Means that the div is the location class
            if counter % 3 == 0:
                tag["location"] = exp.text.strip()
            #Means that the div is the info class
            elif counter % 3 == 1:
                tag["name"] = exp.find("h3").text
                tag["desc"] = exp.find('p', class_= 'cassette-hotel-locate jsc-ellipsis-target').text
                tag["ratings"] = exp.find_all("span")[1].text
                tag["href"] = 'https://www.jalan.net' + exp.find("a", href = True)['href']
            #Means that the div is the price class
            else:
                tryspan = exp.find_all("span")[0].text
                usd_pos = tryspan.find("USD")
                substring = tryspan[usd_pos + 4:]
                tag["price_usd"] = substring.replace(")", "")
                dict.append(tag.copy())
            counter += 1
        pageNum += 1
    dataframe = pd.DataFrame(dict)
    # Create a BytesIO object and save the DataFrame to it
    output = BytesIO()
    dataframe.to_excel(output, index=False)
    output.seek(0)

    # Send the file to the user
    return send_file(output, download_name='search_result.xlsx', as_attachment=True)


if __name__ == '__main__':
    app.run()