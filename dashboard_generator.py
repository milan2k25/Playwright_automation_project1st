#!/usr/bin/env python3
"""
InferIQ Test Dashboard Generator
================================
Parses pytest XML results and generates an attractive HTML dashboard
showing module-wise test statistics.

Author: InferIQ QA Team
"""

import xml.etree.ElementTree as ET
import os
from datetime import datetime
from collections import defaultdict
import json
import base64

class TestDashboardGenerator:
    
    def __init__(self, xml_file_path="report/old_report.xml", output_path="report/dashboard.html"):
        self.xml_file_path = xml_file_path
        self.output_path = output_path
        self.test_data = defaultdict(lambda: {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'errors': 0,
            'duration': 0.0,
            'tests': []
        })
        
    def parse_xml_results(self):
        """Parse the pytest XML file and extract test results"""
        try:
            if not os.path.exists(self.xml_file_path):
                print(f"XML file not found: {self.xml_file_path}")
                print("Make sure to run pytest first to generate the XML report")
                return False
                
            tree = ET.parse(self.xml_file_path)
            root = tree.getroot()
            
            print(f"📊 Parsing XML results from: {self.xml_file_path}")
            
            # Handle both testsuite and testsuites root elements
            testsuites = root.findall('.//testsuite') if root.tag == 'testsuites' else [root]
            
            for testsuite in testsuites:
                for testcase in testsuite.findall('testcase'):
                    self._process_testcase(testcase)
                    
            return True
            
        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False
    
    def _process_testcase(self, testcase):
        """Process individual test case and extract module information"""
        classname = testcase.get('classname', '')
        test_name = testcase.get('name', '')
        duration = float(testcase.get('time', 0))
        
        # Extract module name from classname (e.g., test_demo.test_inferIQ_bank_statement.TestBankStatement)
        module_name = self._extract_module_name(classname)
        
        # Determine test status
        status = self._determine_test_status(testcase)
        
        # Update module statistics
        module_data = self.test_data[module_name]
        module_data['total'] += 1
        module_data['duration'] += duration
        module_data[status] += 1
        
        # Store individual test details
        test_info = {
            'name': self._format_test_name(test_name),
            'raw_name': test_name,  # Keep original name for reference
            'status': status,
            'duration': duration,
            'classname': classname
        }
        
        # Add failure/error message if present
        failure = testcase.find('failure')
        error = testcase.find('error')
        if failure is not None:
            test_info['message'] = failure.get('message', '')[:200] + '...' if len(failure.get('message', '')) > 200 else failure.get('message', '')
        elif error is not None:
            test_info['message'] = error.get('message', '')[:200] + '...' if len(error.get('message', '')) > 200 else error.get('message', '')
        
        # Extract test steps from docstring
        test_steps = self._extract_test_steps(classname, test_name)
        if test_steps:
            test_info['steps'] = test_steps
        
        module_data['tests'].append(test_info)
    
    def _extract_module_name(self, classname):
        """Extract readable module name from test classname"""
        if not classname:
            return "Unknown Module"
            
        # Split by dots and get the test file name
        parts = classname.split('.')
        if len(parts) >= 2:
            test_file = parts[-2]  # e.g., test_inferIQ_bank_statement
            
            # Convert test file name to readable module name
            if 'bank_statement' in test_file.lower():
                return "Bank Statement Extraction Testcases"
            elif 'cash_flow' in test_file.lower():
                return "Cash Flow Analysis"
            elif 'classification' in test_file.lower():
                return "Classification"
            elif 'extraction' in test_file.lower():
                return "Extraction"
            elif 'redaction' in test_file.lower():
                return "Redaction"
            elif 'rent_roll' in test_file.lower():
                return "Rent Roll"
            elif 'conversational_ai' in test_file.lower() or 'con_ai' in test_file.lower():
                return "Conversational AI"
            else:
                # Fallback: clean up the test file name
                return test_file.replace('test_inferIQ_', '').replace('_', ' ').title()
        
        return "Unknown Module"
    
    def _get_module_description(self, module_name):
        """Get descriptive text for each module"""
        descriptions = {
            "Bank Statement Extraction Testcases": "Tests complete workflow: Navigation, File upload with page selection, Processing status tracking, Support portal verification with date/time validation, File submission, and Downloadable Excel output in ZIP format",
            "Cash Flow Analysis": "Tests portfolio creation, File upload workflow, File processing status, and Analysis features",
            "Classification": "Tests document classification for multiple document types and file format validations",
            "Conversational AI": "Tests AI-powered document interaction with chat-based extraction features",
            "Extraction": "Tests data extraction from various document types in multiple file formats",
            "Redaction": "Tests PII redaction and masking for sensitive data across multiple file formats",
            "Rent Roll": "Tests rent roll document upload, AI model selection, and output verification"
        }
        return descriptions.get(module_name, "")
    
    def _determine_test_status(self, testcase):
        """Determine the status of a test case"""
        if testcase.find('failure') is not None:
            return 'failed'
        elif testcase.find('error') is not None:
            return 'errors'
        elif testcase.find('skipped') is not None:
            return 'skipped'
        else:
            return 'passed'
    
    def _format_test_name(self, test_name):
        """Format test name to be more readable by removing test_ prefix and converting underscores to spaces"""
        if not test_name:
            return "Unknown Test"
        
        # Remove 'test_' prefix if present
        formatted_name = test_name
        if formatted_name.startswith('test_'):
            formatted_name = formatted_name[5:]  # Remove 'test_' prefix
        
        # Replace underscores with spaces
        formatted_name = formatted_name.replace('_', ' ')
        
        # Convert to title case for better readability
        formatted_name = formatted_name.title()
        
        # Fix some common abbreviations and terms that should be uppercase
        replacements = {
            'Ai': 'AI',
            'Api': 'API',
            'Url': 'URL',
            'Http': 'HTTP',
            'Pdf': 'PDF',
            'Json': 'JSON',
            'Xml': 'XML',
            'Csv': 'CSV',
            'Id': 'ID',
            'Qa': 'QA',
            'Ui': 'UI',
            'Bs': 'Bank Statement Extraction Testcases',
            'Inferiq': 'InferIQ'
        }
        
        for old, new in replacements.items():
            formatted_name = formatted_name.replace(old, new)
        
        return formatted_name
    
    def _extract_test_steps(self, classname, test_name):
        """Extract test steps from test file docstring"""
        try:
            # Parse classname to get test file path
            # e.g., test_demo.test_inferIQ_bank_statement.TestBankStatement
            if not classname:
                print(f"  ⚠️  No classname for {test_name}")
                return ""
            
            parts = classname.split('.')
            if len(parts) < 2:
                print(f"  ⚠️  Invalid classname format: {classname}")
                return ""
            
            # Get test file name
            # Format can be either:
            # - test_inferIQ_bank_statement.TestBankStatement (2 parts)
            # - test_demo.test_inferIQ_bank_statement.TestBankStatement (3 parts)
            if len(parts) == 2:
                # Format: test_inferIQ_bank_statement.TestBankStatement
                test_file = parts[0]  # test_inferIQ_bank_statement
                test_dir = "test_demo"  # Default directory
            else:
                # Format: test_demo.test_inferIQ_bank_statement.TestBankStatement
                test_dir = parts[0]  # test_demo
                test_file = parts[1]  # test_inferIQ_bank_statement
            
            # Construct file path
            test_file_path = os.path.join(test_dir, f"{test_file}.py")
            
            print(f"  🔍 Looking for: {test_file_path} -> {test_name}")
            
            if not os.path.exists(test_file_path):
                print(f"  ❌ File not found: {test_file_path}")
                return ""
            
            # Read the file and find the test function
            with open(test_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find the test function definition
            function_pattern = f"def {test_name}("
            if function_pattern not in content:
                return ""
            
            # Extract the docstring
            start_idx = content.find(function_pattern)
            if start_idx == -1:
                return ""
            
            # Find the docstring (look for ''' or """)
            docstring_start = content.find("'''", start_idx)
            if docstring_start == -1:
                docstring_start = content.find('"""', start_idx)
                if docstring_start == -1:
                    return ""
                quote_type = '"""'
            else:
                quote_type = "'''"
            
            # Find the end of docstring
            docstring_end = content.find(quote_type, docstring_start + 3)
            if docstring_end == -1:
                return ""
            
            # Extract docstring content
            docstring = content[docstring_start + 3:docstring_end].strip()
            
            # Extract only the "Steps:" section
            if "Steps:" in docstring or "steps:" in docstring:
                # Find Steps section
                steps_start = docstring.lower().find("steps:")
                if steps_start != -1:
                    steps_content = docstring[steps_start + 6:].strip()
                    # Clean up and format steps
                    steps_lines = [line.strip() for line in steps_content.split('\n') if line.strip()]
                    
                    # Remove leading numbers, hyphens, and clean up each step
                    cleaned_steps = []
                    for step in steps_lines:
                        # Remove leading "1.", "2.", etc. or "1 ", "2 ", or "- "
                        step = step.lstrip('0123456789.-) ').strip()
                        if step:  # Only add non-empty steps
                            cleaned_steps.append(step)
                    
                    # Format as numbered list with HTML line breaks
                    formatted_steps = '<br/>'.join([f"{i+1}. {step}" for i, step in enumerate(cleaned_steps)])
                    print(f"  ✅ Extracted steps for {test_name}")
                    return formatted_steps
            
            print(f"  ⚠️  No steps found in docstring for {test_name}")
            return ""
            
        except Exception as e:
            print(f"Error extracting steps for {test_name}: {e}")
            return ""
    
    def _calculate_success_rate(self, module_data):
        """Calculate success rate for a module"""
        total = module_data['total']
        if total == 0:
            return 0
        return round((module_data['passed'] / total) * 100, 1)
    
    def _get_status_color(self, success_rate):
        """Get color based on success rate"""
        if success_rate >= 90:
            return "success"  # Green
        elif success_rate >= 70:
            return "warning"  # Yellow
        else:
            return "danger"   # Red
    
    def generate_dashboard(self):
        """Generate the HTML dashboard"""
        if not self.parse_xml_results():
            return False
            
        print(f"🎨 Generating dashboard...")
        
        # Calculate overall statistics
        overall_stats = self._calculate_overall_stats()
        
        # Generate HTML content
        html_content = self._generate_html_template(overall_stats)
        
        # Ensure report directory exists
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        
        # Write HTML file
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✅ Dashboard generated successfully: {self.output_path}")
            return True
        except Exception as e:
            print(f"Error writing dashboard file: {e}")
            return False
    
    def _get_logo_base64(self):
        """Convert logo image to base64 for embedding in HTML"""
        logo_path = os.path.join(os.path.dirname(self.output_path), "logo.png")
        
        try:
            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as img_file:
                    img_data = img_file.read()
                    base64_data = base64.b64encode(img_data).decode('utf-8')
                    return f"data:image/png;base64,{base64_data}"
            else:
                print(f"Logo file not found at: {logo_path}")
                return ""
        except Exception as e:
            print(f"Error reading logo file: {e}")
            return ""
    
    def _calculate_overall_stats(self):
        """Calculate overall test statistics"""
        total_tests = sum(module['total'] for module in self.test_data.values())
        total_passed = sum(module['passed'] for module in self.test_data.values())
        total_failed = sum(module['failed'] for module in self.test_data.values())
        total_skipped = sum(module['skipped'] for module in self.test_data.values())
        total_errors = sum(module['errors'] for module in self.test_data.values())
        total_duration = sum(module['duration'] for module in self.test_data.values())
        
        success_rate = round((total_passed / total_tests * 100), 1) if total_tests > 0 else 0
        
        return {
            'total': total_tests,
            'passed': total_passed,
            'failed': total_failed,
            'skipped': total_skipped,
            'errors': total_errors,
            'duration': round(total_duration, 2),
            'success_rate': success_rate,
            'modules_count': len(self.test_data)
        }
    
    def _generate_html_template(self, overall_stats):
        """Generate the complete HTML dashboard"""
        
        # Generate module cards HTML
        module_cards_html = self._generate_module_cards()
        
        # Get logo as base64 for embedding
        logo_base64 = self._get_logo_base64()

        # Get current timestamp in DD-MM-YYYY format with 12-hour time
        timestamp = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
        
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Automation Test Report</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #1e3c72 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        .dashboard-container {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            margin: 20px;
            padding: 30px;
        }}
        
        .header-section {{
            position: relative;
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            border-radius: 15px;
            color: white;
            box-shadow: 0 10px 30px rgba(30, 60, 114, 0.4);
        }}
        
        .header-logo {{
            position: absolute;
            left: 30px;
            top: 50%;
            transform: translateY(-50%);
            max-width: 280px;
            max-height: 190px;
            object-fit: contain;
        }}
        
        .header-content {{
            margin-left: 140px;
        }}
        
        .header-section h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }}
        
        .header-section .subtitle {{
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 0;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .stat-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            border: none;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        }}
        
        .stat-icon {{
            font-size: 2.5rem;
            margin-bottom: 15px;
        }}
        
        .stat-number {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .modules-section {{
            margin-top: 40px;
        }}
        
        .section-title {{
            font-size: 1.7rem;
            font-weight: 600;
            margin-bottom: 30px;
            color: #333;
            text-align: center;
        }}
        
        .module-card {{
            background: white;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            border: none;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .module-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        }}
        
        .module-header {{
            padding: 25px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .module-name {{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        
        .module-description {{
            font-size: 1rem;
            font-weight: 400;
            line-height: 1.6;
            margin-bottom: 15px;
            opacity: 0.95;
            padding: 8px 12px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            border-left: 3px solid rgba(255, 255, 255, 0.4);
        }}
        
        .module-summary {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }}
        
        .module-stats {{
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }}
        
        .module-stat {{
            text-align: center;
        }}
        
        .module-stat-number {{
            font-size: 1.5rem;
            font-weight: 700;
        }}
        
        .module-stat-label {{
            font-size: 0.8rem;
            opacity: 0.9;
        }}
        
        .success-badge {{
            background: rgba(255, 255, 255, 0.2);
            border-radius: 25px;
            padding: 8px 20px;
            font-weight: 600;
            font-size: 1.1rem;
        }}
        
        .module-body {{
            padding: 25px;
        }}
        
        .progress-container {{
            margin-bottom: 20px;
        }}
        
        .progress {{
            height: 12px;
            border-radius: 10px;
            background-color: #f8f9fa;
        }}
        
        .progress-bar {{
            border-radius: 10px;
        }}
        
        .test-details {{
            margin-top: 20px;
        }}
        
        .test-item-container {{
            border-bottom: 1px solid #eee;
        }}
        
        .test-item-container:last-child {{
            border-bottom: none;
        }}
        
        .test-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 8px;
            transition: background-color 0.2s ease;
        }}
        
        .test-item:hover {{
            background-color: #f8f9fa;
        }}
        
        .test-name-container {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .test-name {{
            font-weight: 500;
        }}
        
        .collapse-icon {{
            color: #667eea;
            font-size: 0.8rem;
            transition: transform 0.3s ease;
        }}
        
        .collapse-icon.rotated {{
            transform: rotate(90deg);
        }}
        
        .test-steps-collapse {{
            overflow: hidden;
            transition: max-height 0.3s ease;
        }}
        
        .test-steps-content {{
            padding: 15px 15px 15px 35px;
            background-color: #f8f9fa;
            border-left: 3px solid #667eea;
            margin: 5px 0 10px 0;
        }}
        
        .steps-list {{
            margin-top: 10px;
            line-height: 1.8;
            color: #555;
        }}
        
        .test-status {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .status-badge {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }}
        
        .status-passed {{
            background-color: #d4edda;
            color: #155724;
        }}
        
        .status-failed {{
            background-color: #f8d7da;
            color: #721c24;
        }}
        
        .status-skipped {{
            background-color: #fff3cd;
            color: #856404;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #666;
            font-size: 0.9rem;
        }}
        
        .text-success {{ color: #28a745 !important; }}
        .text-warning {{ color: #ffc107 !important; }}
        .text-danger {{ color: #dc3545 !important; }}
        .text-info {{ color: #17a2b8 !important; }}
        .text-secondary {{ color: #6c757d !important; }}
        
        /* Large/Ultra-wide Laptops (17+ inch, 2560x1440 or higher) */
        @media (min-width: 2000px) {{
            .dashboard-container {{
                max-width: 2200px;
                margin: 30px auto;
            }}
            
            .header-section h1 {{
                font-size: 3rem;
            }}
            
            .header-section .subtitle {{
                font-size: 1.4rem;
            }}
            
            .stat-number {{
                font-size: 3rem;
            }}
            
            .stat-icon {{
                font-size: 3rem;
            }}
        }}
        
        /* Small Laptops (13-14 inch, 1366x768 or similar) */
        @media (max-width: 1400px) {{
            .header-section {{
                padding: 25px;
            }}
            
            .header-content {{
                margin-left: 110px;
            }}
            
            .header-logo {{
                max-width: 220px;
                max-height: 150px;
            }}
            
            .header-section h1 {{
                font-size: 2.2rem;
            }}
            
            .header-section .subtitle {{
                font-size: 1.1rem;
            }}
            
            .stat-card {{
                padding: 20px;
            }}
            
            .stat-number {{
                font-size: 2rem;
            }}
            
            .stat-icon {{
                font-size: 2rem;
            }}
        }}
        
        /* Extra Small Laptops (older 13 inch models, 1280x800) */
        @media (max-width: 1280px) {{
            .dashboard-container {{
                margin: 15px;
                padding: 25px;
            }}
            
            .header-section {{
                padding: 20px;
            }}
            
            .header-content {{
                margin-left: 90px;
            }}
            
            .header-logo {{
                max-width: 180px;
                max-height: 120px;
                left: 20px;
            }}
            
            .header-section h1 {{
                font-size: 2rem;
            }}
            
            .header-section .subtitle {{
                font-size: 1rem;
            }}
            
            .stats-grid {{
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 15px;
            }}
            
            .stat-card {{
                padding: 18px;
            }}
            
            .stat-number {{
                font-size: 1.8rem;
            }}
            
            .section-title {{
                font-size: 1.5rem;
            }}
            
            .module-name {{
                font-size: 1.3rem;
            }}
            
            .module-description {{
                font-size: 0.85rem;
                padding: 6px 10px;
            }}
        }}
        
        /* Very Small Laptops (11-12 inch netbooks, 1024x768) */
        @media (max-width: 1024px) {{
            .dashboard-container {{
                margin: 10px;
                padding: 20px;
            }}
            
            .header-section {{
                padding: 20px 15px;
            }}
            
            .header-content {{
                margin-left: 75px;
            }}
            
            .header-logo {{
                max-width: 150px;
                max-height: 100px;
                left: 15px;
            }}
            
            .header-section h1 {{
                font-size: 1.8rem;
            }}
            
            .header-section .subtitle {{
                font-size: 0.95rem;
            }}
            
            .stats-grid {{
                grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
                gap: 12px;
            }}
            
            .stat-card {{
                padding: 15px;
            }}
            
            .stat-number {{
                font-size: 1.6rem;
            }}
            
            .stat-icon {{
                font-size: 1.8rem;
            }}
            
            .module-stat-number {{
                font-size: 1.3rem;
            }}
            
            .module-description {{
                font-size: 0.8rem;
                padding: 6px 8px;
                line-height: 1.5;
            }}
        }}
        
        /* Tablets and Mobile (Not for company use, but fallback) */
        @media (max-width: 768px) {{
            .dashboard-container {{
                margin: 10px;
                padding: 20px;
            }}
            
            .header-section {{
                padding: 30px;
            }}
            
            .header-content {{
                margin-left: 0;
            }}
            
            .header-logo {{
                position: static;
                transform: none;
                display: block;
                margin: 0 auto 15px;
                max-width: 140px;
                max-height: 110px;
            }}
            
            .header-section h1 {{
                font-size: 2rem;
            }}
            
            .stats-grid {{
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 15px;
            }}
            
            .module-summary {{
                flex-direction: column;
                align-items: flex-start;
            }}
            
            .module-description {{
                font-size: 0.8rem;
                padding: 6px 8px;
                line-height: 1.4;
            }}
        }}
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="dashboard-container">
            <!-- Header Section -->
            <div class="header-section">
                {"<img src='" + logo_base64 + "' alt='InferIQ Logo' class='header-logo'>" if logo_base64 else ""}
                <div class="header-content">
                    <h1><i class="fas fa-chart-line"></i> Automation Test Report</h1>
                    <p class="subtitle">Automated Test Results Overview</p>
                    <small>Generated on {timestamp}</small>
                </div>
            </div>
            
            <!-- Overall Statistics -->
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon text-info">
                        <i class="fas fa-list-check"></i>
                    </div>
                    <div class="stat-number text-info">{overall_stats['total']}</div>
                    <div class="stat-label">Total Tests</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon text-success">
                        <i class="fas fa-check-circle"></i>
                    </div>
                    <div class="stat-number text-success">{overall_stats['passed']}</div>
                    <div class="stat-label">Passed</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon text-danger">
                        <i class="fas fa-times-circle"></i>
                    </div>
                    <div class="stat-number text-danger">{overall_stats['failed'] + overall_stats['errors']}</div>
                    <div class="stat-label">Failed</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon text-warning">
                        <i class="fas fa-minus-circle"></i>
                    </div>
                    <div class="stat-number text-warning">{overall_stats['skipped']}</div>
                    <div class="stat-label">Skipped</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon text-secondary">
                        <i class="fas fa-clock"></i>
                    </div>
                    <div class="stat-number text-secondary">{overall_stats['duration']}s</div>
                    <div class="stat-label">Duration</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon text-{'success' if overall_stats['success_rate'] >= 90 else 'warning' if overall_stats['success_rate'] >= 70 else 'danger'}">
                        <i class="fas fa-percentage"></i>
                    </div>
                    <div class="stat-number text-{'success' if overall_stats['success_rate'] >= 90 else 'warning' if overall_stats['success_rate'] >= 70 else 'danger'}">{overall_stats['success_rate']}%</div>
                    <div class="stat-label">Success Rate</div>
                </div>
            </div>
            
            <!-- Module Details -->
            <div class="modules-section">
                <h2 class="section-title">
                    <i class="fas fa-cubes"></i> Module-wise Results
                </h2>
                {module_cards_html}
            </div>
            
            <!-- Footer -->
            <div class="footer">
                <p><i class="fas fa-robot"></i> Generated by InferIQ</p>
                <p style="margin-top: 15px; font-weight: 500;">
                    &copy; Copyright 2025 Idexcel, Inc. All Rights Reserved.
                </p>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Toggle test steps expand/collapse
        function toggleSteps(collapseId) {{
            const element = document.getElementById(collapseId);
            const icon = document.getElementById('icon-' + collapseId);
            
            if (element.style.display === 'none' || element.style.display === '') {{
                element.style.display = 'block';
                if (icon) {{
                    icon.classList.add('rotated');
                }}
            }} else {{
                element.style.display = 'none';
                if (icon) {{
                    icon.classList.remove('rotated');
                }}
            }}
        }}
    </script>
</body>
</html>"""
        
        return html_template
    
    def _generate_module_cards(self):
        """Generate HTML for module cards"""
        if not self.test_data:
            return '<div class="alert alert-warning"><i class="fas fa-exclamation-triangle"></i> No test data found</div>'
        
        cards_html = ""
        
        # Sort modules by success rate (best first)
        sorted_modules = sorted(
            self.test_data.items(),
            key=lambda x: self._calculate_success_rate(x[1]),
            reverse=True
        )
        
        for module_name, module_data in sorted_modules:
            success_rate = self._calculate_success_rate(module_data)
            status_color = self._get_status_color(success_rate)
            
            # Generate test details
            test_details_html = ""
            for idx, test in enumerate(module_data['tests']):
                status_class = f"status-{test['status']}"
                icon = self._get_status_icon(test['status'])
                
                # Get test steps if available
                test_steps = test.get('steps', '')
                has_steps = bool(test_steps)
                
                # Generate unique ID for collapse
                collapse_id = f"collapse-{module_name.replace(' ', '-')}-{idx}"
                
                test_details_html += f"""
                <div class="test-item-container">
                    <div class="test-item" {'onclick="toggleSteps(\'' + collapse_id + '\')"' if has_steps else ''} style="cursor: {'pointer' if has_steps else 'default'};">
                        <div class="test-name-container">
                            {f'<i class="fas fa-chevron-right collapse-icon" id="icon-{collapse_id}"></i>' if has_steps else ''}
                            <span class="test-name">{test['name']}</span>
                        </div>
                        <div class="test-status">
                            <span class="status-badge {status_class}">
                                <i class="{icon}"></i> {test['status'].upper()}
                            </span>
                            <small class="text-muted">{test['duration']:.2f}s</small>
                        </div>
                    </div>
                    {f'''<div class="test-steps-collapse" id="{collapse_id}" style="display: none;">
                        <div class="test-steps-content">
                            <strong><i class="fas fa-list-ol"></i> Test Steps:</strong>
                            <div class="steps-list">{test_steps}</div>
                        </div>
                    </div>''' if has_steps else ''}
                </div>
                """
            
            cards_html += f"""
            <div class="module-card">
                <div class="module-header">
                    <div class="module-name">
                        <i class="fas fa-folder"></i> {module_name}
                    </div>
                    <div class="module-description">
                        {self._get_module_description(module_name)}
                    </div>
                    <div class="module-summary">
                        <div class="module-stats">`
                            <div class="module-stat">
                                <div class="module-stat-number">{module_data['total']}</div>
                                <div class="module-stat-label">Total</div>
                            </div>
                            <div class="module-stat">
                                <div class="module-stat-number">{module_data['passed']}</div>
                                <div class="module-stat-label">Passed</div>
                            </div>
                            <div class="module-stat">
                                <div class="module-stat-number">{module_data['failed'] + module_data['errors']}</div>
                                <div class="module-stat-label">Failed</div>
                            </div>
                            <div class="module-stat">
                                <div class="module-stat-number">{int(module_data['duration'] // 60)}m {int(module_data['duration'] % 60)}s</div>
                                <div class="module-stat-label">Duration</div>
                            </div>
                        </div>
                        <div class="success-badge">
                            <i class="fas fa-chart-pie"></i> {success_rate}% Success
                        </div>
                    </div>
                </div>
                <div class="module-body">
                    <div class="progress-container">
                        <div class="progress">
                            <div class="progress-bar bg-success" style="width: {(module_data['passed'] / module_data['total'] * 100) if module_data['total'] > 0 else 0}%"></div>
                            <div class="progress-bar bg-danger" style="width: {((module_data['failed'] + module_data['errors']) / module_data['total'] * 100) if module_data['total'] > 0 else 0}%"></div>
                            <div class="progress-bar bg-warning" style="width: {(module_data['skipped'] / module_data['total'] * 100) if module_data['total'] > 0 else 0}%"></div>
                        </div>
                    </div>
                    <div class="test-details">
                        {test_details_html}
                    </div>
                </div>
            </div>
            """
        
        return cards_html
    
    def _get_status_icon(self, status):
        """Get Font Awesome icon for test status"""
        icons = {
            'passed': 'fas fa-check',
            'failed': 'fas fa-times',
            'errors': 'fas fa-exclamation',
            'skipped': 'fas fa-minus'
        }
        return icons.get(status, 'fas fa-question')


def main():
    """Main function to run the dashboard generator"""
    print("🚀 InferIQ Test Dashboard Generator")
    print("=" * 50)
    
    generator = TestDashboardGenerator()
    
    success = generator.generate_dashboard()
    
    if success:
        print("=" * 50)
        print("🎉 Dashboard generation completed successfully!")
        print(f"📁 Open: {os.path.abspath(generator.output_path)}")
        
        # Try to open the dashboard in default browser (optional)
        try:
            import webbrowser
            webbrowser.open(f"file://{os.path.abspath(generator.output_path)}")
            print("🌐 Dashboard opened in your default browser")
        except:
            print("💡 Open the dashboard manually in your browser")
    else:
        print("❌ Dashboard generation failed")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())