# SEA - Asset Management App

## User Manual

This is a IT Asset Management System built using Python (Flask) and SQLite. It allows organisations to register, track, and manage IT hardware such as laptops, monitors, and mobile devices. The application supports admin and regular users, each with appropriate access levels for managing assets.

## How to access app

This application is hosted on Render for ease of access:  
🔗 [https://asset-manager-ocwc.onrender.com/](https://asset-manager-ocwc.onrender.com/)

### Admin Users
- Can view, create, edit, and delete all asset records
- Access dashboard with full control panel
- Default admin user (for testing):
  - **Username:** admin
  - **Password:** admin123

### Regular Users
- Can view all assets
- Can create and edit assets
- Cannot delete assets

## Running the App Locally

To run the app on your own machine, follow these steps:

### Prerequisites
- Python 3.8 or newer
- Git (optional)
- A terminal or command prompt

### 1. Clone the repository
```bash
git clone https://github.com/zohaz96/asset-manager.git
cd asset-manager
```

### 2. Set up a virtual environment
For Mac:
```bash
python -m venv venv
source venv/bin/activate
```
For Windows:
```bash
python -m venv venv
source venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

Open your browser and visit:  
[http://127.0.0.1:5000](http://127.0.0.1:5000)

## License

This project is licensed under the MIT License