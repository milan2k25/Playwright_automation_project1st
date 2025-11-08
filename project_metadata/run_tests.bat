@echo off
REM example Playwright Test Automation - Batch Execution Script
REM Author: QA Team
REM Description: Runs all bank statement tests and generates dashboard

echo ================================================
echo   example Test Automation - Playwright
echo ================================================
echo.

REM Navigate to test_demo directory
cd test_demo

REM Run pytest with Chrome browser
echo Running tests with Chrome browser...
pytest test_example_bank_statement.py --browser_name chrome -v

REM Go back to root directory
cd ..

REM Generate dashboard
echo.
echo Generating dashboard report...
python dashboard_generator.py

echo.
echo ================================================
echo   Test Execution Complete!
echo   Reports available in: report/
echo     - report.xml (JUnit)
echo     - report.html (Pytest HTML)
echo     - dashboard.html (Custom Dashboard)
echo ================================================
echo.

pause
