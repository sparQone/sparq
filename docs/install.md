# Install sparQ

## Requirements:
- Python 3.10+
- pip
- git
- OSX/Linux


## Get the code:
```bash
git clone https://github.com/sparqone/sparq
cd sparq
```

## Setup Virtual Environment

If you don't have venv installed (Ubuntu/Debian):
```bash
sudo apt-get install python3-venv
```

## Create and activate virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install Dependencies

### Quick Install (Recommended)
```bash
pip install -r requirements.txt
```

Skip to the end to run the application.


### Manual Dependency Update 
If you need to update dependencies:

1. Install pip-tools:
```bash
pip install pip-tools
```

2. Update requirements.in with new dependencies

3. Compile new requirements.txt:
```bash
pip-compile --output-file=requirements.txt requirements.in
```

4. Install updated dependencies:
```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python app.py
```

The application will be available at http://localhost:8000


