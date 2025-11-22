# Gmail ⇄ Google Sheets Automation

A professional, dual-stack automation solution to sync Gmail data into
Google Sheets.

## 📦 Variations

This repository contains two distinct versions of the automation:

### 1. The "Lite" Version (Apps Script)

-   **Best for:** Individuals, Small Businesses, Low Volume (\<500
    emails/day).
-   **Tech:** Google Apps Script (JavaScript).
-   **Cost:** Free (Serverless, runs inside Google).
-   **Location:** `gsuite/apps-script/`
-   **Features:**
    -   Runs on a timer (e.g., every 10 mins).
    -   No external servers required.
    -   Easy to customize filtering.

### 2. The "Pro" Version (Python/FastAPI)

-   **Best for:** Developers, High Volume, Complex Logic, CRM
    Integrations.
-   **Tech:** Python 3.11, FastAPI, Docker.
-   **Cost:** Requires a hosting environment (VPS, Render, Railway,
    etc.).
-   **Location:** `app/`
-   **Features:**
    -   Real-time Polling Loop (Background Task).
    -   Webhook Endpoint included.
    -   Robust Error Handling & Logging.
    -   Modular structure (`services.py`).

------------------------------------------------------------------------

## 🚀 Quick Start: Python Version

### Prerequisites

-   Python 3.11+
-   A Google Cloud Project with `Gmail API` and `Google Sheets API`
    enabled.
-   A `service-account.json` file credentials.

### 1. Setup Environment

Copy the example env file:

``` bash
cp .env.example .env
```

Edit `.env` and set `ENABLE_GMAIL_POLLING=true` to start the background
worker automatically.

### 2. Install Dependencies

``` bash
pip install -r requirements.txt
```

### 3. Run Local

``` bash
uvicorn app.main:app --reload
```

The app will start up, connect to Gmail, and begin printing logs of
found emails to the console.

### 4. Docker Deployment

``` bash
docker-compose up --build -d
```

------------------------------------------------------------------------

## ⚡ Quick Start: Apps Script Version

1.  Open your Google Sheet.\
2.  Go to Extensions \> Apps Script.\
3.  Copy the code from `gsuite/apps-script/Code.gs`.\
4.  Run `setup()` once to authorize.\
5.  Set a Time-driven Trigger to run `checkGmail` every 10 minutes.

------------------------------------------------------------------------

# Project Catalog: Automated Gmail to Google Sheets Extraction

**Title:** I will build a custom Gmail to Google Sheets automation
(Python or Script)

**Headline:** Stop manually copying data. Get a reliable bot that
watches your inbox 24/7.

------------------------------------------------------------------------

### 📝 Project Description

Do you spend hours copying leads, orders, or invoices from email into a
spreadsheet? I will build a robust automation system that captures
incoming emails and organizes them perfectly into Google Sheets.

I offer two solutions depending on your needs:

**Option A: The "Serverless" Script (Best for most clients)** \* **Zero
monthly cost:** Runs entirely inside your Google Account. \*
**Features:** Extracts Date, Sender, Subject, and Body. \*
**Maintenance:** None. Set it and forget it.

**Option B: The "Pro" Python Engine** \* **Best for:** High volume or
complex data cleaning. \* **Features:** Hosted on your server/VPS.
Includes logging, error handling, and potential for complex integrations
(CRM/Database).

### 🎯 What you get

1.  **Data Extraction:** Automated parsing of Sender, Subject, Date, and
    Email Body.
2.  **Filtering:** The bot only picks up emails that match your criteria
    (e.g., "Label: Orders", "Subject: Invoice").
3.  **Post-Processing:** Automatically marks emails as "Read" or adds a
    "Processed" label so you never get duplicates.
4.  **Documentation:** A simple PDF or Video guide on how to use it.

### ⚙️ How it works

1.  We define the search criteria (e.g., "Unread emails from
    client@example.com").
2.  I deploy the code (either to your Google Sheet directly or your
    server).
3.  You watch the rows populate automatically.

### ⚠️ Requirements

-   Access to your Google Sheet (Editor permission).
-   (For Python version only) Access to a hosting environment or Google
    Cloud Project.

------------------------------------------------------------------------

**Delivery Time:** 1-2 Days.\
**Revisions:** 2 Included.
