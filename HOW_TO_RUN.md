# 🚀 How to Run Event Management System in VS Code

> Note: Default setup uses SQLite. Use the Quick Start below. MySQL is optional.

## ▶️ Run Now (copy–paste)

- Mac / Linux (SQLite, recommended):
```bash
cd "/Users/samarthchoudhary/Desktop/DBMS event" && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && cp .env.example .env && python setup_database_sqlite.py && python app.py
```

- Windows (PowerShell):
```powershell
cd "C:\Users\samarthchoudhary\Desktop\DBMS event"; python -m venv venv; .\venv\Scripts\Activate.ps1; pip install -r requirements.txt; copy .env.example .env; python setup_database_sqlite.py; python app.py
```

- Windows (CMD):
```cmd
cd /d "C:\Users\samarthchoudhary\Desktop\DBMS event" && python -m venv venv && call venv\Scripts\activate.bat && pip install -r requirements.txt && copy .env.example .env && python setup_database_sqlite.py && python app.py
```

## 🔁 Reset and Rerun (if something breaks)

- Mac / Linux:
```bash
cd "/Users/samarthchoudhary/Desktop/DBMS event" && rm -rf venv instance && mkdir -p instance && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && cp .env.example .env && python setup_database_sqlite.py && python app.py
```

- Windows (PowerShell):
```powershell
cd "C:\Users\samarthchoudhary\Desktop\DBMS event"; Remove-Item -Recurse -Force venv, instance -ErrorAction SilentlyContinue; mkdir instance | Out-Null; python -m venv venv; .\venv\Scripts\Activate.ps1; pip install -r requirements.txt; copy .env.example .env; python setup_database_sqlite.py; python app.py
```

## ✅ Verify
- Terminal should show:
```
* Running on http://127.0.0.1:5001
```
- Open http://localhost:5001 and log in with admin / admin123.

## ❗ Connection Refused (localhost refused to connect)

If your browser says "localhost refused to connect" or "ERR_CONNECTION_REFUSED", follow these steps:

1. **Check if the Flask server is running:**
   - You must see this in your terminal:
     ```
      * Running on http://127.0.0.1:5001
     ```
   - If not, start it:
     ```bash
     python app.py
     ```

2. **If the server crashes or exits immediately:**
   - Read the error message in the terminal and fix any missing package, database, or import error.
   - Reinstall dependencies:
     ```bash
     source venv/bin/activate
     pip install -r requirements.txt
     ```
   - If using MySQL and it fails, switch back to SQLite in your `.env`:
     ```
     SQLALCHEMY_DATABASE_URI=sqlite:///instance/event_management.db
     ```
     Then run:
     ```bash
     python setup_database_sqlite.py
     python app.py
     ```

3. **Check if something else is using port 5001:**
   - Mac/Linux:
     ```bash
     lsof -nP -iTCP:5001 | grep LISTEN || echo "Nothing listening on 5001"
     ```
   - Windows (PowerShell):
     ```powershell
     netstat -ano | findstr :5001
     ```
   - If another process is using the port, kill it or change the port in `app.py` (e.g., `app.run(debug=True, port=5002)`).

4. **Ensure your `app.py` ends with:**
   ```python
   if __name__ == '__main__':
       app.run(debug=True, host='127.0.0.1', port=5001)
   ```

5. **Try a clean restart (SQLite):**
   ```bash
   cd "/Users/samarthchoudhary/Desktop/DBMS event"
   rm -rf venv instance
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   python setup_database_sqlite.py
   python app.py
   ```

6. **Test with curl (optional):**
   ```bash
   curl -v http://127.0.0.1:5001/
   ```
   - If you get "connection refused", the server is still not running.

7. **Other tips:**
   - Make sure you are in the project root directory.
   - Ensure the virtual environment is activated (`(venv)` in your prompt).
   - If you edited `.env`, make sure it matches the database you want to use.

### 1. Is the server running?
You must see this in the terminal:
```
 * Running on http://127.0.0.1:5001
```
If not present, start it:
```bash
python app.py
```

### 2. Check for immediate crash
If it exits or prints a traceback, fix the error (missing package, DB connection failure, bad import).
- Reinstall deps:
  ```bash
  source venv/bin/activate
  pip install -r requirements.txt
  ```
