# OrangeHRM Recruitment – Candidates Automation (Selenium + Pytest)

## Prerequisites

- Python 3.x
- Microsoft Edge browser installed
- Edge WebDriver matching your Edge version
- pip

## Setup


(Include in `requirements.txt`: selenium, pytest, pytest-html, pytest-reportlog.)

## Running Tests

Basic run (all tests):
pytest -v

Run only Recruitment (OrangeHRM) tests:
pytest -v -m recruitment

Run all tests and generate an HTML report:
pytest -v --html=report.html --self-contained-html

Generate HTML report:


## Test Scope

This suite covers:

- Open Candidates page
- Search candidate
- Reset search
- Add candidate
- Required fields validation
- Pagination
- Delete candidate
- Filter using all fields
