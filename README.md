# ATS Resume Scorer

A simple and powerful web application to check if a resume matches a job description and get clear suggestions for improvement. 

Perfect for students preparing for job hunts!

---

## How It Works

1. **Upload Resume**: Upload your resume in PDF or DOCX format.
2. **Add Job Description**: Paste the job description you want to target.
3. **Get Score & Feedback**: View your ATS compatibility score (0-100), see what keywords you missed, and get actionable recommendations.
4. **Download Report**: Download a professional PDF summary of your analysis.

---

## Quick Start Guide

Follow these 5 simple steps to get the app running on your machine:

### Step 1: Download & Open the Project
1. Download or clone this project's folder.
2. Open your terminal or Command Prompt, and navigate to the project directory:
   ```bash
   cd ai-resume-ats-main
   ```

### Step 2: Set Up Python Virtual Environment
Creating a virtual environment keeps the project dependencies isolated.
* **On Windows:**
  ```powershell
  python -m venv venv
  venv\Scripts\activate
  ```
* **On Mac/Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### Step 3: Install Requirements
Install the required packages and download the NLP library:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_md
```
*(Note: PDF generation works out-of-the-box on all operating systems using a built-in fallback, so no extra system installations are required!)*

### Step 4: Configure API Keys
Create a `.env` file in the root folder (you can copy `.env.example` and rename it to `.env`). Add the following keys:
- **Groq API Key**: Get a free API key from [Groq Console](https://console.groq.com).
- **Supabase Keys**: Set up a free account at [Supabase](https://supabase.com) and get your project API keys.

Also, copy `frontend/.streamlit/secrets.toml.example` to `frontend/.streamlit/secrets.toml` and fill it with your Supabase anonymous keys.

### Step 5: Start the App!

You need to run two commands in separate terminal windows (make sure your virtual environment `venv` is activated in both):

1. **Start the Backend API Server:**
   ```bash
   venv\Scripts\uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   *(On Mac/Linux, run: `source venv/bin/activate` then `uvicorn backend.main:app --reload`)*

2. **Start the Frontend Web App:**
   ```bash
   venv\Scripts\streamlit run frontend/streamlit_app.py
   ```
   *(On Mac/Linux, run: `source venv/bin/activate` then `streamlit run frontend/streamlit_app.py`)*

Open your browser and go to **`http://localhost:8501`** to start using the app!

---


## Project Structure (For Curious Minds)
* `backend/`: Handles all the heavy lifting (file parsing, text comparison, NLP).
* `frontend/`: Streamlit code for the user interface.
* `requirements.txt`: List of Python libraries this project needs.
* `.env`: Holds your private API keys (never upload or share this file!).


## Environment Variables Setup

This project requires API keys from Supabase and Groq. Create a `.env` file in the root directory and add the following variables.

### 1. Supabase Configuration

Create a free account on Supabase and create a new project.

Navigate to:

**Project Settings → API**

Copy the following values:

* **SUPABASE_URL** – Your Supabase project URL.
* **SUPABASE_ANON_KEY** – Public anonymous key.
* **SUPABASE_KEY** – Service Role Key (used by the backend for database operations).
* **SUPABASE_JWT_SECRET** – JWT Secret used for authentication token verification.

### 2. Groq API Configuration

Create a free account at Groq and generate an API key.

* **GROQ_API_KEY** – Used for AI-powered resume analysis and suggestions.

### `.env` File Example

```env
# ─────────────────────────────
# SUPABASE CONFIGURATION
# ─────────────────────────────
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_public_key
SUPABASE_KEY=your_supabase_service_role_key
SUPABASE_JWT_SECRET=your_supabase_jwt_secret

# ─────────────────────────────
# GROQ API CONFIGURATION
# ─────────────────────────────
GROQ_API_KEY=your_groq_api_key
```

### Where to Get the Keys

#### Supabase

1. Go to your Supabase Dashboard.
2. Open your project.
3. Navigate to **Project Settings → API**.
4. Copy the required keys and URL.

#### Groq

1. Visit https://console.groq.com
2. Sign in or create an account.
3. Generate a new API key.
4. Paste it into your `.env` file.

### Security Note

Never commit your `.env` file or API keys to GitHub. Add `.env` to your `.gitignore` file before pushing your code.