- If using MySQL and it fails, temporarily switch back to SQLite (.env SQLALCHEMY_DATABASE_URI=sqlite:///instance/event_management.db and rerun setup_database_sqlite.py).

### 3. Confirm port usage
Mac / Linux:
```bash
lsof -nP -iTCP:5001 | grep LISTEN || echo "Nothing listening on 5001"
```
Windows (PowerShell):
```powershell
netstat -ano | findstr :5001
```
If another process occupies the port, kill it or change the port (edit app.run(..., port=5002)).

### 4. Ensure correct app.run line
In app.py (last lines) should be:
```python
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)
```
Use host='0.0.0.0' only if you need external access:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### 5. Test reachability without browser
```bash
curl -v http://127.0.0.1:5001/
```
If connection refused, server still not running.

### 6. Clean restart (SQLite)
```bash
cd "/Users/samarthchoudhary/Desktop/DBMS event"
rm -rf venv instance
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python setup_database_sqlite.py
python app.py
```

### 7. Common hidden issues
- Wrong working directory: must be project root.
- Virtualenv not active: (venv) missing in prompt.
- Mixed MySQL config with no server running.
- Stale compiled files: remove __pycache__ directories (optional).

### 8. Alternative start (Flask CLI)
```bash
export FLASK_APP=app.py
export FLASK_DEBUG=1
flask run --port=5001
```
Windows (PowerShell):
```powershell
$Env:FLASK_APP="app.py"; $Env:FLASK_DEBUG="1"; flask run --port=5001
```

## 🔥 Quick Start (one-liners)

- Mac / Linux:
  ```bash
  cd "/Users/samarthchoudhary/Desktop/DBMS event" && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && cp .env.example .env && python setup_database_sqlite.py && python app.py
  ```

- Windows (PowerShell):
  ```powershell
  cd "C:\Users\samarthchoudhary\Desktop\DBMS event"; python -m venv venv; .\venv\Scripts\Activate.ps1; pip install -r requirements.txt; copy .env.example .env; python setup_database_sqlite.py; python app.py
  ```

- Windows (CMD):
  ```cmd
  cd /d "C:\Users\samarthchoudhary\Desktop\DBMS event" && python -m venv venv && call venv\Scripts\activate.bat && pip install -r requirements.txt && copy .env.example .env && python setup_database_sqlite.py && python app.py
  ```

## 🔁 Reset and Rerun (if something breaks)

- Mac / Linux:
```bash
cd "/Users/samarthchoudhary/Desktop/DBMS event" && rm -rf venv instance && mkdir -p instance && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && cp .env.example .env && python setup_database_sqlite.py && python app.py
```

- Windows (PowerShell):
```powershell
cd "C:\Users\samarthchoudhary\Desktop\DBMS event"; Remove-Item -Recurse -Force venv, instance -ErrorAction SilentlyContinue; mkdir instance | Out-Null; python -m venv venv; .\venv\Scripts\Activate.ps1; pip install -r requirements.txt; copy .env.example .env; python setup_database_sqlite.py; python app.py
```

## ✅ Quick Troubleshooting (common failures)

- Prefer SQLite first. Only follow MySQL steps if you intentionally switched to MySQL.

- "python: command not found"
  - Use python3 instead of python (Mac/Linux) or ensure Windows PATH includes Python.

- "No module named flask"
  - Make sure the virtualenv is activated (you see (venv) in the prompt) and rerun:
    ```bash
    pip install -r requirements.txt
    ```

- "Port 5001 already in use"
  - Kill the process using the port or change port when running:
    ```bash
    # mac/linux
    lsof -ti:5001 | xargs kill
    # or run on different port
    python app.py  # edit last line to app.run(debug=True, port=5002) or set env FLASK_RUN_PORT
    ```

- "Database file missing" or "OperationalError"
  - Ensure you ran setup_database_sqlite.py and that instance/event_management.db exists:
    ```bash
    python setup_database_sqlite.py
    ```

- "Can't connect to MySQL server"
  - Ensure MySQL service is running:
    ```bash
    # Mac:
    brew services start mysql
    # Windows: Check MySQL service in Task Manager
    # Linux:
    sudo systemctl status mysql
    ```

- "Access denied for user"
  - Check your MySQL credentials in .env file
  - Verify user exists and has proper permissions:
    ```bash
    mysql -u root -p
    SELECT User, Host FROM mysql.user WHERE User='event_user';
    SHOW GRANTS FOR 'event_user'@'localhost';
    ```

- "Unknown database 'event_management'"
  - Create the database:
    ```bash
    mysql -u root -p
    CREATE DATABASE event_management;
    ```

- "No module named PyMySQL"
  - Install MySQL dependencies:
    ```bash
    source venv/bin/activate
    pip install PyMySQL cryptography
    ```

---

# 🚀 How to Run Event Management System with MySQL Database

## 📋 Prerequisites

### 1. Install Python
```bash
# Check if Python is installed
python --version
# or
python3 --version

# Should show: Python 3.8 or higher
```

**If not installed:**
- Download from: https://www.python.org/downloads/
- Install Python 3.8 or higher

---

### 2. Install MySQL Server
```bash
# Check if MySQL is installed
mysql --version

# Should show: mysql Ver 8.0 or higher
```

**If not installed:**

**Mac (using Homebrew):**
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install MySQL
brew install mysql

# Start MySQL service
brew services start mysql

# Secure installation (set root password)
mysql_secure_installation
```

**Windows:**
- Download from: https://dev.mysql.com/downloads/mysql/
- Install MySQL Server 8.0+
- Remember the root password you set during installation

**Ubuntu/Linux:**
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

### 3. Create Database
```bash
# Connect to MySQL as root
mysql -u root -p

# Create database and user
CREATE DATABASE event_management;
CREATE USER 'event_user'@'localhost' IDENTIFIED BY 'your_password_here';
GRANT ALL PRIVILEGES ON event_management.* TO 'event_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 4. Install VS Code
- Download from: https://code.visualstudio.com/
- Install Python extension in VS Code

---

## 🔧 Setup Steps (First Time Only)

### Step 1: Open Project in VS Code

**Option A: From VS Code**
```
1. Open VS Code
2. File → Open Folder
3. Navigate to: /Users/samarthchoudhary/Desktop/DBMS event
4. Click "Open"
```

**Option B: From Terminal**
```bash
cd "/Users/samarthchoudhary/Desktop/DBMS event"
code .
```

---

### Step 2: Create Virtual Environment

**Open VS Code Terminal:**
- Menu: Terminal → New Terminal
- Or press: `` Ctrl + ` `` (backtick)

**Run these commands:**

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# You should see (venv) in terminal prompt
```

---

### Step 3: Install Dependencies (Updated for MySQL)

```bash
# Make sure venv is activated (you see (venv) in prompt)
pip install -r requirements.txt
pip install PyMySQL cryptography
```

**Expected output:**
```
Installing collected packages: Flask, Flask-SQLAlchemy, python-dotenv, PyMySQL, cryptography...
Successfully installed Flask-3.0.0 Flask-SQLAlchemy-3.1.1 PyMySQL-1.1.0...
```

---

### Step 4: Configure Environment (Updated for MySQL)

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file for MySQL
code .env
```

**Your .env should contain:**
```env
SECRET_KEY=your-secret-key-here
SQLALCHEMY_DATABASE_URI=mysql+pymysql://event_user:your_password_here@localhost/event_management

# MySQL Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=event_user
MYSQL_PASSWORD=your_password_here
MYSQL_DATABASE=event_management
```

---

### Step 5: Setup Database (Updated for MySQL)

```bash
# Create database tables
python setup_database_mysql.py
```

**Expected output:**
```
Connected to MySQL successfully!
Database setup complete!
Default admin user created:
Username: admin
Email: admin@gmail.com
Password: admin123
```

---

## ▶️ Running the Application

### Method 1: Using Terminal (Recommended)

```bash
# Make sure you're in project folder
cd "/Users/samarthchoudhary/Desktop/DBMS event"

# Activate virtual environment (if not already active)
source venv/bin/activate    # Mac/Linux
# or
venv\Scripts\activate       # Windows

# Start MySQL service (if not running)
# Mac:
brew services start mysql
# Windows: Start MySQL from Services or MySQL Workbench
# Linux:
sudo systemctl start mysql

# Run Flask application
python app.py
```

**Expected output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server.
 * Running on http://127.0.0.1:5001
Press CTRL+C to quit
 * Restarting with stat
```

---

### Method 2: Using VS Code Run Button

**Setup launch.json:**

1. Click **Run and Debug** icon (left sidebar)
2. Click **"create a launch.json file"**
3. Select **"Python"**
4. Select **"Python File"**

**Or manually create `.vscode/launch.json`:**
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "debugpy",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "app.py",
                "FLASK_DEBUG": "1"
            },
            "args": [
                "run",
                "--port=5001"
            ],
            "jinja": true,
            "autoReload": {
                "enable": true
            }
        }
    ]
}
```

**Then:**
1. Press **F5** or click **Start Debugging** (green play button)
2. Application will start on http://localhost:5001

---

### Method 3: Using VS Code Tasks

**Create `.vscode/tasks.json`:**
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run Flask App",
            "type": "shell",
            "command": "${workspaceFolder}/venv/bin/python",
            "args": ["app.py"],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "presentation": {
                "reveal": "always",
                "panel": "new"
            }
        }
    ]
}
```

