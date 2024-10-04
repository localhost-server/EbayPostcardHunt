from playwright.sync_api import sync_playwright
import json
import time
# import asyncio

# Load cookies from the text file
with open('Authcookies.txt', 'r') as file:
    cookies = json.load(file)

def open_browser(page):
    page.set_viewport_size({'width': 1900, 'height': 1000})
    page.emulate_media(color_scheme='dark')
    weblink="https://www.developer.ebay.com/my/auth/?env=production&index=0&auth_type=oauth"
    # weblink="https://www.developer.ebay.com/"
    page.goto(weblink)
    time.sleep(2)
    # while page.is_visible('div.js-message.skrppp'):
    #     page.click('#accept-all')
        # time.sleep(2)
    return page

def getToken(cookies):
    with sync_playwright() as p:
        
        # Ensure all cookies have valid 'sameSite' values
        valid_same_site_values = {"Strict", "Lax", "None"}

        for cookie in cookies:
            # Fix 'sameSite' if invalid or unspecified
            if cookie.get("sameSite") not in valid_same_site_values:
                cookie["sameSite"] = "Lax"  # Default to "Lax" or choose another valid value

            # Ensure 'sameSite' is not None (could lead to another error)
            if cookie.get("sameSite") is None:
                cookie["sameSite"] = "Lax"


        browser = p.firefox.launch(headless=False)
        context = browser.new_context()
        context.add_cookies(cookies)

        page=context.new_page()
        open_browser(page)

        if page.is_visible('section.app-signin-tabs'):
            page.click("text=Sign in")

            time.sleep(1)
            page.fill('input[name="subject"]', 'davidmatlock59@yahoo.com')
            time.sleep(1)
            page.fill('input[name="password"]', 'AGChurch-59')
            # page.click('button.sign-in-button.btn')
            time.sleep(1)
            page.keyboard.press('Enter')

        time.sleep(10)

        # clicking on particular location using mouse
        # page.click('xpath=//*[@id="s0-1-24-7-60-9-72-signin"]')
        button_sec=page.query_selector_all('button.btn.btn--fluid.btn--primary')
        button_sec[1].click()
        time.sleep(5)
        try:    
            tokenSection= page.query_selector('div.gutter-top.token.break')
            token=tokenSection.inner_text()
            
        except:
            button_sec=page.query_selector_all('button.btn.btn--fluid.btn--primary')
            button_sec[1].click()
            time.sleep(5)
            tokenSection= page.query_selector('div.gutter-top.token.break')
            token=tokenSection.inner_text()

        print(token)
        # saving token to file
        with open('token.txt', 'w') as file:
            file.write(token)

        # saving the cookies to file
        cookies = context.cookies()
        with open('Authcookies.txt', 'w') as file:
            json.dump(cookies, file)

# if __name__ == '__main__':
getToken(cookies)