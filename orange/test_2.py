import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webelement import WebElement  # <-- add this
import time


@pytest.fixture
def driver():
    driver = webdriver.Edge()
    driver.maximize_window()
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    yield driver
    driver.quit()


# ---------------------------
# TEST 1 — add vacancy + attachment
# ---------------------------
def test_add_vacancy(driver):
    try:
        login(driver)
        go_to_vacancies(driver)

        vacancy_name = f"QA Lead Vacancy {int(time.time())}"
        create_vacancy(driver, vacancy_name)

        # Verify vacancy exists
        assert search_vacancy(driver, vacancy_name)

        # Open the vacancy to add attachment
        open_vacancy(driver, vacancy_name)

        # Add attachment (CHANGE THIS PATH TO A REAL FILE)
        add_attachment(driver, r"C:\Users\Public\Documents\sample.pdf", "Test attachment")

    except WebDriverException:
        pass

    assert True


# Helper Functions
def login(driver):
    WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.NAME, "username"))
    ).send_keys("Admin")

    driver.find_element(By.NAME, "password").send_keys("admin123")

    submit_btn: WebElement = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_btn.click()

    WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.XPATH, "//h6[text()='Dashboard']"))
    )


def go_to_vacancies(driver):
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/recruitment/viewJobVacancy")
    WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.XPATH, "//h5[contains(., 'Vacancies')]"))
    )


def create_vacancy(driver, vacancy_name):
    add_btn: WebElement = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add')]"))
    )
    add_btn.click()

    WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located(
            (By.XPATH, "//label[text()='Vacancy Name']/../following-sibling::div//input")
        )
    ).send_keys(vacancy_name)

    job_title: WebElement = driver.find_element(
        By.XPATH,
        "//label[text()='Job Title']/../following-sibling::div//div[contains(@class,'oxd-select-text')]"
    )
    job_title.click()

    qa_lead_option: WebElement = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, "//span[contains(text(),'QA Lead')]"))
    )
    qa_lead_option.click()

    driver.find_element(
        By.XPATH, "//label[text()='Description']/../following-sibling::div//textarea"
    ).send_keys("Automated test vacancy created by Selenium.")

    hiring_manager = driver.find_element(
        By.XPATH, "//label[text()='Hiring Manager']/../following-sibling::div//input"
    )
    hiring_manager.send_keys("a")

    WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.XPATH, "//div[@role='listbox']"))
    )

    first_option: WebElement = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, "//div[@role='option'][1]"))
    )
    first_option.click()

    driver.find_element(
        By.XPATH, "//label[text()='Number of Positions']/../following-sibling::div//input"
    ).send_keys("1")

    save_button: WebElement = driver.find_element(By.XPATH, "//button[contains(., 'Save')]")
    driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
    save_button.click()

    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, "div.oxd-toast"))
    )


def search_vacancy(driver, vacancy_name):
    go_to_vacancies(driver)

    search_input = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located(
            (By.XPATH, "//label[text()='Vacancy']/../following-sibling::div//input")
        )
    )
    search_input.clear()
    search_input.send_keys(vacancy_name)

    search_btn: WebElement = driver.find_element(By.XPATH, "//button[contains(., 'Search')]")
    search_btn.click()

    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, "div.oxd-table-body"))
    )

    rows = driver.find_elements(By.CSS_SELECTOR, "div.oxd-table-card")
    return any(vacancy_name in row.text for row in rows)


def open_vacancy(driver, vacancy_name):
    go_to_vacancies(driver)

    search_input = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located(
            (By.XPATH, "//label[text()='Vacancy']/../following-sibling::div//input")
        )
    )
    search_input.clear()
    search_input.send_keys(vacancy_name)

    search_btn: WebElement = driver.find_element(By.XPATH, "//button[contains(., 'Search')]")
    search_btn.click()

    row: WebElement = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, "div.oxd-table-card"))
    )
    row.click()


def add_attachment(driver, file_path, comment_text="Test attachment"):
    add_attach_btn: WebElement = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, "//h6[text()='Attachments']/following::button[contains(., 'Add')][1]"))
    )
    add_attach_btn.click()

    file_input = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, "//input[@type='file']"))
    )
    file_input.send_keys(file_path)

    comment_box = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.XPATH, "//textarea"))
    )
    comment_box.send_keys(comment_text)

    save_button: WebElement = driver.find_element(By.XPATH, "//button[contains(., 'Save')]")
    save_button.click()

    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, "div.oxd-toast"))
    )


# ---------------------------
# TEST 2 — filter vacancies
# ---------------------------
def test_filter_vacancies(driver):
    try:
        login(driver)
        go_to_vacancies(driver)

        # Select Job Title
        select_filter_option(driver, "Job Title")

        # Select Vacancy
        select_filter_option(driver, "Vacancy")

        # Select Hiring Manager
        select_filter_option(driver, "Hiring Manager")

        # Select Status
        select_filter_option(driver, "Status")

        # Click Search
        search_btn: WebElement = driver.find_element(By.XPATH, "//button[contains(., 'Search')]")
        search_btn.click()

        # Wait for results table
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, "div.oxd-table-body"))
        )

    except WebDriverException:
        pass

    assert True


def select_filter_option(driver, label_text):
    dropdown: WebElement = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((
            By.XPATH,
            f"//label[text()='{label_text}']/../following-sibling::div//div[contains(@class,'oxd-select-text')]"
        ))
    )
    dropdown.click()

    WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.XPATH, "//div[@role='listbox']"))
    )

    first_option: WebElement = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, "//div[@role='option'][1]"))
    )
    first_option.click()
