import os
import shutil
import base64
from io import BytesIO
try:
    import fitz  # pymupdf
except ImportError:
    try:
        import pymupdf as fitz
    except ImportError:
        print("Error: PyMuPDF (fitz) module not found. Please install it using 'pip install pymupdf'.")
        exit(1)

from markdownify import markdownify as md
from PIL import Image

def extract_images_from_html(html_content, output_dir):
    """
    Parses HTML content, finds base64 encoded images, saves them to disk,
    and replaces the src attribute with the relative path.
    This is a simplistic approach using string manipulation to avoid adding BeautifulSoup dependency if possible.
    However, for robust HTML parsing, BeautifulSoup is better. Let's try to stick to standard library or what we have.
    Actually, fitz.get_text("html") produces specific output.
    
    BUT, a better way with PyMuPDF is to extract images directly from the PDF pages
    and then insert placeholders or just rely on the text extraction.
    
    The issue is that get_text("html") embeds images as base64.
    Let's use a regex to find <img src="data:image/..." ...> and replace it.
    """
    import re
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    img_pattern = re.compile(r'<img[^>]+src="data:image/([^;]+);base64,([^"]+)"[^>]*>')
    
    def replace_image(match):
        ext = match.group(1)
        data = match.group(2)
        
        # Simple hash or counter for filename
        # Using a counter requires state, so let's use hash of data
        import hashlib
        img_hash = hashlib.md5(data.encode()).hexdigest()
        img_filename = f"img_{img_hash}.{ext}"
        img_path = os.path.join(output_dir, img_filename)
        
        # Save image if it doesn't exist
        if not os.path.exists(img_path):
            try:
                with open(img_path, "wb") as f:
                    f.write(base64.b64decode(data))
            except Exception as e:
                print(f"Failed to save image {img_filename}: {e}")
                return match.group(0) # Return original if failed
        
        # Return new img tag with relative path
        # We need the relative path from the markdown file location
        # Assuming markdown file is in the parent directory of output_dir
        rel_path = os.path.join(os.path.basename(output_dir), img_filename).replace("\\", "/")
        # Use standard markdown image syntax
        return f'![Image]({rel_path})'

    new_html = img_pattern.sub(replace_image, html_content)
    return new_html

def convert_pdf_to_md(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        
        # Create a directory for images based on the pdf filename
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        images_dir = os.path.join("images", base_name)
        
        html_content = ""
        for page in doc:
            # Use "blocks" or "text" to better control layout if needed, 
            # but "html" preserves structure best for markdownify.
            # Let's try to improve the markdownify options.
            html_content += page.get_text("html")
        
        # Process HTML to extract images
        html_content = extract_images_from_html(html_content, images_dir)
        
        # Configure markdownify to handle tables and other elements better
        markdown_content = md(html_content, heading_style="ATX", strip=['a']) 
        # Removing 'a' tags might be too aggressive if there are real links, 
        # but often PDF links are internal anchors that break.
        # Let's stick to default but maybe add some post-processing.
        
        # Post-processing to clean up excessive newlines which is common with PDF extraction
        import re
        markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
        
        output_path = base_name + ".md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        
        print(f"Successfully converted {pdf_path} to {output_path}")
        return output_path
    except Exception as e:
        print(f"Error converting {pdf_path}: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    files = [f for f in os.listdir('.') if f.lower().endswith('.pdf')]
    converted_files = []
    
    if not files:
        print("No PDF files found in the current directory.")
        return

    print(f"Found {len(files)} PDF files: {files}")

    for file in files:
        print(f"Converting {file}...")
        result = convert_pdf_to_md(file)
        if result:
            converted_files.append(result)

    if converted_files:
        print("\nConversion complete.")
        print("Converted files:")
        for f in converted_files:
            print(f"- {f}")
    else:
        print("\nNo files were converted successfully.")

if __name__ == "__main__":
    main()
