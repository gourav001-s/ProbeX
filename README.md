🔎 ProbeX

ProbeX is a hybrid OSINT username correlation framework designed for multi-platform account discovery and digital footprint analysis.

It provides a clean, modular, menu-driven CLI experience for responsible open-source intelligence research and public account verification.

<img width="456" height="302" alt="Screenshot 2026-02-13 132538" src="https://github.com/user-attachments/assets/5ae6e755-8655-4b00-9df0-4298fa9ec91c" />

⚠️ For educational purposes and authorized investigations only.

✨ Key Features

Asynchronous multi-platform username scanning
Hybrid HTTP + headless browser verification
Username permutation engine
Confidence scoring system
Controlled concurrency & retry logic
Anti-block detection with browser fallback
JSON report generation
Interactive and CLI-based execution
Clean and professional terminal interface

🧠 Design Philosophy

ProbeX is not a one-click tracking tool.

The framework focuses on:

Accuracy over blind automation
Transparency over hidden scraping
Responsible OSINT methodology
Analyst-controlled verification
Public data only

Each module assists the researcher instead of hiding what happens internally.

Hybrid scanning ensures:

Speed from async HTTP checks
Accuracy from browser verification
Structured correlation instead of raw guessing

🛠 Requirements

Linux / macOS / Windows
Python 3.9+
aiohttp

Install dependencies:

pip install aiohttp 

🚀 Installation
```
git clone https://github.com/gourav001-s/probex.git
cd probex
python3 ProbeX.py
```

Ensure:

Internet connection is active
Dependencies are installed correctly

📋 Usage

Run the framework:
```
python3 ProbeX.py
```

Or use CLI mode:
```
python3 ProbeX.py --username ravx
```

Enable permutations:
```
python3 ProbeX.py --username ravx --permutations
```

Generate a JSON report:
```
python3 ProbeX.py --username ravx --report report.json
```
🔗 Example Workflow

Run interactive mode

Enter target username

Enable permutation scanning (optional)

ProbeX performs asynchronous HTTP scanning

Blocked or ambiguous platforms trigger browser verification

Results are correlated and confidence score calculated

Optional JSON report is generated

📁 Output

Console-based findings

Structured JSON report (if enabled):

report.json


Report contains:

Username scanned
Platforms discovered
Confidence level
Total requests made
Scan duration
Timestamp


⚠️ Ethical Notice

This framework is intended for educational purposes and authorized OSINT research only.

You must:

Use publicly available data only
Respect platform terms of service
Avoid accessing private accounts
Comply with local laws

The author assumes no responsibility for misuse.

👤 Author

RavX

Cybersecurity & Automation Enthusiast

⭐ Contributions

Contributions and improvements are welcome.

Please ensure:

Ethical usage
Clean modular structure
Transparent logic
Responsible research orientation

Pull requests promoting illegal activity will not be accepted.
