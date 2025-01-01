from flask import Flask, request, jsonify, send_from_directory
import os
import xml.etree.ElementTree as ET
import logging
import csv

from xml.dom import minidom

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__, static_folder='static')

@app.before_request
def log_request_info():
    logger.info(f"Handling request: {request.method} {request.path}")

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'xmlView.html')

@app.route('/generate-xml', methods=['POST'])
def generate_xml():
    # Ensure a file is uploaded
    if 'txtFile' not in request.files and 'txtFile2' not in request.files: 
        return "No file uploaded", 400

    form_type = ""
    
    if 'txtFile' in request.files:
        file = request.files['txtFile']
        delimiter = request.form.get('delimiter', '，')
        form_type = "1"
    else: 
        file = request.files['txtFile2']
        delimiter = request.form.get('delimiter2', '，')
        form_type = "2"

    if file.filename == '':
        return "No file selected", 400

    # Save the file temporarily
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        # Parse the TXT file and generate XML
        xml_content = generate_xml_from_file(filepath, delimiter, form_type)
        
        # Save XML content to a temporary file
        xml_filename = os.path.splitext(file.filename)[0] + ".xml"
        xml_filepath = os.path.join(UPLOAD_FOLDER, xml_filename)
        with open(xml_filepath, 'w', encoding='utf-8') as xml_file:
            xml_file.write(xml_content)

        # Return XML content as response
        return xml_content, 200, {'Content-Type': 'application/xml'}
    except FileNotFoundError:
        return "Input file not found", 404
    except ValueError as ve:
        return f"Error: {str(ve)}", 400
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return f"Error: {str(e)}", 500
    finally:
        # Clean up the uploaded file
        if os.path.exists(filepath):
            os.remove(filepath)
            
def generate_xml_from_file(filepath, delimiter='，', form_type="1"):
    
    """
    Generate XML content from a CSV or TXT file.
    
    Args:
        filepath (str): Path to the input file (.csv or .txt).
        delimiter (str): Delimiter for splitting fields in TXT files.

    Returns:
        str: XML content as a string.
    """
    # Determine file type and process accordingly
    if filepath.endswith('.csv'):
        return csv_to_xml(filepath)
    elif filepath.endswith('.txt'):
        if form_type == "1":
            return txt_to_xml(filepath, delimiter)
        else:
            return txt_to_xml_normal(filepath, delimiter)
    else:
        raise ValueError("Unsupported file format. Only .csv and .txt are supported.")

def txt_to_xml(filepath, delimiter='，'):
    # Read the TXT file
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Create the root element
    root = ET.Element('books')

    for line in lines:
        fields = line.strip().split(delimiter)
        if len(fields) != 5:
            raise ValueError("Each line must contain exactly 5 fields: ID, Title, Category, Author, Price.")

        # Extract fields
        book_id, title, category, author, price = fields

        # Create a book element with ID and category as attributes
        book = ET.SubElement(root, "book", id=book_id, category=category)

        # Add sub-elements for title, author, and price
        ET.SubElement(book, "title").text = title.strip()
        ET.SubElement(book, "author").text = author.strip()
        ET.SubElement(book, "price").text = price.strip()

    # Pretty-print XML using minidom
    rough_string = ET.tostring(root, encoding='unicode', method='xml')
    reparsed = minidom.parseString(rough_string)
    
    # Add encoding="UTF-8" to the XML declaration
    pretty_xml = reparsed.toprettyxml(indent="  ")
    # Replace the default XML declaration with the one that includes encoding
    return pretty_xml.replace('<?xml version="1.0" ?>\n', '<?xml version="1.0" encoding="UTF-8" ?>\n')

def txt_to_xml_normal(filepath, delimiter='，'):
    # Create the root element for XML
    root = ET.Element("data")

    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()
        
        # Process each line of the file
        for i, line in enumerate(lines):
            # Create a record for each line
            record = ET.SubElement(root, "record", id=str(i + 1))
            
            # Split the line into fields based on the delimiter
            fields = line.strip().split(delimiter)
            
            # Add a field element for each value in the line
            for j, field in enumerate(fields):
                field_tag = f"field{j + 1}"
                ET.SubElement(record, field_tag).text = field.strip()

    # Pretty-print XML using minidom
    rough_string = ET.tostring(root, encoding='unicode', method='xml')
    reparsed = minidom.parseString(rough_string)
    
    # Add encoding="UTF-8" to the XML declaration
    pretty_xml = reparsed.toprettyxml(indent="  ")
    # Replace the default XML declaration with the one that includes encoding
    return pretty_xml.replace('<?xml version="1.0" ?>\n', '<?xml version="1.0" encoding="UTF-8" ?>\n')


def csv_to_xml(filepath):
    # Read the CSV file
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        root = ET.Element('root')

        for i, row in enumerate(reader):
            record = ET.SubElement(root, "record", id=str(i + 1))
            for j, field in enumerate(row):
                ET.SubElement(record, f"field{j + 1}").text = field.strip()

    # Convert to XML string
    return ET.tostring(root, encoding='unicode', method='xml')

if __name__ == '__main__':
    app.run(debug=True)
