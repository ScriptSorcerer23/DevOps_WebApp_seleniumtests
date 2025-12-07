import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    yield driver
    driver.quit()

BASE_URL = "http://54.183.180.138:5000"

def test_homepage_load(driver):
    driver.get(BASE_URL)
    assert "Stroke Prediction" in driver.title or "Login" in driver.page_source

def test_register_user(driver):
    driver.get(f"{BASE_URL}/auth/register")
    wait = WebDriverWait(driver, 10)
    email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    email_field.send_keys("test@example.com")
    driver.find_element(By.NAME, "username").send_keys("testuser")
    driver.find_element(By.NAME, "full_name").send_keys("Test User")
    driver.find_element(By.NAME, "password").send_keys("TestPass123!")
    driver.find_element(By.NAME, "confirm_password").send_keys("TestPass123!")
    driver.find_element(By.TAG_NAME, "form").submit()
    wait.until(EC.url_contains("/auth/login"))
    assert "/auth/login" in driver.current_url

def test_login_user(driver):
    driver.get(f"{BASE_URL}/auth/login")
    wait = WebDriverWait(driver, 10)
    email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    email_field.send_keys("test@example.com")
    driver.find_element(By.NAME, "password").send_keys("TestPass123!")
    driver.find_element(By.TAG_NAME, "form").submit()
    wait.until(EC.url_contains("/"))
    assert "/" in driver.current_url or "dashboard" in driver.current_url

def test_dashboard_access(driver):
    # Assuming logged in from previous test
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    assert "Dashboard" in driver.page_source or "Welcome" in driver.page_source

def test_navigate_to_patients(driver):
    driver.get(f"{BASE_URL}/patients")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")) or EC.presence_of_element_located((By.CLASS_NAME, "patient-list")))
    assert "Patients" in driver.page_source

def test_add_patient(driver):
    driver.get(f"{BASE_URL}/patients/add")  # Assuming add route
    wait = WebDriverWait(driver, 10)
    name_field = wait.until(EC.presence_of_element_located((By.NAME, "name")))
    name_field.send_keys("John Doe")
    driver.find_element(By.NAME, "age").send_keys("45")
    driver.find_element(By.NAME, "gender").send_keys("Male")
    # Add more fields as needed
    driver.find_element(By.TAG_NAME, "form").submit()
    wait.until(EC.url_contains("/patients"))
    assert "/patients" in driver.current_url

def test_view_patient_details(driver):
    driver.get(f"{BASE_URL}/patients")
    wait = WebDriverWait(driver, 10)
    patient_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "John Doe")))  # Assuming name is link
    patient_link.click()
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
    assert "John Doe" in driver.page_source

def test_search_patients(driver):
    driver.get(f"{BASE_URL}/patients")
    wait = WebDriverWait(driver, 10)
    search_field = wait.until(EC.presence_of_element_located((By.NAME, "search")))
    search_field.send_keys("John")
    driver.find_element(By.ID, "search-btn").click()  # Assuming button id
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "search-results")))
    assert "John Doe" in driver.page_source

def test_logout(driver):
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)
    logout_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Logout")))
    logout_link.click()
    wait.until(EC.url_contains("/auth/login"))
    assert "/auth/login" in driver.current_url

def test_invalid_login(driver):
    driver.get(f"{BASE_URL}/auth/login")
    wait = WebDriverWait(driver, 10)
    email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    email_field.send_keys("invalid@example.com")
    driver.find_element(By.NAME, "password").send_keys("wrongpass")
    driver.find_element(By.TAG_NAME, "form").submit()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "alert-danger")))
    assert "Invalid" in driver.page_source or "error" in driver.page_source

# 10th test: Test responsive design or another feature
def test_responsive_menu(driver):
    driver.set_window_size(768, 1024)  # Tablet size
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)
    menu_toggle = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "navbar-toggler")))
    menu_toggle.click()
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "navbar-collapse")))
    assert driver.find_element(By.CLASS_NAME, "navbar-collapse").is_displayed()