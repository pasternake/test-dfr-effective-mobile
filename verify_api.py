import urllib.request
import urllib.error
import json
import sys

BASE_URL = "http://127.0.0.1:8000/api"

def make_request(url, method='GET', data=None, cookies=None):
    req = urllib.request.Request(url, method=method)
    req.add_header('Content-Type', 'application/json')
    
    if cookies:
        cookie_str = '; '.join([f"{k}={v}" for k, v in cookies.items()])
        req.add_header('Cookie', cookie_str)
    
    if data is not None:
        json_data = json.dumps(data).encode('utf-8')
        req.data = json_data

    try:
        with urllib.request.urlopen(req) as response:
            resp_data = response.read().decode('utf-8')
            # Simple cookie parsing
            resp_cookies = {}
            for header in response.info().get_all('Set-Cookie', []):
                parts = header.split(';')
                if parts:
                    name, value = parts[0].split('=', 1)
                    resp_cookies[name] = value
            
            return {
                'status': response.status,
                'data': json.loads(resp_data) if resp_data else {},
                'cookies': resp_cookies
            }
    except urllib.error.HTTPError as e:
        return {
            'status': e.code,
            'data': json.loads(e.read().decode('utf-8')) if e.fp else {},
            'cookies': {}
        }
    except Exception as e:
        print(f"Request failed: {e}")
        return {'status': 500, 'data': {}, 'cookies': {}}

def test_api():
    # 1. Admin Login
    print("Testing Admin Login...")
    resp = make_request(f"{BASE_URL}/auth/login/", method='POST', data={"email": "admin@example.com", "password": "admin123"})
    if resp['status'] != 200:
        print(f"Admin login failed: {resp['status']} {resp['data']}")
        return
    admin_cookies = resp['cookies']
    print("Admin login successful.")
    
    # 2. Admin Access GET
    print("Testing Admin GET Document...")
    resp = make_request(f"{BASE_URL}/business/documents/", method='GET', cookies=admin_cookies)
    if resp['status'] != 200:
        print(f"Admin GET failed: {resp['status']} {resp['data']}")
    else:
        print("Admin GET successful.")

    # 3. Admin Access POST
    print("Testing Admin POST Document...")
    resp = make_request(f"{BASE_URL}/business/documents/", method='POST', data={}, cookies=admin_cookies)
    if resp['status'] != 200:
        print(f"Admin POST failed: {resp['status']} {resp['data']}")
    else:
        print("Admin POST successful.")
        
    # 4. Viewer Login
    print("Testing Viewer Login...")
    resp = make_request(f"{BASE_URL}/auth/login/", method='POST', data={"email": "viewer@example.com", "password": "viewer123"})
    if resp['status'] != 200:
        print(f"Viewer login failed: {resp['status']} {resp['data']}")
        return
    viewer_cookies = resp['cookies']
    print("Viewer login successful.")
    
    # 5. Viewer Access GET
    print("Testing Viewer GET Document...")
    resp = make_request(f"{BASE_URL}/business/documents/", method='GET', cookies=viewer_cookies)
    if resp['status'] != 200:
        print(f"Viewer GET failed: {resp['status']} {resp['data']}")
    else:
        print("Viewer GET successful.")

    # 6. Viewer Access POST (Should fail)
    print("Testing Viewer POST Document (Expect 403)...")
    resp = make_request(f"{BASE_URL}/business/documents/", method='POST', data={}, cookies=viewer_cookies)
    if resp['status'] != 403:
        print(f"Viewer POST unexpected status: {resp['status']} {resp['data']}")
    else:
        print("Viewer POST correctly forbidden.")

    # 7. Anonymous Access
    print("Testing Anonymous GET Document (Expect 401)...")
    resp = make_request(f"{BASE_URL}/business/documents/", method='GET')
    if resp['status'] != 401:
        print(f"Anonymous GET unexpected status: {resp['status']} {resp['data']}")
    else:
        print("Anonymous GET correctly unauthorized.")

if __name__ == "__main__":
    test_api()