**Then:**
1. Terminal → Run Task
2. Select **"Run Flask App"**

---

## 🌐 Accessing the Application

### Once Server is Running:

**Open Browser and go to:**
```
http://localhost:5001
```

**Or:**
```
http://127.0.0.1:5001
```

### VS Code Shortcuts:
- **Ctrl + Click** on the URL in terminal
- Or click the **"Open in Browser"** popup

---

## 🔑 Login Credentials

### Default Admin Account
```
Username: admin
Email:    admin@gmail.com
Password: admin123
```

---

## 🛠️ VS Code Extensions (Recommended)

### Essential Extensions:

1. **Python** (Microsoft)
   - Syntax highlighting
   - Debugging support
   - IntelliSense

2. **Pylance** (Microsoft)
   - Advanced Python language support
   - Type checking

3. **SQLite** (alexcvzz)
   - View database contents
   - Run SQL queries

4. **HTML CSS Support** (ecmel)
   - HTML/CSS autocomplete
   - Class/ID suggestions

5. **Jinja** (wholroyd)
   - Jinja2 template syntax highlighting
   - Autocomplete for templates

### Install Extensions:
```
1. Click Extensions icon (left sidebar)
2. Search for extension name
3. Click "Install"
```

---

## 📂 VS Code Workspace Settings

