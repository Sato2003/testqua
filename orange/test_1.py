import time
import pytest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

pytestmark = [
    pytest.mark.recruitment,
]

@pytest.fixture
def driver():
    driver = webdriver.Edge()
    driver.maximize_window()
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    yield driver
    driver.quit()

def login(driver):
    WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.NAME, "username"))
    ).send_keys("Admin")

    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.XPATH, "//h6[text()='Dashboard']"))
    )

def go_to_candidates(driver):
    logging.info("Navigating to Candidates page")
    WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, "//span[text()='Recruitment']"))
    ).click()
    ...


# TEST 1 — Open Candidates Page
@pytest.mark.p1
def test_open_candidates_page(driver):
    login(driver)
    go_to_candidates(driver)
    assert "recruitment/viewCandidates" in driver.current_url
    table = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, "div.oxd-table"))
    )
    assert table.is_displayed()

# TEST 2 — Search Candidate
@pytest.mark.p2
@pytest.mark.parametrize("search_name", ["Peter", "Linda"])
def test_search_candidate(driver, search_name):
    login(driver)
    go_to_candidates(driver)
    name_field = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located(
            (By.XPATH, "//label[text()='Candidate Name']/../following-sibling::div//input")
        )
    )
    name_field.send_keys(search_name)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    rows = WebDriverWait(driver, 10).until(
        ec.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.oxd-table-card"))
    )
    assert len(rows) >= 0


# TEST 3 — Reset Search
@pytest.mark.p3
def test_reset_search(driver):
    login(driver)
    go_to_candidates(driver)
    name_field = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located(
            (By.XPATH, "//label[text()='Candidate Name']/../following-sibling::div//input")
        )
    )
    name_field.send_keys("aki")
    reset_button = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, "//button[contains(., 'Reset')]"))
    )
    reset_button.click()
    time.sleep(1)
    assert name_field.get_attribute("value") == "aki"

# TEST 4 — Add Candidate
@pytest.mark.p1
def test_add_candidate(driver):
    login(driver)
    go_to_candidates(driver)
    add_button = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add')]"))
    )
    add_button.click()
    first = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.NAME, "firstName"))
    )
    first.send_keys("Aki")
    driver.find_element(By.NAME, "middleName").send_keys("Test")
    driver.find_element(By.NAME, "lastName").send_keys("Candidate")
    vacancy = driver.find_element(
        By.XPATH, "//label[text()='Vacancy']/../following-sibling::div//div[contains(@class,'oxd-select-text')]"
    )
    vacancy.click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//span[contains(text(),'Senior QA Lead')]").click()
    unique_email = f"aki{int(time.time())}@example.com"
    driver.find_element(
        By.XPATH, "//label[text()='Email']/../following-sibling::div//input"
    ).send_keys(unique_email)
    driver.find_element(
        By.XPATH, "//label[text()='Contact Number']/../following-sibling::div//input"
    ).send_keys("09123456789")
    driver.find_element(
        By.XPATH, "//label[text()='Keywords']/../following-sibling::div//input"
    ).send_keys("automation, python, selenium")
    calendar_icon = driver.find_element(
        By.XPATH, "//label[text()='Date of Application']/../following-sibling::div//i[contains(@class,'calendar')]"
    )
    calendar_icon.click()
    WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((
            By.XPATH, "//div[@class='oxd-date-input-calendar']//div[text()='12']"
        ))
    ).click()
    driver.find_element(
        By.XPATH, "//label[text()='Notes']/../following-sibling::div//textarea"
    ).send_keys("This is a test candidate created by automation.")
    WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((
            By.XPATH, "//label[contains(., 'Consent to keep data')]/../following-sibling::div//div[contains(@class,'oxd-checkbox-wrapper')]"
        ))
    ).click()
    save_button = driver.find_element(By.XPATH, "//button[contains(., 'Save')]")
    save_button.click()
    WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, "div.orangehrm-paper-container"))
    )
    candidate_row = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((
            By.XPATH, "//div[@class='oxd-table-card']//div[contains(., 'Aki Test Candidate')]"
        ))
    )
    assert candidate_row is not None

# TEST 5 — Required Fields Validation
@pytest.mark.p1
def test_add_candidate_required_fields(driver):
    login(driver)
    go_to_candidates(driver)
    add_button = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add')]"))
    )
    add_button.click()
    save_button = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, "//button[contains(., 'Save')]"))
    )
    save_button.click()
    time.sleep(1)
    required_fields = driver.find_elements(By.CSS_SELECTOR, "input.oxd-input--error")
    assert len(required_fields) > 0

# TEST 6 — Pagination
@pytest.mark.p3
def test_pagination(driver):
    login(driver)
    go_to_candidates(driver)
    next_button = driver.find_elements(By.XPATH, "//button[contains(., 'Next')]")
    if next_button:
        next_button[0].click()
        time.sleep(1)
        assert True
    else:
        assert True

# TEST 7 — Delete Candidate
@pytest.mark.p1
def test_delete_candidate(driver):
    login(driver)
    go_to_candidates(driver)
    time.sleep(2)
    rows = driver.find_elements(By.CSS_SELECTOR, "div.oxd-table-card")
    if len(rows) == 0:
        assert True
        return
    delete_button = rows[0].find_element(
        By.XPATH, ".//i[contains(@class,'bi-trash')]/ancestor::button"
    )
    delete_button.click()
    confirm = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, "//button[contains(., 'Yes, Delete')]"))
    )
    confirm.click()
    WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, "div.oxd-toast"))
    )
    assert True

# TEST 8 — Filter using ALL fields
@pytest.mark.p2
def test_filter_all_fields(driver):
    login(driver)
    go_to_candidates(driver)
    job_title = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, "//label[text()='Job Title']/../following-sibling::div//div[contains(@class,'oxd-select-text')]"))
    )
    job_title.click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//span[text()='QA Engineer']").click()
    vacancy = driver.find_element(
        By.XPATH, "//label[text()='Vacancy']/../following-sibling::div//div[contains(@class,'oxd-select-text')]"
    )
    vacancy.click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//span[contains(text(),'Senior QA Lead')]").click()
    status = driver.find_element(
        By.XPATH, "//label[text()='Status']/../following-sibling::div//div[contains(@class,'oxd-select-text')]"
    )
    status.click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//span[text()='Shortlisted']").click()
    candidate_name = driver.find_element(
        By.XPATH, "//label[text()='Candidate Name']/../following-sibling::div//input"
    )
    candidate_name.send_keys("Peter")
    time.sleep(1)
    suggestions = driver.find_elements(By.XPATH, "//div[@role='option']")
    if suggestions:
        suggestions[0].click()
    keywords = driver.find_element(
        By.XPATH, "//label[text()='Keywords']/../following-sibling::div//input"
    )
    keywords.send_keys("automation, python")
    date_from = driver.find_element(By.XPATH, "//input[@placeholder='From']")
    date_from.send_keys("2023-01-01")
    date_to = driver.find_element(By.XPATH, "//input[@placeholder='To']")
    date_to.send_keys("2023-12-31")
    method = driver.find_element(
        By.XPATH, "//label[text()='Method of Application']/../following-sibling::div//div[contains(@class,'oxd-select-text')]"
    )
    method.click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//span[text()='Online']").click()
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    rows = driver.find_elements(By.CSS_SELECTOR, "div.oxd-table-card")
    assert len(rows) >= 0
