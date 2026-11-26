from selenium.webdriver.common.by import By

def test_debug(driver):
    driver.get("https://www.w3schools.com")
    for el in driver.find_elements(By.TAG_NAME, "input"):
        print("ID:", el.get_attribute("id"),
              "| NAME:", el.get_attribute("name"),
              "| PLACEHOLDER:", el.get_attribute("placeholder"),
              "| VISIBLE:", el.is_displayed())
    driver.save_screenshot("home.png")