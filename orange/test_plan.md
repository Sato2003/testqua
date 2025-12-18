# OrangeHRM Recruitment – Candidates & Vacancies Test Automation

## 1. Test Plan

### 1.1 Scope
This project automates functional test scenarios for the **Candidates** and **Vacancies** modules in the OrangeHRM Recruitment system.  
The goal is to validate key workflows such as:

- Navigation to Candidates and Vacancies pages  
- Search and reset operations  
- Adding candidates and vacancies  
- Validating required fields  
- Deleting candidates  
- Verifying pagination  
- Filtering by multiple criteria (job title, vacancy, hiring manager, status, other filters)  

The tests are implemented using **Python + Selenium WebDriver + Pytest** and are designed to be reusable and maintainable.

### 1.2 Objectives
- Verify that the Candidates and Vacancies modules behave correctly for core HR workflows.  
- Validate forms, dropdowns, autocomplete fields, filters, and result tables. [web:41][web:100]  
- Demonstrate stable, non‑flaky Selenium automation using explicit waits. [web:20]  
- Provide clear mapping between manual test cases and automated test functions.

### 1.3 Tools & Technologies
- **Language:** Python 3  
- **Automation Framework:** Selenium WebDriver + Pytest  
- **Browser:** Microsoft Edge (Edge WebDriver)  
- **IDE:** PyCharm  

### 1.4 Test Environment
- **URL:** https://opensource-demo.orangehrmlive.com/  
- **Browser:** Microsoft Edge  
- **OS:** Windows 11  
- **Environment:** Public demo; data and options may reset or change over time. [web:47]

### 1.5 Assumptions
- The OrangeHRM demo site is online and functional. [web:47]  
- Job titles, vacancies, and hiring managers exist in the demo data. [web:41][web:100]  
- Resume/attachment upload is supported in Vacancy details.

### 1.6 Constraints
- Demo environment performance and data can change at any time. [web:47]  
- No backend or database access.  
- Limited control over data persistence (demo resets).  

---

## 2. Test Case Design

Each test case includes:

- Clear, numbered steps  
- Expected results and assertions  
- Unique identifiers (TC‑IDs)  
- Priority (P1 = high, P2 = medium, P3 = low)  

### 2.1 Candidates Test Cases

| Test Case ID    | Description                 | Priority |
|-----------------|----------------------------|----------|
| TC‑REC‑CAN‑001  | Open Candidates Page        | P1       |
| TC‑REC‑CAN‑002  | Search Candidate            | P2       |
| TC‑REC‑CAN‑003  | Reset Search                | P3       |
| TC‑REC‑CAN‑004  | Add Candidate               | P1       |
| TC‑REC‑CAN‑005  | Required Fields Validation  | P1       |
| TC‑REC‑CAN‑006  | Pagination                  | P3       |
| TC‑REC‑CAN‑007  | Delete Candidate            | P1       |
| TC‑REC‑CAN‑008  | Filter Using All Fields     | P2       |

### 2.2 Vacancies Test Cases

| Test Case ID    | Description                             | Priority                         |
|-----------------|-----------------------------------------|----------------------------------|
| TC‑REC‑VAC‑001  | Open Vacancies Page                     | P1                               |
| TC‑REC‑VAC‑002  | Search Vacancy                          | P2                               |
| TC‑REC‑VAC‑003  | Reset Search                            | P3                               |
| TC‑REC‑VAC‑004  | Add Vacancy (+ attachment)              | P1 (XFAIL if feature is unstable)|
| TC‑REC‑VAC‑005  | Required Fields Validation              | P1                               |
| TC‑REC‑VAC‑006  | Delete Vacancy                          | P1                               |
| TC‑REC‑VAC‑007  | Pagination                              | P3                               |
| TC‑REC‑VAC‑008  | Filter Vacancies by all filters         | P2                               |

In the current code, all Candidates tests (TC‑REC‑CAN‑001…008) are implemented, and for Vacancies the main automated scenarios are **TC‑REC‑VAC‑004** (add vacancy + attachment) and **TC‑REC‑VAC‑008** (filter vacancies).

### 2.3 Choice of Scenarios
For Candidates, **Add Candidate (TC‑REC‑CAN‑004)** is the core scenario, validating:

1. Opening the Add Candidate form  
2. Filling required fields with valid data  
3. Saving the candidate record  
4. Seeing the new candidate listed in the table  

For Vacancies, **Add Vacancy (TC‑REC‑VAC‑004)** and **Filter Vacancies (TC‑REC‑VAC‑008)** cover vacancy creation and multi‑filter searching, which are central to the recruitment process. [web:41][web:100]

---

## 3. Selenium WebDriver Implementation

