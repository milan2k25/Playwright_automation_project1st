# Quick Setup Guide - example Playwright Framework

## 🚀 Quick Start (5 Minutes)

### Step 1: Navigate to Project Directory
```powershell
cd "D:\Automation Project\Test_Env\example_qa_playwright"
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Install Playwright Browsers
```powershell
playwright install
```

### Step 4: Run Tests
```powershell
cd test_demo
pytest test_example_bank_statement.py --browser_name chrome -v
```

## ✅ Verify Installation

Run this command to check if everything is installed:
```powershell
playwright --version
python -c "import playwright; print('Playwright imported successfully')"
```

## 🎯 First Test Run

```powershell
# Navigate to test_demo folder
cd test_demo

# Run a single test
pytest test_example_bank_statement.py::TestBankStatement::test_verify_bank_statement_side_bar_expanded --browser_name chrome -v
```

## 📊 View Reports

After running tests, open:
- `report/report.html` - Pytest HTML Report
- `report/dashboard.html` - Custom Dashboard (after running dashboard_generator.py)

## 🔧 Configuration

Update `config.json` with your environment details:
```json
{
  "dev_url": "https://your-app-url.com",
  "dev_login": {
    "email": "your-email@example.com",
    "password": "your-password"
  }
}
```

## 🐛 Troubleshooting

### Issue: "playwright not found"
**Solution:**
```powershell
pip install playwright
playwright install
```

### Issue: "No module named 'interface'"
**Solution:**
```powershell
pip install python-interface
```

### Issue: "No test data found"
**Solution:** 
Ensure `testdata/bank_statement/` folder contains PDF files

### Issue: "Browser not launching"
**Solution:**
```powershell
playwright install chromium
playwright install firefox
playwright install webkit
```

## 📝 Next Steps

1. ✅ Framework is ready to use!
2. Add more test files to `testdata/bank_statement/`
3. Customize `config.json` for your environment
4. Extend tests in `test_example_bank_statement.py`
5. Run tests with different browsers (chrome, firefox, edge, webkit)

## 🎓 Key Commands Reference

```powershell
# Run all tests
pytest test_example_bank_statement.py --browser_name chrome -v

# Run with Firefox
pytest test_example_bank_statement.py --browser_name firefox -v

# Run with Edge
pytest test_example_bank_statement.py --browser_name edge -v

# Run with WebKit (Safari engine)
pytest test_example_bank_statement.py --browser_name webkit -v

# Run specific test class
pytest test_example_bank_statement.py::TestBankStatement -v

# Run using batch script (from root directory)
run_tests.bat
```

## 🏆 Success Indicators

✅ All dependencies installed  
✅ Playwright browsers installed  
✅ Test execution successful  
✅ Reports generated in `report/` folder  
✅ No import errors  

---

**You're all set! Happy Testing! 🎉**