**Create `.vscode/settings.json`:**
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "autopep8",
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    },
    "files.associations": {
        "*.html": "jinja-html"
    },
    "emmet.includeLanguages": {
        "jinja-html": "html"
    }
}
```

---

## 🐛 Debugging in VS Code

### Set Breakpoints:
1. Click left of line number (red dot appears)
2. Press **F5** to start debugging
3. Code will pause at breakpoint

### Debug Actions:
- **F5** - Continue
- **F10** - Step Over
- **F11** - Step Into
- **Shift+F11** - Step Out
- **Shift+F5** - Stop

### View Variables:
- **Variables** panel shows current values
- **Watch** panel for custom expressions
- **Call Stack** shows function calls

---

## 📁 Project Structure in VS Code

```
DBMS/
├── 📄 app.py                     ← Main Flask application
├── 📄 models.py                  ← Database models
├── 📄 config.py                  ← Configuration
├── 📄 requirements.txt           ← Dependencies
├── 📄 .env                       ← Environment variables (MySQL config)
├── 📄 setup_database_mysql.py    ← MySQL database setup
│
├── 📁 templates/                 ← HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── auth/
│   ├── events/
│   ├── guests/
│   └── bookings/
│
├── 📁 instance/                  ← Database folder
│   └── event_management.db
│
└── 📁 venv/                      ← Virtual environment
```

---

## 🔄 Common Workflows

### Starting Your Work Session:

```bash
# 1. Open project in VS Code
cd "/Users/samarthchoudhary/Desktop/DBMS event"
code .

# 2. Open terminal in VS Code (Ctrl + `)

# 3. Activate virtual environment
source venv/bin/activate    # Mac/Linux
# or
venv\Scripts\activate       # Windows

# 4. Run application
python app.py

# 5. Open browser
# http://localhost:5001
```

---

### Making Changes:

```bash
# 1. Edit your files in VS Code

# 2. Save changes (Ctrl + S)

# 3. Server auto-reloads (if debug mode on)
#    Or restart manually (Ctrl + C, then python app.py)

# 4. Refresh browser to see changes
```

---

### Stopping the Server:

```bash
# In terminal where server is running:
# Press Ctrl + C

# Deactivate virtual environment:
deactivate
```

---

## ⚡ Quick Commands

### Terminal Commands:

```bash
# Activate venv
source venv/bin/activate         # Mac/Linux
venv\Scripts\activate            # Windows

# Install new package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# Run application
python app.py

# Setup database
python setup_database_mysql.py

