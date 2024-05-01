## **Guide to installing Python-Dominos from the source code**

### **Step 1: Download the source code from Github**

First, you need to download the source code of Python Dominos from Github. You can access the project's Github page at: [https://github.com/dinhthinh6/python-dominos/releases/tag/v.1.0.0](https://github.com/dinhthinh6/python-dominos/releases/tag/v.1.0.0)

Download the latest version of the python-dominos.zip file that corresponds to your operating system. Proceed to download and extract it.

### **Step 2: Install Python (if you don't have Python already installed)**

Python Dominos Game is written in Python, so you need to install Python on your computer if you don't already have it. You can download the latest version of Python from the official Python website at [https://www.python.org/downloads/](https://www.python.org/downloads/).

After downloading, install Python using the downloaded .exe file.

### **Step 3: Install necessary libraries**

You can install the necessary libraries using the requirements.txt file that comes with the Python Dominos source code. Open Command Prompt or Terminal and navigate to the directory that contains the application source code, then run the following command to install the necessary libraries:

- Windows

```powershell
pip install -r requirements.txt
```

The above command will install all the necessary libraries to run the Python Dominos application.

- Linux

If pip is not installed, use the following command to install pip:

```powershell
sudo apt-get update
sudo apt-get install python3-pip
```

Next, run this command to install the libraries:

```powershell
pip install -r requirements.txt
```

### **Step 4: Run the application**

After installing Python and the necessary libraries, you can run the Python Dominos application. Open Command Prompt or Terminal and navigate to the directory that contains the application's source code.

Run the following command to start the application:

```powershell
python run.py
```

Or

```powershell
python3 run.py
```

Then, the Python Dominos application will start up and display on the screen.
