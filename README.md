# CLI Task Manager

## Overview
A Python-based command-line interface (CLI) application designed for structured task assignment, user authentication, and automated report generation. This project serves as a showcase for managing persistent data using flat-file storage and implementing custom logic for reporting and analytics.

## Technical Methodology
* **Language**: Python 3
* **Data Persistence**: Uses standard file I/O (`tasks.txt` and `user.txt`) to maintain state between sessions.
* **Core Functionality**:
    * **User Auth**: Role-based access control (Admin vs. Standard User).
    * **CRUD**: Create, read, update, and delete functionality for task tracking.
    * **Reporting**: Automated algorithm to calculate completion percentages and identify overdue tasks.

## Security & Architectural Perspective
This project demonstrates the full lifecycle of data manipulation. 
* *Security Note*: While this implementation uses flat-file storage for educational transparency, it serves as a foundation for understanding the importance of secure credential handling and database integration. I am actively expanding this logic to include `bcrypt` password hashing and secure SQL database backends.

## How to Run
1. Ensure Python is installed.
2. Run the script: `python task_manager.py`
