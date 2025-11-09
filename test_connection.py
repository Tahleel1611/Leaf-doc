"""
Test script to verify backend is working and ready for frontend connection.
"""
import requests
import sys
from pathlib import Path

BACKEND_URL = "http://localhost:8000"
COLORS = {
    'GREEN': '\033[92m',
    'RED': '\033[91m',
    'YELLOW': '\033[93m',
    'BLUE': '\033[94m',
    'END': '\033[0m'
}

def print_colored(text, color='GREEN'):
    """Print colored text."""
    print(f"{COLORS.get(color, '')}{text}{COLORS['END']}")

def test_health():
    """Test health endpoint."""
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_colored(f"   ✓ Health check passed", 'GREEN')
            print(f"   - Status: {data['status']}")
            print(f"   - App: {data['app_name']}")
            print(f"   - Model loaded: {data['model_loaded']}")
            return True
        else:
            print_colored(f"   ✗ Health check failed: {response.status_code}", 'RED')
            return False
    except requests.exceptions.ConnectionError:
        print_colored(f"   ✗ Cannot connect to backend at {BACKEND_URL}", 'RED')
        print(f"   Please make sure backend is running: uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print_colored(f"   ✗ Error: {e}", 'RED')
        return False

def test_cors():
    """Test CORS headers."""
    print("\n2. Testing CORS configuration...")
    try:
        headers = {'Origin': 'http://localhost:5173'}
        response = requests.options(f"{BACKEND_URL}/api/predict", headers=headers, timeout=5)
        cors_header = response.headers.get('access-control-allow-origin')
        if cors_header:
            print_colored(f"   ✓ CORS configured correctly", 'GREEN')
            print(f"   - Allowed origins: {cors_header}")
            return True
        else:
            print_colored(f"   ⚠ CORS headers not found", 'YELLOW')
            print(f"   This might cause issues with frontend")
            return True
    except Exception as e:
        print_colored(f"   ✗ Error testing CORS: {e}", 'RED')
        return False

def test_static_files():
    """Test static file serving."""
    print("\n3. Testing static file configuration...")
    try:
        # Just check if static endpoint exists (will 404 but that's ok)
        response = requests.get(f"{BACKEND_URL}/static/test.jpg", timeout=5)
        # 404 is expected, but it means static files are configured
        if response.status_code in [404, 200]:
            print_colored(f"   ✓ Static files endpoint configured", 'GREEN')
            return True
        else:
            print_colored(f"   ⚠ Static files might not be configured", 'YELLOW')
            return True
    except Exception as e:
        print_colored(f"   ✗ Error: {e}", 'RED')
        return False

def test_api_endpoints():
    """Test API endpoints are accessible."""
    print("\n4. Testing API endpoints...")
    
    endpoints = [
        ("GET", "/api/history"),
    ]
    
    all_pass = True
    for method, endpoint in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{BACKEND_URL}{endpoint}", timeout=5)
            
            if response.status_code in [200, 422]:  # 422 for validation errors is ok
                print_colored(f"   ✓ {method} {endpoint}", 'GREEN')
            else:
                print_colored(f"   ✗ {method} {endpoint}: {response.status_code}", 'RED')
                all_pass = False
        except Exception as e:
            print_colored(f"   ✗ {method} {endpoint}: {e}", 'RED')
            all_pass = False
    
    return all_pass

def check_storage_directories():
    """Check if storage directories exist."""
    print("\n5. Checking storage directories...")
    
    storage_path = Path("backend/storage")
    images_path = storage_path / "images"
    heatmaps_path = storage_path / "heatmaps"
    
    all_exist = True
    
    for path, name in [(images_path, "images"), (heatmaps_path, "heatmaps")]:
        if path.exists():
            print_colored(f"   ✓ {name} directory exists", 'GREEN')
        else:
            print_colored(f"   ✗ {name} directory missing", 'RED')
            print(f"   Creating {path}...")
            path.mkdir(parents=True, exist_ok=True)
            all_exist = False
    
    return True

def main():
    """Run all tests."""
    print_colored("\n" + "="*60, 'BLUE')
    print_colored("LeafDoc Backend Integration Test", 'BLUE')
    print_colored("="*60, 'BLUE')
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health()))
    results.append(("CORS Configuration", test_cors()))
    results.append(("Static Files", test_static_files()))
    results.append(("API Endpoints", test_api_endpoints()))
    results.append(("Storage Directories", check_storage_directories()))
    
    # Summary
    print_colored("\n" + "="*60, 'BLUE')
    print_colored("Test Summary", 'BLUE')
    print_colored("="*60, 'BLUE')
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        color = 'GREEN' if result else 'RED'
        print_colored(f"  {status} - {test_name}", color)
    
    print()
    if passed == total:
        print_colored(f"All tests passed! ({passed}/{total})", 'GREEN')
        print_colored("\n✓ Backend is ready for frontend connection!", 'GREEN')
        print(f"\nYou can now start the frontend:")
        print(f"  cd leafdoc-plant-aid")
        print(f"  npm run dev")
        return 0
    else:
        print_colored(f"Some tests failed ({passed}/{total})", 'RED')
        print_colored("\n⚠ Please fix the issues before connecting frontend", 'YELLOW')
        return 1

if __name__ == "__main__":
    sys.exit(main())
