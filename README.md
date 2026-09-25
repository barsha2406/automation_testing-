# OrangeHRM QA Automation — Selenium + pytest

A Python/Selenium Page Object Model framework for the QA Automation assessment.

## Coverage

- Login to the OrangeHRM demo and assert dashboard visibility.
- Create an employee from JSON test data, including profile image upload.
- Update Job Title and Employment Status and assert the values in the UI.
- Use `restful-api.dev` as the assignment-permitted API substitute: create/read/update/read/delete/read and assert responses.
- Delete the UI employee and assert it is no longer in the employee search results.
- Log out and verify a protected route redirects to login.
- pytest HTML report and failure screenshots.

**API scope limitation:** `restful-api.dev` is a separate public mock API. It is not connected to OrangeHRM and cannot independently prove the OrangeHRM backend's persisted data. The test mirrors the UI employee's data to the mock API and compares the corresponding values as a demonstration of API contract validation. This limitation is stated transparently because the assignment allows a public test API as a substitute.

## Requirements

- Python 3.10+
- Google Chrome
- Internet access to the OrangeHRM demo and restful-api.dev
- Optional desktop/recording environment for video capture

## Setup

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The demo credentials from the assignment are defaults. Override with environment variables if needed:

```bash
# macOS/Linux
export ORANGEHRM_BASE_URL="https://opensource-demo.orangehrmlive.com"
export ORANGEHRM_USERNAME="Admin"
export ORANGEHRM_PASSWORD="admin123"
export HEADLESS="true"
```

PowerShell equivalents use `$env:NAME="value"`.

## Run

Run all tests:

```bash
pytest
```

Run only UI lifecycle:

```bash
pytest -m e2e
```

Run only API contract:

```bash
pytest -m api
```

The HTML report is generated at `reports/report.html`. Failed UI tests produce a screenshot in `reports/`. The browser driver is provisioned by webdriver-manager; first run requires internet access.

To watch the browser:

```bash
HEADLESS=false pytest -m e2e
```

## Video recording

A real video must be recorded on the machine where the browser is visible. This repository does not claim to contain a completed execution video. For cross-platform recording, use a desktop recorder such as OBS Studio or the operating system's screen recorder while running:

```bash
HEADLESS=false pytest -m e2e
```

Save the recording as `videos/employee-lifecycle.mp4` and commit it if repository size permits, or share a viewable Google Drive link in the submission. Headless browser runs do not capture desktop video.

## Structure

```text
.
├── api/
│   ├── __init__.py
│   └── mock_api_client.py
├── assets/
│   └── profile.png.base64
├── data/
│   └── employee.json
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   └── pim_page.py
├── tests/
│   ├── test_employee_lifecycle.py
│   └── test_mock_api_contract.py
├── reports/              # generated reports/screenshots
├── videos/               # add your recorded MP4 here
├── config.py
├── conftest.py
├── pytest.ini
└── requirements.txt
```

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `ORANGEHRM_BASE_URL` | OrangeHRM demo URL | Target application |
| `ORANGEHRM_USERNAME` | `Admin` | Login user |
| `ORANGEHRM_PASSWORD` | `admin123` | Login password |
| `HEADLESS` | `true` | Run Chrome headlessly |
| `SELENIUM_TIMEOUT` | `20` | Explicit wait timeout |
| `MOCK_API_URL` | `https://api.restful-api.dev` | Public API substitute |

## Submission checklist

1. Run the tests on your machine and confirm the report reflects the latest run.
2. Record the visible browser run and add the MP4 or a shared drive link.
3. Review the generated report for failures and environment-specific issues.
4. Push the project to GitHub and grant the requested reviewer access.
