# Japan Hotel Web Scraper
#### Video Demo:  [Video Demo](https://www.youtube.com/watch?v=x-HBo7pGa7s)
#### Description:
This is a mini project that I made which uses bs4 and plawright chromium to scrap hotel data from jalan and booking.com. 
The project uses flask for the webpage.
##Installation
You can try to install via:
```bash
pip install -r requirements.txt
playwright install chromium
```
After install you can use
```bash
flash run
```
to run the program.
## Main page
In the main page, just enter the checkin, checkout dates, number of adults and children as well as destination.
Currently, there is only 1 room fixed and the amount of locations are limited as well.
## Deep Search
There is also a function called deep search. Instead of giving the first few results, the deep search gives all result available.
There is no display for deep search and only downloads the excel file. Only available for jalan source.
## Project Mechanism (Only added this because submit50 said description is not long enough)

In order to scrape the data from the 2 websites jalan and booking.com, the simulation of query is needed.
For jalan, it requires adult number, child 1-5 number (Which from the website of jalan refers to different age infants),
a roomcrack value (Which is just adults number + all child number in string), a scVal (Which to this day I still do not know what it is),
a check-in date and a staycount (meaning how long you have to stay), as well as a special method indicating the location.
Each location is different so I have to manually try to check for the url. Thats what the jalanlookup array is for.

For booking.com, it requires a checkin and checkout date, adults number, child number, as well as location (the ss and ssne may mean different things
but I put in the same thing). There is also a special lookup for booking.com to translate location into the url.

The index page allows to user to fill in the corrisponding information while having front-end and back-end check. After the index form is filled in and submitted,
the back-end started to scrape real-time.

For jalan, I used bs4 since it is very easy comparatively to scrape. There are 3 main class for divs which contains different information. A counter is used to make sure each 3 is combined
into 1 entry. For booking.com, chromium is used since last time I checked, the data-testid changed when I used bs4 which makes it very hard to scrape with that. Therefore, playwright chromium
is used which is literally a browser. The difficult part is that when there is certain information missing, the program stops running. For that, I added a timeout and a try argument to make it skip
if that situation happened.

Finally, combining both data and sorting it with price, the data is sent to the website which it is displayed in the html. A filter for it has been implemented so that if a certain source isn't wanted,
it could be opted out. 

For the deep search, it is basically the same except another attributes was added which is page number, which increases everytime until the back-end receives nothing. Then, instead of displaying, an excel was given back to the user considering the display limit of website and that people who wanted to scrape everything probably isn't really looking for booking hotels. The obstacle for implementing
deep search for booking.com is that there is an ad blocking it to scroll down. And so far, no effective measures of closing the ad has been found. Therefore, there is no deep search function.