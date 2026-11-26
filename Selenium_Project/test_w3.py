import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.w3schools.com/"
SEARCH_ID = "tnb-google-search-input"


# ---------- Homepage ----------
def test_homepage_title(driver):
    driver.get(URL)
    WebDriverWait(driver, 10).until(EC.title_contains("W3Schools"))
    assert "W3Schools" in driver.title

def test_homepage_url(driver):
    driver.get(URL)
    assert "w3schools.com" in driver.current_url

def test_search_box_visible(driver):
    driver.get(URL)
    box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, SEARCH_ID)))
    assert box.is_displayed()
    assert box.get_attribute("placeholder") == "Search..."


# ---------- Search ----------
@pytest.mark.parametrize("keyword", ["HTML", "CSS", "Python", "SQL", "JavaScript"])
def test_search_valid(driver, keyword):
    driver.get(URL)
    old_url = driver.current_url
    box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, SEARCH_ID)))
    box.send_keys(keyword)
    box.send_keys(Keys.ENTER)
    WebDriverWait(driver, 10).until(lambda d: d.current_url != old_url)
    assert keyword.lower() in driver.page_source.lower()

def test_search_empty(driver):
    driver.get(URL)
    old_url = driver.current_url
    box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, SEARCH_ID)))
    box.send_keys(Keys.ENTER)
    assert driver.current_url == old_url


# ---------- Navigation ----------
def test_html_tutorial_open(driver):
    driver.get(URL + "html/")
    WebDriverWait(driver, 10).until(EC.title_contains("HTML"))
    assert "HTML Tutorial" in driver.title

def test_python_tutorial_open(driver):
    driver.get(URL + "python/")
    WebDriverWait(driver, 10).until(EC.title_contains("Python"))
    assert "Python Tutorial" in driver.title

def test_next_chapter_button(driver):
    driver.get(URL + "html/")
    old_url = driver.current_url
    nxt = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Next')]")))
    nxt.click()
    WebDriverWait(driver, 10).until(lambda d: d.current_url != old_url)
    assert driver.current_url != old_url

# ---------- Try it Yourself (iframe) ----------
def test_try_it_yourself_run(driver):
    driver.get("https://www.w3schools.com/html/tryit.asp?filename=tryhtml_default")
    # Run button dabao
    run_btn = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Run')]")))
    run_btn.click()
    # Result iframe ke andar switch karo
    WebDriverWait(driver, 15).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "iframeResult")))
    heading = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1")))
    assert heading.text != ""
    # Wapas main page pe aao
    driver.switch_to.default_content()

# ---------- More Navigation ----------
@pytest.mark.parametrize("path, title_word", [
    ("css/", "CSS Tutorial"),
    ("js/", "JavaScript Tutorial"),
    ("sql/", "SQL Tutorial"),
    ("java/", "Java Tutorial"),
])
def test_more_tutorials_open(driver, path, title_word):
    driver.get(URL + path)
    WebDriverWait(driver, 10).until(EC.title_contains(title_word))
    assert title_word in driver.title

def test_previous_chapter_button(driver):
    driver.get(URL + "html/html_intro.asp")
    old_url = driver.current_url
    prev = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Previous')]")))
    prev.click()
    WebDriverWait(driver, 10).until(lambda d: d.current_url != old_url)
    assert driver.current_url != old_url

def test_browser_back_button(driver):
    driver.get(URL + "html/")
    first_url = driver.current_url
    nxt = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Next')]")))
    nxt.click()
    WebDriverWait(driver, 10).until(lambda d: d.current_url != first_url)
    driver.back()
    WebDriverWait(driver, 10).until(lambda d: d.current_url == first_url)
    assert driver.current_url == first_url


# ---------- Responsive ----------
@pytest.mark.parametrize("width, height", [(1920, 1080), (768, 1024), (375, 667)])
def test_responsive_homepage(driver, width, height):
    driver.set_window_size(width, height)
    driver.get(URL)
    WebDriverWait(driver, 10).until(EC.title_contains("W3Schools"))
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.is_displayed()
    assert "W3Schools" in driver.title


# ---------- Negative ----------
def test_invalid_page_404(driver):
    driver.get(URL + "this_page_does_not_exist_123/")
    assert "404" in driver.title or "404" in driver.page_source

# # ---------- Evidence screenshots (for report) ----------
# def test_capture_evidence(driver):
#     import os
#     os.makedirs("evidence", exist_ok=True)

#     driver.get(URL)
#     WebDriverWait(driver, 10).until(EC.title_contains("W3Schools"))
#     driver.save_screenshot("evidence/1_homepage.png")

#     box = driver.find_element(By.ID, SEARCH_ID)
#     box.send_keys("Python")
#     driver.save_screenshot("evidence/2_search_typed.png")
#     box.send_keys(Keys.ENTER)
#     WebDriverWait(driver, 10).until(lambda d: d.current_url != URL)
#     driver.save_screenshot("evidence/3_search_result.png")

#     driver.get("https://www.w3schools.com/html/tryit.asp?filename=tryhtml_default")
#     WebDriverWait(driver, 15).until(
#         EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Run')]"))).click()
#     driver.save_screenshot("evidence/4_try_it_yourself.png")