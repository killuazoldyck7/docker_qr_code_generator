import os
import sys
import qrcode
import logging
import argparse
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
import validators

print("Starting QR Code generation script...")

# Load environment variables from .env file if it exists
load_dotenv()
print("Environment variables loaded")

# Set environment variables for QR code customization
QR_DATA_URL = os.getenv('QR_DATA_URL', 'https://github.com/killuazoldyck7')
QR_DIRECTORY = os.getenv('QR_CODE_DIR', 'qr_codes')
QR_CODE_FILENAME = os.getenv('QR_CODE_FILENAME', 'github_qr.png')
FILL_COLOR = os.getenv('FILL_COLOR', 'black')
BACK_COLOR = os.getenv('BACK_COLOR', 'white')

print(f"URL: {QR_DATA_URL}")
print(f"Directory: {QR_DIRECTORY}")
print(f"Filename: {QR_CODE_FILENAME}")
print(f"Colors - Fill: {FILL_COLOR}, Back: {BACK_COLOR}")

def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )

def create_directory(path: Path):
    """Create directory if it doesn't exist."""
    try:
        path.mkdir(parents=True, exist_ok=True)
        print(f"Directory created or already exists at: {path}")
    except Exception as e:
        logging.error(f"Failed to create directory {path}: {e}")
        sys.exit(1)

def is_valid_url(url):
    """Validate the URL."""
    if validators.url(url):
        print(f"Valid URL provided: {url}")
        return True
    print(f"Invalid URL provided: {url}")
    return False

def generate_qr_code(data, path, fill_color='black', back_color='white'):
    """Generate and save QR code."""
    if not is_valid_url(data):
        print("QR code generation aborted due to invalid URL.")
        return

    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color)

        print(f"Attempting to save QR code to {path}")
        with path.open('wb') as f:
            img.save(f)
        print(f"QR code successfully saved to {path}")
    except Exception as e:
        print(f"Error generating or saving QR code: {e}")

def main():
    # Set up logging
    setup_logging()
    print("Entering main function")

    # Set up argument parser and handle URL input
    parser = argparse.ArgumentParser(description="Generate a QR code.")
    parser.add_argument('--url', help="URL for the QR code", default=QR_DATA_URL)
    args = parser.parse_args()

    url = args.url
    print(f"Using URL: {url}")

    # Ensure QR code directory exists
    output_directory = Path(QR_DIRECTORY)
    print(f"Output directory: {output_directory}")
    create_directory(output_directory)

    # Define the full path for the QR code file
    qr_code_path = output_directory / QR_CODE_FILENAME
    print(f"QR code will be saved as {qr_code_path}")

    # Generate the QR code
    generate_qr_code(url, qr_code_path, FILL_COLOR, BACK_COLOR)

if __name__ == "__main__":
    main()
