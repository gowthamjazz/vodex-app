# Vodex App
Thanks for the opertunity
## Overview

Vodex App is a FastAPI application that performs CRUD (Create, Read, Update, Delete) operations for **Items** and **User Clock-In Records**. The application uses MongoDB as its database and is documented using Swagger UI.

## Features

- **Items API**
  - Create a new item.
  - Retrieve an item by ID.
  - Filter items based on email, expiry date, insert date, and quantity.
  - Aggregate items to count the number per email.
  - Update an item by ID.
  - Delete an item by ID.

- **Clock-In Records API**
  - Create a new clock-in record.
  - Retrieve a clock-in record by ID.
  - Filter clock-in records based on email, location, and insert datetime.
  - Update a clock-in record by ID.
  - Delete a clock-in record by ID.

## Technologies Used

- **FastAPI**: Web framework for building APIs.
- **MongoDB**: NoSQL database.
- **Motor**: Asynchronous MongoDB driver.
- **Pydantic**: Data validation and settings management.
- **Uvicorn**: ASGI server for running FastAPI applications.

## Setup Instructions

### Prerequisites

- **Python 3.7+**
- **pip** (Python package installer)
- **MongoDB Atlas Account** or **Local MongoDB Instance**
- **Git**
- **Heroku CLI** (if deploying on Heroku) or **Koyeb Account** (if deploying on Koyeb)

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/gowthamjazz/vodex-app.git
   cd vodex-app
