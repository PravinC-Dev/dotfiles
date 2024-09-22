import os
import ebooklib
from ebooklib import epub

# Function to read text from a file
def read_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to create an EPUB book from text files
def create_epub_from_text_files(folder_path, output_filename="output.epub"):
    try:
        # Create a new EPUB book
        book = epub.EpubBook()

        # Set book metadata
        book.set_identifier("id123456")
        book.set_title("Otherworldly Hotel")
        book.set_language("en")

        # List all files in the folder
        text_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
        print(f"Found {len(text_files)} text files.")

        if not text_files:
            print("No text files found in the specified directory.")
            return

        # Sort the files if needed (alphabetically by default)
        text_files.sort()

        # Add chapters to the book
        spine = ['nav']  # Spine keeps track of the reading order
        for text_file in text_files:
            chapter_title = os.path.splitext(text_file)[0]  # Chapter title is the filename without extension
            chapter_content = read_file_content(os.path.join(folder_path, text_file))
            print(f"Adding chapter: {chapter_title}")

            # Create an HTML representation for the chapter
            # Ensure that backslashes in content are properly handled
            chapter_html = "<h2>{}</h2>\n<p>{}</p>".format(
    chapter_title,
    chapter_content.replace('\n', '</p><p>')
)

            # Create an EPUB chapter
            chapter = epub.EpubHtml(title=chapter_title, file_name=f"{chapter_title}.xhtml", content=chapter_html)
            
            # Add chapter to the book
            book.add_item(chapter)
            spine.append(chapter)  # Append chapter to spine

        # Add navigation files (table of contents)
        book.toc = spine[1:]  # Exclude 'nav'
        book.spine = spine

        # Add the default navigation documents
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # Define CSS style for EPUB (optional)
        style = 'body { font-family: Times, serif; }'
        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style.encode('utf-8'))
        book.add_item(nav_css)

        # Write the EPUB to the output file
        epub.write_epub(output_filename, book, {})
        print(f"EPUB created successfully: {output_filename}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Usage
if __name__ == "__main__":
    # Choose one of the following methods to define folder_path

    # Option A: Raw String
    folder_path = r"D:\study materials\Epubs\异度旅社 - The Otherworldly Inn(possibly Mansion)"

    # Option B: Escaped Backslashes
    # folder_path = "D:\\study materials\\Epubs\\异度旅社 - The Otherworldly Inn(possibly Mansion)"

    # Option C: Forward Slashes
    # folder_path = "D:/study materials/Epubs/异度旅社 - The Otherworldly Inn(possibly Mansion)"

    create_epub_from_text_files(folder_path, output_filename="Otherworldly_Hotel.epub")
