# 🧠 Math Microservice API

This project is a production-ready Python microservice that exposes an API for solving basic mathematical operations:

- ✅ Power (`/pow`)
- ✅ Factorial (`/factorial`)
- ✅ N-th Fibonacci number (`/fibonacci`)

Each API request is logged to a SQLite database, and the logs can be queried, filtered, paginated, and exported in both `.csv` and `.json` formats.

---

## 🚀 Features

- Built with **Flask** using Blueprint + App Factory pattern
- Clean separation of concerns: **Controllers**, **Services**, **Models**
- **Request logging** with SQLAlchemy + SQLite
- **Filterable & paginated** `/logs` endpoint
- **Downloadable** logs via:
  - `/logs/export` → CSV
  - `/logs/export.json` → JSON
- **Input validation & error handling**
- Fully tested with `pytest` (10+ unit + integration tests)
- Zero warnings, modern code style

---

## 🧪 How to Run

1. Clone the project or unzip the folder  
2. Install dependencies:
   ```bash
   pip install flask sqlalchemy pytest
