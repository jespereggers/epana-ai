from flask import redirect, render_template, session
from functools import wraps
import zipfile
import io
from datetime import datetime


def login_required(f):
    """
    Decorate routes to require login.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def get_zip_as_text(file):
    if file and file.filename.endswith(".zip"):
        try:
            # Öffne die hochgeladene ZIP-Datei im Speicher
            with zipfile.ZipFile(io.BytesIO(file.read())) as zip_ref:
                # Liste alle Dateien in der ZIP auf
                for file_info in zip_ref.infolist():
                    print(f"Extracting file: {file_info.filename}")

                    # Lese den Inhalt der Dateien in der ZIP
                    with zip_ref.open(file_info) as extracted_file:
                        # Versuche, die Datei als Text zu lesen
                        try:
                            file_contents = extracted_file.read().decode("utf-8")
                            print(f"Contents of {file_info.filename}:")
                            return file_contents
                        except UnicodeDecodeError as e:
                            print(f"Error reading {file_info.filename}: {e}")
        except zipfile.BadZipFile:
            print("The uploaded file is not a valid zip file.")
    else:
        print("No valid zip file was uploaded or file is empty")

    return "Empty"


def extract_timespan(text):
    # Split the text by lines
    lines = text.strip().splitlines()

    # Extract the date from the first and last line, removing brackets and other characters
    first_line_date = lines[0].split(']')[0][1:].split(',')[0].strip()
    last_line_date = lines[-1].split(']')[0][1:].split(',')[0].strip()

    # Convert the dates from DD.MM.YY to YYYY-MM-DD
    start_date = datetime.strptime(first_line_date, "%d.%m.%y").strftime("%Y-%m-%d")
    end_date = datetime.strptime(last_line_date, "%d.%m.%y").strftime("%Y-%m-%d")

    return start_date, end_date


def extract_name(text):
    # Split the text by lines
    lines = text.strip().splitlines()

    # Extract the part after "] " and before ":"
    first_line = lines[0]
    name = first_line.split("] ")[1].split(":")[0]

    return name


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code
