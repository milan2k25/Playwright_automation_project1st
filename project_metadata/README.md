# InferIQ Automation - Playwright Framework

Selenium-based test automation framework migrated to Playwright for improved stability and reliability.

## Framework Architecture

- **Language**: Python 3.x
- **Automation Tool**: Playwright (Sync API)
- **Test Framework**: Pytest
- **Design Pattern**: Page Object Model (POM) with Interface + Factory Pattern
- **Reporting**: JUnit XML + HTML + Custom Interactive Dashboard

## Folder Structure

```
inferiq_qa_playwright/
├── config.json                    # Environment Configuration
├── dashboard_generator.py         # Custom Dashboard Generator
├── README.md
├── run_tests.bat                  # Test Execution Script
│
├── core/                          # Driver Factory
│   └── playwright_manager.py      # Interface + Factory Pattern
│
├── pages/                         # Page Object Model
│   ├── login_page.py
│   ├── home_page.py
│   └── bank_statement_page.py
│
├── locators/                      # Centralized Locators
│   ├── login_page_locators.py
│   ├── home_page_locators.py
│   └── bank_statemenet_page_locators.py
│
├── helper/                        # Playwright Wrapper Functions
│   └── playwright_helper.py
│
├── utility/                       # Utility Functions
│   └── utils.py
│
├── test_demo/                     # Test Suite
│   ├── conftest.py                # Pytest Configuration
│   ├── pytest.ini
│   ├── data/                      # JSON Test Data
│   └── test_inferIQ_bank_statement.py
│
├── testdata/                      # Test Files (PDFs, Images)
│   └── bank_statement/
│
└── report/                        # Test Reports
    ├── report.xml
    ├── report.html
    └── dashboard.html
```

## Key Features

✅ **Multi-Browser Support**: Chrome, Firefox, Edge, WebKit  
✅ **Interface + Factory Pattern**: Consistent with original Selenium framework  
✅ **Playwright Auto-Waiting**: No explicit waits needed, reduced flakiness  
✅ **Modular Architecture**: Easy to maintain and extend  
✅ **Data-Driven Testing**: JSON format test data  
✅ **Custom Dashboard**: Interactive HTML report with test steps  
✅ **Async-Ready**: Structure supports future async implementation  

## Installation

### 1. Install Python Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Install Playwright Browsers

```powershell
playwright install
```

## Execution

### Run All Tests

```powershell
# Chrome (default)
pytest --browser_name chrome -v

# Firefox
pytest --browser_name firefox -v

# Edge
pytest --browser_name edge -v

# WebKit
pytest --browser_name webkit -v
```

### Run Specific Test File

```powershell
pytest test_demo/test_inferIQ_bank_statement.py --browser_name chrome -v
```

### Run Specific Test Function

```powershell
pytest test_demo/test_inferIQ_bank_statement.py::TestBankStatement::test_verify_bank_statement_side_bar_expanded --browser_name chrome -v
```

### Using Batch Script

```powershell
run_tests.bat
```

## Reports

After execution, reports are generated in the `report/` folder:

1. **report.xml** - JUnit XML format (CI/CD compatible)
2. **report.html** - Pytest HTML report
3. **dashboard.html** - Custom interactive dashboard

## Configuration

### Environment Setup (`config.json`)

```json
{
  "dev_url": "https://dev.inferiq.com",
  "dev_login": {
    "email": "user@example.com",
    "password": "password"
  }
}
```

### Pytest Configuration (`pytest.ini`)

```ini
[pytest]
addopts = --strict-markers --junitxml=report/report.xml -ra -v -s --html=report/report.html
markers =
    test_details
    slow
    smoke
    regression
```

## Differences from Selenium Version

| Feature | Selenium | Playwright |
|---------|----------|------------|
| **Driver Management** | `pytest.driver` | `pytest.page` |
| **Element Interaction** | `driver.find_element().click()` | `page.locator().click()` |
| **Waits** | Explicit WebDriverWait | Auto-wait (built-in) |
| **File Upload** | `send_keys(filepath)` | `set_input_files(filepath)` |
| **Downloads** | Manual handling | `expect_download()` context |
| **Text Content** | `.text` | `.text_content()` |
| **Checked Status** | `.is_selected()` | `.is_checked()` |
| **Fill Input** | `.send_keys()` | `.fill()` |

## Async Support (Future)

The framework is structured to support async operations in the future without major refactoring:

1. Add `async_playwright_helper.py` with async methods
2. Update page objects to use async/await
3. Add async fixtures in conftest.py
4. No framework structure changes needed!

## Test Coverage

- **Bank Statement Module**: 10+ test cases
  - Sidebar functionality
  - Tab navigation
  - File upload
  - History verification
  - Search functionality
  - File processing status

## Advantages Over Selenium

1. **Built-in Auto-Waiting**: Reduces test flakiness
2. **Faster Execution**: More efficient browser communication
3. **Better Debugging**: Screenshots, videos, trace viewer
4. **Network Interception**: Easy API mocking/monitoring
5. **WebKit Support**: Test on Safari engine
6. **No Driver Management**: No ChromeDriver, GeckoDriver needed

## Troubleshooting

### Issue: Browsers not installed
```powershell
playwright install
```

### Issue: Module not found
```powershell
pip install -r requirements.txt
```

### Issue: Test data not found
Ensure `testdata/bank_statement/` contains PDF files

## Maintainer

InferIQ QA Team

## License

Proprietary
