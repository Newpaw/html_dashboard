# User-Uploaded HTML Dashboard

This project is a simple web application built with **Flask** that allows users to upload a custom HTML file (named `index.html`) and an optional CSV data file (which is saved as `data.csv`). The application then serves this custom HTML file, making it possible to create dynamic dashboards or web pages powered by the uploaded data.

The application includes a user-friendly interface for managing the uploaded files, allowing you to:

  * **Upload** a new `index.html` file.
  * **Upload** an optional `data.csv` file.
  * **View** the original filenames of the uploaded files.
  * **Delete** the currently uploaded files to upload new ones.

-----

## File Structure

The project has a straightforward file structure, which is easy to navigate:

```
html_dashboard/
├── .venv/                   # Python virtual environment
├── templates/               # Flask templates
│   └── upload.html          # The upload and file management page
├── uploaded_files/          # Directory where user files are stored
├── app.py                   # The main Flask application file
└── requirements.txt         # Project dependencies
```

-----

## How to Run

Follow these steps to set up and run the application locally.

### Prerequisites

  * Python 3.6 or higher

### 1\. Create and Activate a Virtual Environment

It's a best practice to use a virtual environment to manage dependencies for your project.

```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

### 2\. Install Dependencies

Install the required Python packages using `pip`.

```bash
pip install Flask gunicorn
# or from requirements.txt
pip install -r requirements.txt
```

### 3\. Run the Application

Execute the `app.py` file to start the Flask development server.

```bash
python app.py
```

The application will now be running on `http://127.0.0.1:5000`. Open this URL in your web browser to start uploading files.

-----

## Usage

1.  **Navigate to the home page (`/`)**. If no `index.html` is present, you will be automatically redirected to the file upload page.
2.  **Upload files**. On the `/upload_files` page, you can select an HTML file and an optional CSV file.
      * The HTML file will be saved as `index.html`.
      * The CSV file will be saved as `data.csv`.
3.  **Manage files**. The upload page will display a list of currently uploaded files, showing their original names and providing a **"Delete"** button for each.
4.  **View the dashboard**. Once an `index.html` file is uploaded, you can access your custom web page at the `/o2site` endpoint. This is where your uploaded HTML and its associated data will be displayed.