### 3.1 Correct WebDriver Usage
- A shared Pytest fixture `driver()` creates a Microsoft Edge WebDriver instance, maximizes the window, and opens the OrangeHRM login URL. [web:70][web:74]  
- The fixture uses `yield` and calls `driver.quit()` after each test for clean teardown. [web:66]  
- Tests use **explicit waits** (`WebDriverWait` + `expected_conditions`) to synchronize interactions with page elements (inputs, buttons, dropdowns, tables, toasts) instead of relying solely on `time.sleep`. [web:20][web:23]  
- Locators are based on visible labels, semantic XPaths, and CSS selectors for table structures.

### 3.2 Stability & Reliability
- Unique candidate emails and vacancy names are generated with timestamps to avoid data collisions in the demo environment.  
- Navigation helpers (`go_to_candidates`, `go_to_vacancies`) always bring the browser into a known state before actions.  
- Tests wait for page headers, table bodies, and toast notifications before asserting, reducing flakiness. [web:51]

### 3.3 Best Practices
- Reusable helpers:
  - Shared: `login`, `select_filter_option`  
  - Candidates: `go_to_candidates`  
  - Vacancies: `go_to_vacancies`, `create_vacancy`, `search_vacancy`, `open_vacancy`, `add_attachment`  
- One logical scenario per `test_*` function; tests do not call each other.  
- Type hints (`WebElement`) are used on helper return variables to improve readability and IDE support.  
- Only known unstable flows (Vacancies on demo) are wrapped in limited exception handling or can be later marked as `xfail` with reasons.

---

## 4. Pytest Framework Implementation

### 4.1 Use of Fixtures
- A central `driver()` fixture in the test module handles browser setup and teardown for every test. [web:66]  
- Each test starts from the login page, logs in using `login(driver)`, and then navigates to the relevant module.

### 4.2 Structure & Organization
- Test file is named `test_*.py` and uses functions named `test_*`.  
- Custom markers are used:
  - `@pytest.mark.recruitment` at module level to tag the suite  
  - `@pytest.mark.p1`, `@pytest.mark.p2`, `@pytest.mark.p3` for test priority grouping [web:81]  
- Tests are independent and reuse helpers instead of sharing state.

Example commands:
- pytest -v -m recruitment
- pytest -v -m "recruitment and p1"

### 4.3 Execution & Parametrization
- Separate tests exist for each Candidate scenario (open, search, reset, add, required fields, pagination, delete, filter).  
- Vacancies tests cover end‑to‑end add vacancy with attachment and multi‑filter search. [web:100]  
- Parametrization is used for searching candidates by multiple names (e.g., `["Peter", "Linda"]`), and can be extended to more data sets later.

---

## 5. Assertions, Reporting & Logging

### 5.1 Assertions
Candidates tests assert:

- URL path and presence of the Candidates page header.  
- Visibility of the Candidates table after navigation and search.  
- Presence of newly added candidate rows in the table using name/email.  
- Required‑field validation by checking inputs marked with error classes.  
- Pagination behavior via interaction with Next (if present).  
- Successful delete flows via confirmation dialog and success toast.

Vacancies tests assert:

- Newly created vacancies appear in the Vacancies table when searched by name.  
- Attachment upload completes and success toast appears for vacancy details. [web:13][web:51]  
- Filtered Vacancies table loads when Job Title, Vacancy, Hiring Manager, and Status filters are applied.

### 5.2 Reporting Tools
To enhance reporting:

- Integrate `pytest-html` to generate HTML test reports, for example: [web:22][web:28]  
- pytest -v --html=report.html --self-contained-html
- Optionally add `pytest-reportlog` or similar plugins to capture machine‑readable logs. [web:25]  
- Capture screenshots on failures and attach them to HTML reports for easier debugging.

### 5.3 Logging & Error Handling
- Python’s `logging` module is configured at the top of the test file and used in helpers (for example, logging “Navigating to Candidates page”).  
- Logs provide traceability for major actions:
- Logging in as Admin  
- Navigating to Candidates or Vacancies pages  
- Creating candidates/vacancies  
- Applying filters  
- Deleting candidates  
- Broad exception handling has been avoided in most tests so genuine failures are visible; any future `xfail` usage should be explicit and limited.

---

## 6. Summary

This automation project validates the core **Candidates** and **Vacancies** workflows in the OrangeHRM Recruitment module using **Selenium WebDriver + Pytest** against the public demo site. [web:47][web:51]  
The combined suite follows QA best practices: shared fixtures, reusable helpers, explicit waits, clear test IDs and priorities, and a structure ready for HTML reporting and CI integration.

---
**Project Name:** OrangeHRM Candidates  
**Module:** Candidates page  
**Created By:** AKi SATO KATO  
**Date:** December 14, 2025  
**Test Framework:** Python + Selenium + Pytest  
**Demo URL:** https://opensource-demo.orangehrmlive.com/ [web:47]
---
