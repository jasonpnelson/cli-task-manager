# CLI Task Manager

## Overview

A Python-based command-line interface (CLI) application for structured task assignment, user authentication, and automated report generation. Demonstrates managing persistent data with flat-file storage and implementing custom logic for reporting and analytics.

## Technical Methodology

- **Language**: Python 3
- **Data Persistence**: Standard file I/O (`tasks.txt` and `user.txt`) to maintain state between sessions.
- **Core Functionality**:
  * **User Authentication**: Role-based access control separating admin and standard user permissions.
  * **CRUD**: Create, read, update, and delete functionality for task tracking.
  * **Reporting**: Automated calculation of completion percentages and identification of overdue tasks.

## Security Note

This implementation uses flat-file storage with plaintext credentials, which is appropriate for a learning exercise but not for production. In a real system, passwords would be hashed with a slow algorithm such as bcrypt, credentials would live in a database rather than a text file, and access control would be enforced server-side rather than in client logic.

## How to Run

1. Ensure Python 3 is installed.
2. Run the script: `python task_manager.py`
