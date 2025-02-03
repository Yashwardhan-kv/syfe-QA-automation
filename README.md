# Syfe QA Automation

## Overview
This project is an automated testing framework for Syfe's web application using Selenium and Pytest. It includes test cases for login, inventory management, cart operations, and checkout workflows on the SauceDemo website.

## Technologies Used
- Python
- Selenium WebDriver
- Pytest
- WebDriver Manager

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/Yashwardhan-kv/syfe-qa-automation.git
   ```
2. Navigate to the project directory:
   ```sh
   cd syfe-qa-automation
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running Tests
To execute all test cases, run:
```sh
pytest
```
For detailed logs, run:
```sh
pytest -v
```

## Project Structure
```
syfe-qa-automation/
│── /pages                  # Page Object Model (POM) classes
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   ├── checkout_page.py
│── /tests                  # Test scripts
│   ├── test_sauce_demo.py
│── .github/workflows       # GitHub Actions for CI/CD
│   ├── selenium-ci.yml
│── Jenkinsfile             # Jenkins Pipeline script
│── config.py               # Configurations for test data
│── conftest.py             # Pytest setup
│── requirements.txt        # Dependencies
│── README.md               # Instructions

```
## script contains all six tasks as mentioned
-Login Validation ✅
-Add Items to Cart from Inventory Page ✅
-Add Items to Cart from Inventory Item Page ✅
-Remove Items from Cart ✅
-Checkout Workflow ✅
-Logout Functionality ✅

## Features
- Automated UI testing for login, cart, and checkout functionalities.
- Uses Selenium WebDriver for browser automation.
- Pytest integration for test execution and reporting.
- Custom logging for test results (PASS/FAIL indicators).

## Contributing
Feel free to submit issues and pull requests to enhance the project.

## License
This project is licensed under the MIT License.

## Google Drive
[DRIVE](https://drive.google.com/drive/folders/1LhdurgTM3M_WjJlSqSioR3gIYxdFfpyg?usp=sharing)
