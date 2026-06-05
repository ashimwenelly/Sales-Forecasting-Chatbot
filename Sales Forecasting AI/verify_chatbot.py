#!/usr/bin/env python3
"""
Verification script to test the Sales Forecasting Chatbot setup
Run this to ensure all components are working correctly
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version"""
    print("\n[1/7] Checking Python version...")
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return version.major >= 3 and version.minor >= 8

def check_dependencies():
    """Check if all required packages are installed"""
    print("\n[2/7] Checking dependencies...")
    required = {
        'pandas': 'Data processing',
        'matplotlib': 'Chart generation',
        'statsmodels': 'Time series forecasting',
        'sklearn': 'Machine learning',
        'fastapi': 'Web framework',
        'uvicorn': 'ASGI server',
    }
    
    missing = []
    for package, description in required.items():
        try:
            __import__(package)
            print(f"✓ {package:15} - {description}")
        except ImportError:
            print(f"✗ {package:15} - {description} [MISSING]")
            missing.append(package)
    
    return len(missing) == 0

def check_data_file():
    """Check if data file exists"""
    print("\n[3/7] Checking data file...")
    csv_file = Path('stores_sales_forecasting.csv')
    if csv_file.exists():
        size_mb = csv_file.stat().st_size / (1024 * 1024)
        print(f"✓ Data file found: {csv_file} ({size_mb:.2f} MB)")
        return True
    else:
        print(f"✗ Data file not found: {csv_file}")
        return False

def check_backend_file():
    """Check if backend file exists"""
    print("\n[4/7] Checking backend file...")
    backend_file = Path('chatbot_backend.py')
    if backend_file.exists():
        print(f"✓ Backend file found: {backend_file}")
        return True
    else:
        print(f"✗ Backend file not found: {backend_file}")
        return False

def check_frontend_files():
    """Check if frontend files exist"""
    print("\n[5/7] Checking frontend files...")
    files = {
        'static/index.html': 'Main UI',
        'static/style.css': 'Styling',
        'static/script.js': 'JavaScript logic',
    }
    
    all_exist = True
    for filepath, description in files.items():
        if Path(filepath).exists():
            print(f"✓ {filepath:25} - {description}")
        else:
            print(f"✗ {filepath:25} - {description} [MISSING]")
            all_exist = False
    
    return all_exist

def test_data_loading():
    """Test if data can be loaded"""
    print("\n[6/7] Testing data loading...")
    try:
        from sales_forecasting import load_sales_data, build_monthly_series
        df = load_sales_data(Path('stores_sales_forecasting.csv'))
        monthly = build_monthly_series(df)
        print(f"✓ Data loaded successfully: {len(df)} records")
        print(f"✓ Monthly aggregation: {len(monthly)} months")
        return True
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        return False

def test_forecasting():
    """Test if forecasting works"""
    print("\n[7/7] Testing forecasting engine...")
    try:
        from sales_forecasting import (
            load_sales_data, build_monthly_series, create_forecast_report
        )
        df = load_sales_data(Path('stores_sales_forecasting.csv'))
        monthly = build_monthly_series(df)
        forecast = create_forecast_report(monthly, 6)
        print(f"✓ Forecast generated: {len(forecast)} months")
        print(f"✓ Forecast columns: {', '.join(forecast.columns)}")
        print(f"✓ Sample forecast:\n{forecast.head(3).to_string()}")
        return True
    except Exception as e:
        print(f"✗ Error generating forecast: {e}")
        return False

def main():
    """Run all checks"""
    print("\n" + "="*60)
    print("  Sales Forecasting AI Chatbot - Verification Script")
    print("="*60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Data File", check_data_file),
        ("Backend File", check_backend_file),
        ("Frontend Files", check_frontend_files),
        ("Data Loading", test_data_loading),
        ("Forecasting", test_forecasting),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"✗ Error during {name}: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "="*60)
    print("  Summary")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} {name}")
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! Your chatbot is ready to use.")
        print("\nTo start the chatbot, run:")
        print("  powershell .\\run_chatbot.ps1")
        print("  or")
        print("  .\\run_chatbot.bat")
        print("\nThen open: http://localhost:8000/static/index.html")
        return 0
    else:
        print(f"\n⚠️  {total - passed} check(s) failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("  • Install dependencies: python -m pip install -r requirements.txt")
        print("  • Ensure stores_sales_forecasting.csv is in this directory")
        print("  • Check that all files were created correctly")
        return 1

if __name__ == '__main__':
    sys.exit(main())
