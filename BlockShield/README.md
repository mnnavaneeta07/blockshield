# BlockShield

**AI-Powered Criminal Network Analysis Platform — SIH26189**

A web prototype for analysing connected crime-related entities and relationships. It provides:

- Relationship network visualization
- Entity and relationship counts
- Risk ranking based on connectivity and transaction value
- CSV data import
- Suspicious/high-risk entity identification
- Investigator-style dashboard

## Tech Stack

- Python
- Flask
- HTML5 / CSS3 / JavaScript
- Cytoscape.js for network visualization

## Run locally

1. Install Python 3.10+.
2. Open a terminal in this project folder.
3. Create a virtual environment:

```bash
python -m venv venv
```

4. Activate it.

Windows:
```bash
venv\Scripts\activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Start the application:

```bash
python app.py
```

7. Open `http://127.0.0.1:5000` in your browser.

## CSV format

Your CSV should contain exactly these four columns:

```text
source,target,relation,amount
Arun,Ravi,phone,0
Ravi,Kumar,money_transfer,75000
```

## Important

This repository is a **prototype/demo**. The current risk score is rule-based, not a trained AI/ML model. For a production/SIH implementation, replace the scoring module with validated NLP/ML models, secure authentication, encrypted data storage, audit logs, and controlled access to sensitive investigative data.
