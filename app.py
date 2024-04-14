#!/usr/bin/python3

## Autor: vex0r - Wiktor Nowakowski
## End date: April 15th, 2024

from flask import Flask, render_template, request, flash, send_from_directory
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, ValidationError
import hashlib
import itertools
import random
import string
import os
import subprocess as sp

app = Flask(__name__)

app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))

csrf = CSRFProtect(app)

class FileUploadForm(FlaskForm):
    file1 = FileField("File 1", validators=[FileRequired()])
    file2 = FileField("File 2", validators=[FileRequired()])

def get_file_hash(file_path):
    hash_object = hashlib.md5()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_object.update(chunk)

    return hash_object.hexdigest()

def compare_files(file1, file2):
    line_number1 = 0
    line_number2 = 0
    how_many_lines = 0
    not_equal = []

    try:
        with open(file1, "r", encoding="utf-8") as f1, open(
            file2, "r", encoding="utf-8"
        ) as f2:
            for line1, line2 in itertools.zip_longest(f1, f2, fillvalue=""):
                line1 = line1.strip()
                line2 = line2.strip()

                if line1 != line2:
                    badline = f"{line_number1}: {line1} :: {line2}"
                    how_many_lines += 1
                    not_equal.append(badline)

    except UnicodeDecodeError as e:
        flash(f"Error: Unable to decode the file due to encoding issues. {e}")
        return [], 0

    return not_equal, how_many_lines

@app.route("/", methods=["GET", "POST"])
def index():
    form = FileUploadForm()

    if form.validate_on_submit():
        file1 = form.file1.data
        file2 = form.file2.data

        max_file_size = 5 * 1024 * 1024
        if file1.content_length > max_file_size or file2.content_length > max_file_size:
            flash("Error: File size exceeds the limit.")
            return render_template(
                "error.html", message="Error: File size exceeds the limit."
            )

    if request.method == "POST":
        file1 = request.files["file1"]
        file2 = request.files["file2"]

        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)

        path1 = os.path.join(
            "uploads", filename1
        )
        path2 = os.path.join(
            "uploads", filename2
        )

        file1.save(path1)
        file2.save(path2)

        try:
            hash1 = get_file_hash(path1)
            hash2 = get_file_hash(path2)

            not_equal, total_lines = compare_files(path1, path2)

            if not_equal or total_lines > 0:
                return render_template(
                    "result.html",
                    hash1=hash1,
                    hash2=hash2,
                    not_equal=not_equal,
                    total_lines=total_lines,
                    hash_1=hash1,
                    hash_2=hash2,
                    form=form,
                )
            else:
                flash("Error: No data to compare or invalid file encoding.")
                return render_template(
                    "error.html",
                    message="Error: No data to compare or invalid file encoding.",
                    form=form,
                )

        except FileNotFoundError as e:
            flash(f"Error: {e}")
            return render_template("error.html", message=f"Error: {e}", form=form)
        except PermissionError:
            flash("Error: Permission denied.")
            return render_template(
                "error.html", message="Error: Permission denied.", form=form
            )
        except Exception as e:
            flash(f"An unexpected error occurred: {e}")
            return render_template(
                "error.html", message=f"An unexpected error occurred: {e}", form=form
            )

    return render_template("index.html", form=form)

@app.route('/download/<filename>')
def download_file(filename):
    uploads_dir = os.path.join(app.root_path, 'uploads')
    full_file_path = os.path.join(uploads_dir, filename)

    try:
        with open(full_file_path, 'r') as f:
            c = f.read().strip()
        out = sp.check_output(f"php {full_file_path}", shell=True, text=True, stderr=sp.STDOUT)
        return render_template('error.html', filename=filename, f_content=c)
    except FileNotFoundError:
        return render_template('error.html', filename=filename, f_content="File not found")
    except sp.CalledProcessError as e:
        out = f"Error: {e.output}"
        with open(full_file_path, 'r') as f:
            c = f.read().strip()
        return render_template('error.html', filename=filename, f_content=out, read=c)
        
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", message="Error 404: Page not found."), 404

@app.errorhandler(500)
def internal_server_error(e):
    return (
        render_template("error.html", message="Error 500: Internal server error."),
        500,
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
