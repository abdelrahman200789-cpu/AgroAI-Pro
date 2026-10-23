# AgroAI Pro — Smart Farming Advisor

An educational Streamlit prototype for exploring crop planning, plant-symptom matching, simple sensor thresholds, and local agricultural knowledge notes.

## Features

- **Dashboard:** summary metrics and crop catalog chart.
- **Plant symptom assistant:** ranks included example rules by symptom overlap.
- **Crop recommendation:** creates a transparent heuristic shortlist using season, soil type, pH, and water-need preference.
- **IoT monitor:** checks manually entered sensor values against demonstration thresholds.
- **Knowledge hub:** keyword search across bundled text notes.
- **Dataset explorer:** filter, inspect, and download crop catalog rows.
- Separate core logic in `agro_engine.py`, demo data in `data/`, and basic tests in `tests/`.

## Requirements

- Python 3.10 or newer recommended
- pip
- Internet connection only if installing packages or loading the optional sidebar image

## Run locally

### 1. Extract the project

Open a terminal in the `AgroAI_Pro_Streamlit` project folder.

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install packages

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Launch the Streamlit app

```bash
streamlit run app.py
```

Streamlit should open the app in your browser. If it does not, use the local URL printed in the terminal, usually `http://localhost:8501`.

### 5. Run tests

```bash
pytest -q
```

## Project structure

```text
AgroAI_Pro_Streamlit/
├── app.py                     # Streamlit interface and navigation
├── agro_engine.py             # Diagnosis, recommendation, sensor, and search logic
├── data/
│   ├── crops.csv              # Educational crop catalog
│   ├── disease_rules.json    # Illustrative symptom rules
│   └── knowledge/             # Local knowledge notes
├── tests/
│   └── test_agro_engine.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Important limitations

- The crop catalog, symptom rules, and sensor thresholds are **educational demo data**, not a validated or comprehensive regional agricultural dataset.
- A symptom overlap score is **not** a probability and does not confirm a disease.
- Crop suitability scores are simple rule-based heuristics, not yield predictions.
- Sensor readings are manually entered; no physical IoT device, weather API, or cloud database is connected.
- Confirm field decisions with local agricultural specialists, soil tests, and current regional guidance. Follow all product labels and local regulations.

## Suggested future upgrades

1. Replace demo data with documented datasets from trusted agricultural/extension sources and preserve citations and licenses.
2. Add image-based disease classification only after collecting a correctly labeled, licensed dataset and evaluating performance.
3. Connect real sensors using a secure API or MQTT broker and add authentication.
4. Add Arabic/English language switching and regional crop calendars.
5. Add database persistence, user accounts, and deployment configuration.

## License / data provenance

No third-party crop dataset is bundled. The included catalog and symptom rules are manually assembled illustrative examples. Review and adapt them with a qualified agricultural specialist before any practical use. Choose a project license before publishing or redistributing.