# Deactivate venv
deactivate
```

---

## 🎨 VS Code Keyboard Shortcuts

### Essential Shortcuts:

```
Ctrl + `          - Open/Close Terminal
Ctrl + B          - Toggle Sidebar
Ctrl + P          - Quick File Open
Ctrl + Shift + P  - Command Palette
Ctrl + /          - Toggle Comment
Ctrl + F          - Find in File
Ctrl + Shift + F  - Find in All Files
F5                - Start Debugging
Ctrl + C          - Stop Server
Ctrl + S          - Save File
Alt + ↑/↓         - Move Line Up/Down
Shift + Alt + ↓   - Duplicate Line
```

---

## 🔍 Viewing Database in VS Code

### Using SQLite Extension:

1. **Install SQLite Extension**
   ```
   Extensions → Search "SQLite" → Install
   ```

2. **Open Database**
   ```
   Right-click instance/event_management.db
   → Open Database
   ```

3. **View Tables**
   ```
   SQLite Explorer panel (left sidebar)
   → Expand database
   → Click table to view data
   ```

4. **Run Queries**
   ```
   Right-click database
   → New Query
   → Write SQL
   → Run (Ctrl + Shift + Q)
   ```

---

## 📊 Monitoring Logs

### View Flask Logs in Terminal:

```
127.0.0.1 - - [15/Oct/2025 02:16:23] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [15/Oct/2025 02:16:24] "GET /events HTTP/1.1" 200 -
```

**What they mean:**
- IP address
- Timestamp
- HTTP method + URL
- Status code (200 = success)

---

## 🚨 Troubleshooting

### Issue 1: "python: command not found"
```bash
# Use python3 instead
python3 --version
python3 app.py
```

### Issue 2: "No module named flask"
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 3: "Port 5001 already in use"
```bash
# Find and kill process using port 5001
# Mac/Linux:
lsof -ti:5001 | xargs kill

# Windows:
netstat -ano | findstr :5001
taskkill /PID [PID_NUMBER] /F

# Or change port in app.py:
# app.run(debug=True, port=5002)
```

### Issue 4: "Template not found"
```bash
# Make sure you're in project root
cd "/Users/samarthchoudhary/Desktop/DBMS event"

# Run from correct directory
python app.py
```

### Issue 5: Virtual environment not activating
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue 6: "Can't connect to MySQL server"
```bash
# Ensure MySQL service is running
# Mac:
brew services start mysql
# Windows: Check MySQL service in Task Manager
# Linux:
sudo systemctl status mysql
```

### Issue 7: "Access denied for user"
```bash
# Check your MySQL credentials in .env file
# Verify user exists and has proper permissions:
mysql -u root -p
SELECT User, Host FROM mysql.user WHERE User='event_user';
SHOW GRANTS FOR 'event_user'@'localhost';
```

### Issue 8: "Unknown database 'event_management'"
```bash
# Create the database:
mysql -u root -p
CREATE DATABASE event_management;
```

### Issue 9: "No module named PyMySQL"
```bash
# Install MySQL dependencies:
source venv/bin/activate
pip install PyMySQL cryptography
```

---

## 📝 Development Tips

### 1. Auto-Reload (Debug Mode)
```python
# In app.py (last line):
if __name__ == '__main__':
    app.run(debug=True, port=5001)
```
- Changes auto-reload
- Better error messages
- Interactive debugger

### 2. Multiple Terminal Windows
```
Terminal → Split Terminal
```
- One for server
- One for commands

### 3. Quick File Navigation
```
Ctrl + P → Type filename → Enter
```

### 4. Format Code
```
Right-click → Format Document
Or: Shift + Alt + F
```

### 5. Git Integration
```
Source Control icon (left sidebar)
- View changes
- Commit changes
- Push to GitHub
```

---

## 🎯 Complete Workflow Example

### First Time Setup:
```bash
# 1. Open VS Code
code "/Users/samarthchoudhary/Desktop/DBMS event"

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
pip install PyMySQL cryptography

# 5. Start MySQL service
brew services start mysql    # Mac
# or check if MySQL is running on Windows/Linux

# 6. Create MySQL database and user (if not done)
mysql -u root -p
# Run CREATE DATABASE and CREATE USER commands

# 7. Configure .env file with MySQL credentials
cp .env.example .env
code .env    # Edit with your MySQL settings

# 8. Setup database
python setup_database_mysql.py

# 9. Run application
python app.py

# 10. Open browser
# http://localhost:5001

# 11. Login with admin/admin123
```

### Daily Development:
```bash
# 1. Open VS Code
code "/Users/samarthchoudhary/Desktop/DBMS event"

# 2. Activate venv
source venv/bin/activate

# 3. Run app
python app.py

# 4. Start coding!
```