from playwright.sync_api import sync_playwright
import time
import csv
import re 

Query = str(input('Enter the query: ')).strip()
file = Query.replace(' ','_')
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page2 = browser.new_page()
    page2.goto(f'https://www.amazon.in/s?k={Query}')
    max_page_element = page2.query_selector("//span[@class='s-pagination-item s-pagination-disabled']")
    max_page = int(max_page_element.inner_text() if max_page_element else 0)
    page2.close()
    with open(f"Scraped_data/{file}.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title",'Rating',"M.R.P(₹)", "Price(₹)","Discount", "URL"])
        for i in range(1,max_page+ 1):
            page = browser.new_page()
            page.goto(f'https://www.amazon.in/s?k={Query}&page={i}')
            divs = page.query_selector_all("//div[@class='puisg-row']")
            for div in divs:
                titleName = div.query_selector(".a-size-medium.a-spacing-none.a-color-base.a-text-normal")
            
                link = div.query_selector("a.a-link-normal.s-line-clamp-2.s-link-style.a-text-normal")
            
                price = div.query_selector(".a-price-whole")
            
                MRP = div.query_selector("//span[@class='a-price a-text-price']/span")
            
                rating = div.query_selector('.a-icon-alt')
            
                discount = div.query_selector("//span[@class='a-letter-space']/following-sibling::span[1]")
            

                discount_text = (re.findall(r'\d+',(discount.inner_text() if discount else "0" )))[0] + ' %' 

                title_text = titleName.inner_text() if titleName else "No title found"
            
                price_text = price.inner_text() if price else "No Price found"
            
                MRP_text =(( MRP.inner_text() if MRP else '').split('₹'))[-1]
                href = link.get_attribute('href') if link else ""
            
                rating_text = rating.inner_text() if rating else "No Rating Available"
                if not div.inner_text() or  title_text == "No title found":
                    continue


                full_url = f"https://www.amazon.in{href}" if href else "No link found"


                writer.writerow([title_text,rating_text,MRP_text, price_text,discount_text, full_url])

                print(f'Discount: {discount_text}')
                print(f"Title: {title_text}")
                print(f'Rating: {rating_text}')
                print(f'M.R.P: {MRP_text}')
                print(f"Price: {price_text}")
                print(f"URL: {full_url}\n")
            print(f'Page Fetched {i}')
        
            page.close()
            time.sleep(1)
    browser.close()
    print(f"✅ Data successfully saved to {file}.csv")
