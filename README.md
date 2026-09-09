# Book Library API (FastAPI + MongoDB Atlas)

A complete, production-ready RESTful API for managing a book collection. Built with **FastAPI**, **Motor** (async MongoDB driver), and **Pydantic v2**.

---

## Overview & Requirements

This project provides a full-featured backend API for book management:
1. **Full Async CRUD Operations**: Endpoints to Create, Read (all or single), Update, and Delete books.
2. **MongoDB Atlas Integration**: Non-blocking connection pooling managed via Motor lifecycle hooks.
3. **Data Model Validation**: Enforces year constraints (`1000 < year <= current_year`), default stock settings, and non-empty string constraints.
4. **Error Handling**: Custom JSON error structures for invalid ObjectIDs (`400 Bad Request`), missing entities (`404 Not Found`), and empty update payloads.

---

## Prerequisites

Before running the project locally, ensure you have:
- **Python 3.10+** installed on your machine.
- An active **MongoDB Atlas** cluster (or a local MongoDB instance).
- `git` or an unzipped folder containing the repository files.

---

## Local Setup & Running Instructions

### Step 1: Navigate to the Project Directory
Open your terminal or command prompt and change directory into the root folder:
Command:
  cd book-library-api

### Step 2: Set Up a Virtual Environment
Create and activate an isolated Python virtual environment:
Command:
  python -m venv venv
  venv\Scripts\activate.bat

### Step 3: Install Dependencies
Ensure pip is updated, then install all project dependencies from requirements.txt:
Command:
  pip install --upgrade pip
  pip install -r requirements.txt

### Step 4: Configure Environment Variables
Create a .env file from the provided .env.example template:
  copy .env.example .env
Open .env in a text editor and configure your environment settings:
  MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority
  DATABASE_NAME=library_db
  COLLECTION_NAME=books
  PORT=8000

### Step 5: Start the Local Development Server
Launch the FastAPI application server using uvicorn:
Command:
  uvicorn app.main:app --reload --port 8000
The application will now be running locally at http://127.0.0.1:8000.
