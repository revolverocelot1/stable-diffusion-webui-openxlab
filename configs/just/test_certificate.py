import os
import webbrowser
from pathlib import Path

# Get the current directory
current_dir = Path(__file__).parent

# Check if the certificate image exists
certificate_image = current_dir / "udemy_certificate.png"
if certificate_image.exists():
    print(f"✓ Certificate image found: {certificate_image}")
    print(f"  Size: {certificate_image.stat().st_size / 1024:.1f} KB")
else:
    print("✗ Certificate image NOT found!")

# Check if the fixed HTML file exists
fixed_html = current_dir / "certificate-fixed.html"
if fixed_html.exists():
    print(f"✓ Fixed HTML file found: {fixed_html}")
    
    # Read and check if it contains the image reference
    with open(fixed_html, 'r', encoding='utf-8') as f:
        content = f.read()
        if 'udemy_certificate.png' in content:
            print("✓ HTML file contains reference to certificate image")
        else:
            print("✗ HTML file does NOT contain reference to certificate image")
    
    # Open in browser
    file_url = fixed_html.as_uri()
    print(f"\nOpening certificate in browser: {file_url}")
    webbrowser.open(file_url)
else:
    print("✗ Fixed HTML file NOT found!")

# Also check the original file
original_html = current_dir / "Udemy Course Completion Certificate _ Udemy.html"
if original_html.exists():
    print(f"\n✓ Original HTML file found: {original_html}")
    print(f"  Size: {original_html.stat().st_size / 1024:.1f} KB")
else:
    print("\n✗ Original HTML file NOT found!")

print("\nIf the certificate doesn't display properly, make sure all files are in the same directory.") 