from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import time
import re

def get_product_links(product_name):
    links = []
    search_query = f"{product_name} site:amazon.com"
    url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"

    print(f"Searching Google with query: {search_query}")

    options = Options()
    options.add_argument("--headless=new")  # Updated headless argument
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")

    try:
        # Using Selenium Manager (built into newer versions of Selenium)
        driver = webdriver.Chrome(options=options)
        
        driver.get(url)
        time.sleep(3)  # Increased wait time

        # Wait for search results to appear
        search_results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.g"))
        )

        for result in search_results:
            try:
                link = result.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
                if re.search(r'amazon\.com', link):
                    # Filter out non-product pages
                    if '/dp/' in link or '/gp/product/' in link:
                        links.append(link)
            except Exception as e:
                continue

            if len(links) >= 5:
                break

    except WebDriverException as e:
        print(f"WebDriver error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()

    return links

def main():
    try:
        product_name = input("Enter product name: ")
        product_links = get_product_links(product_name)

        if product_links:
            print("\nProduct links:")
            for i, link in enumerate(product_links, 1):
                print(f"{i}. {link}")
        else:
            print("No product links found. Please try again with a different search term.")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An error occurred in main: {e}")

if __name__ == "__main__":
    main()