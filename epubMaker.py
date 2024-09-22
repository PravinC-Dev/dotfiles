import os
from pathlib import Path
import ebooklib
from ebooklib import epub

# Function to read text from a file
def read_file_content(file_path):
    with file_path.open('r', encoding='utf-8') as file:
        return file.read()

# Function to create an EPUB book from text files
def create_epub_from_text_files(folder_path, output_filename, book_title):
    try:
        # Create a new EPUB book
        book = epub.EpubBook()

        # Set book metadata
        book.set_identifier("id123456")
        book.set_title(book_title)  # Use user input for title
        book.set_language("en")

        # List all .txt files in the folder
        text_files = sorted(folder_path.glob('*.txt'))
        print(f"Found {len(text_files)} text file(s).")

        if not text_files:
            print("No text files found in the specified directory.")
            return

        # Add chapters to the book
        spine = ['nav']  # Spine keeps track of the reading order
        chapters = []

        for text_file in text_files:
            chapter_title = text_file.stem  # Filename without extension
            chapter_content = read_file_content(text_file)
            
            print(f"Adding chapter: {chapter_title}")
            print(f"Chapter content preview: {chapter_content[:60]}...")  # Preview first 60 characters

            # Create an HTML representation for the chapter
            chapter_html = "<h2>{}</h2>\n<p>{}</p>".format(
                chapter_title,
                chapter_content.replace('\n', '</p><p>')
            )

            # Create an EPUB chapter
            chapter = epub.EpubHtml(
                title=chapter_title,
                file_name=f"{chapter_title}.xhtml",
                content=chapter_html.encode('utf-8')  # Ensure content is bytes
            )
            
            # Add chapter to the book
            book.add_item(chapter)
            chapters.append(chapter)

        # Define table of contents
        book.toc = chapters

        # Define spine
        spine.extend(chapters)
        book.spine = spine

        # Add navigation files
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # Define CSS style for EPUB (optional)
        style = 'body { font-family: Times, serif; }'
        nav_css = epub.EpubItem(
            uid="style_nav",
            file_name="styles/nav.css",
            media_type="text/css",
            content=style.encode('utf-8')  # Ensure content is bytes
        )
        book.add_item(nav_css)

        # Add CSS file to each chapter
        for chapter in chapters:
            chapter.add_link(href="styles/nav.css", rel="stylesheet", type="text/css")

        # Write the EPUB to the output file
        epub.write_epub(output_filename, book, {})
        print(f"EPUB created successfully: {output_filename}")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

# Usage
if __name__ == "__main__":
    # Dynamically set folder_path to the directory where the script is located
    script_directory = Path(__file__).resolve().parent
    print(f"Script directory: {script_directory}")

    # Ensure the folder exists
    folder_path = script_directory
    if not folder_path.exists():
        print(f"The folder path does not exist: {folder_path}")
    else:
        # Prompt user for output filename and book title
        output_filename = input("Enter the output filename (without extension): ") + ".epub"
        book_title = input("Enter the book title: ")
        
        create_epub_from_text_files(folder_path, output_filename, book_title)
