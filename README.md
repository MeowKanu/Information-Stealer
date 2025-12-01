# Safe Information Stealer Simulation

This project is a safe and educational simulation of how an information stealer works internally. 
It does NOT access or decrypt any real browser data. All files and credentials are generated 
locally using dummy test data for training and learning purposes.

## Features

- Generates a fake browser profile with:
  - Fake 'Local State' JSON file
  - Fake 'Login Data' SQLite database
  - AES-GCM encrypted dummy passwords
- Reads and decrypts ONLY the dummy test data
- Safe detector scans for Chrome-like paths (no decryption)
- 100% safe for academic use and cyber security learning

## Project Structure

safe-info-stealer-sim/
│── generate_fake_browser_data.py # Creates fake Local State + Login Data
│── simulated_stealer.py # Decrypts the dummy test data
│── detector.py # Safe browser artifact detector
│── fake_profile/ # Auto-generated fake browser files
│── artifact_copies/ # Copies of detected artifacts (optional)
└── README.md

shell
Copy code

## Installation

Install required modules:

pip install cryptography
pip install pyperclip # optional

shell
Copy code

## Usage

### 1. Generate Fake Browser Data
python generate_fake_browser_data.py

shell
Copy code

### 2. Run the Simulation (Decrypt Dummy Data)
python simulated_stealer.py

shell
Copy code

### 3. Run the Safe Detector (Optional)
python detector.py

markdown
Copy code

## Notes

- This project uses ONLY locally generated dummy data.
- It does NOT access real Chrome/Edge/Brave profiles.
- Use for cybersecurity education, labs, or research only.
- Always run in a controlled environment (VM recommended).

## License

MIT License
