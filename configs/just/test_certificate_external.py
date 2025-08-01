import webbrowser
import requests
from pathlib import Path

# Get the current directory
current_dir = Path(__file__).parent

# Test the external image URL
external_image_url = "https://i.ibb.co/YBMmKFqT/udemy-certificate.png"
print("Testing external image URL...")
try:
    response = requests.head(external_image_url, timeout=10)
    if response.status_code == 200:
        print(f"✓ External image URL is accessible: {external_image_url}")
        content_length = response.headers.get('content-length')
        if content_length:
            print(f"  Image size: {int(content_length) / 1024:.1f} KB")
    else:
        print(f"✗ External image URL returned status {response.status_code}")
except requests.RequestException as e:
    print(f"✗ Could not access external image: {e}")

# Check if the fixed HTML file exists
fixed_html = current_dir / "certificate-fixed.html"
if fixed_html.exists():
    print(f"\n✓ Fixed HTML file found: {fixed_html}")
    
    # Read and check if it contains the external image reference
    with open(fixed_html, 'r', encoding='utf-8') as f:
        content = f.read()
        if 'i.ibb.co' in content:
            print("✓ HTML file contains reference to external certificate image")
        elif 'udemy_certificate.png' in content:
            print("⚠ HTML file still contains reference to local image")
        else:
            print("✗ HTML file does NOT contain any certificate image reference")
    
    # Open in browser
    file_url = fixed_html.as_uri()
    print(f"\nOpening certificate in browser: {file_url}")
    webbrowser.open(file_url)
    
    print("\n" + "="*60)
    print("CERTIFICATE VERIFICATION COMPLETE")
    print("="*60)
    print("The certificate should now display with the external image.")
    print("This version will work even without the local image file!")
else:
    print("✗ Fixed HTML file NOT found!") 