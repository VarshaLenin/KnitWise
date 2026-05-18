# KnitWise AI

AI powered crochet pattern generation from reference images using Gemma 4 multimodal understanding.

---

## Overview

KnitWise AI is a crochet pattern generation platform designed to help beginners and crochet enthusiasts recreate designs from inspiration images.

Users can upload a reference image of a crochet piece, select the crochet type, yarn size, hook size, and generation mode, and receive a structured crochet pattern with organized rounds, stitch counts, construction notes, and a printable PDF version.

The system currently supports:
- Beanies
- Granny Squares
- Scarves

KnitWise AI focuses on generating beginner friendly, structured, and mathematically consistent crochet instructions instead of generic AI generated text.

---

## Problem Statement

Many beginners discover crochet inspiration through platforms like Pinterest, Instagram, Etsy, or handmade marketplaces, but struggle to find the actual pattern used to create the design.

Existing AI tools often generate inconsistent or structurally incorrect crochet instructions, which can result in warped shapes, incorrect stitch counts, or unusable patterns.

KnitWise AI was built to bridge that gap by turning visual crochet inspiration into readable and structured crochet guidance.

---

## Features

- Upload crochet reference images
- AI powered crochet structure analysis using Gemma 4
- Supports beanies, granny squares, and scarves
- Structured round by round pattern generation
- Beginner friendly formatting
- Strict Replication and Creative Adaptive modes
- Stitch count consistency handling
- Low image quality approximation warnings
- Printable PDF export
- Clean JSON response inspection

---

## Tech Stack

### Frontend
- React
- Vite
- Plain CSS

### Backend
- FastAPI
- Pydantic
- ReportLab

### AI & Processing
- Gemma 4 via Gemini API
- Multimodal image analysis
- Structured response schema validation

---

## System Architecture

```text
User Uploads Crochet Image
            ↓
Frontend Sends Request to FastAPI Backend
            ↓
Gemma 4 Multimodal Analysis via Gemini API
            ↓
Structured Validation using Pydantic Schemas
            ↓
Pattern Formatting & Geometry Handling
            ↓
PDF Generation using ReportLab
            ↓
Structured Crochet Pattern Returned to User
```

---

## How Gemma 4 Was Used

KnitWise AI uses the `gemma-4-26b-a4b-it` model through the Gemini API for multimodal image understanding and crochet pattern generation.

The model analyzes:
- crochet geometry
- stitch layouts
- structural shapes
- texture density
- pattern flow

Custom prompt engineering and structured schema validation were implemented to improve:
- stitch consistency
- shape accuracy
- beginner readability
- structured formatting

Different generation rules were designed for:
- circular beanies
- granny squares
- row based scarves

---

## Project Structure

```text
crochet-pattern-generator/
│
├── backend/
│   ├── main.py
│   ├── services.py
│   ├── pdf_generator.py
│   ├── requirements.txt
│   └── .env
│
└── frontend/
    ├── index.html
    ├── package.json
    ├── src/
    │   ├── main.jsx
    │   ├── App.jsx
    │   ├── App.css
    │   └── components/
    │       ├── PatternForm.jsx
    │       └── PatternDisplay.jsx
    └── vite.config.js
```

---

## Installation

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

Run the backend:

```bash
uvicorn main:app --reload
```

---

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## Usage

1. Upload a crochet reference image
2. Select:
   - Crochet type
   - Yarn size
   - Hook size
   - Generation mode
3. Generate the crochet pattern
4. View:
   - Structured rounds
   - Stitch counts
   - Notes
   - PDF export

---

## Example Output

### Supported Outputs Include

- Setup phases
- Round based instructions
- Stitch totals
- Geometry aware increases
- Construction notes
- Color change guidance
- PDF blueprint generation

---

## Challenges Faced

One of the biggest challenges was maintaining structural consistency during generation.

Crochet patterns follow strict construction logic depending on the geometry of the piece. Different handling was required for:
- circular beanies
- granny squares
- row based scarves

Additional validation logic and prompt constraints were introduced to reduce:
- inconsistent stitch counts
- warped geometry
- incorrect increases
- structurally invalid outputs

---

## Future Improvements

- Additional crochet structure support
- Stitch visualization overlays
- Yarn estimation system
- Crochet symbol diagram generation
- Interactive tutorials for beginners
- Multi language crochet terminology support

---

## Demo Video

https://youtu.be/CotVI4cWcf4

---


## Built For

The Gemma 4 Good Hackathon 2026 by Google DeepMind.

---

## Author

Varsha L.
