import os
from pathlib import Path
import ebooklib
from ebooklib import epub

# Function to read text from a file
def read_file_content(file_path):
    with file_path.open('r', encoding='utf-8') as file:
        return file.read()

# Function to create an EPUB book from text files
def create_epub_from_text_files(folder_path, epub_title, output_filename):
    try:
        # Create a new EPUB book
        book = epub.EpubBook()

        # Set book metadata
        book.set_identifier("id123456")
        book.set_title(epub_title)
        book.set_language("en")

        # Add the cover image
        cover_file = folder_path / 'cover.jpg'
        if cover_file.exists():
            with cover_file.open('rb') as f:
                cover_image = f.read()
            book.set_cover("cover.jpg", cover_image)
            print("Cover image added successfully.")
        else:
            print("Cover image not found, skipping cover.")

        # List all .txt files in the folder
        text_files = sorted(folder_path.glob('*.txt'))
        print(f"Found {len(text_files)} text file(s).")

        if not text_files:
            print("No text files found in the specified directory.")
            return

        # Add chapters to the book
        spine = ['nav']  # Spine keeps track of the reading order
        chapters = []

        for i, text_file in enumerate(text_files):
            chapter_content = read_file_content(text_file)

            # Split the content into paragraphs and use the first <p> tag for the chapter title
            paragraphs = chapter_content.splitlines()

            # Find the first non-empty paragraph for the chapter title
            chapter_title = None
            if i == 0:  # If it's the first chapter (synopsis)
                chapter_title = text_file.stem  # Set title as the file name
            else:
                for para in paragraphs:
                    para = para.strip()
                    if para:
                        chapter_title = para
                        break

            if not chapter_title:
                print(f"No valid title found for chapter in file: {text_file}")
                chapter_title = text_file.stem  # Fallback to the filename if no valid title

            # Special handling for the first chapter (synopsis)
            if i == 0:  # If it's the first chapter (synopsis)
                # Ensure the body content is properly wrapped in <p> tags
                body_content = "\n".join(paragraphs).replace('\n', '</p><p>')
                if body_content:
                    body_content = f"<p>{body_content}</p>"

                print(f"Adding synopsis (first chapter) with title: {chapter_title}")
                print(f"Synopsis content preview: {body_content[:60]}...")  # Preview first 60 characters

                # Create an EPUB chapter for synopsis without heading or CSS
                chapter_html = f"""
                <div>{body_content}</div>
                """

            else:  # For other chapters
                # Remove the first <p> (the title) from the body content
                body_content = "\n".join(paragraphs[1:]).replace('\n', '</p><p>')
                if body_content:
                    body_content = f"<p>{body_content}</p>"

                print(f"Adding chapter: {chapter_title}")
                print(f"Chapter content preview: {body_content[:60]}...")  # Preview first 60 characters of body

                # Add the decorative line after the <h2> and the ending line at the end of the chapter
                chapter_html = f"""
                <h2>{chapter_title}</h2>
                <div class="decorative-line">
                    —————✧✧✧✧—————
                </div>
                {body_content}
                <div class="ending-line">
                    ✦ ✧ ✦ ✧ ✦
                </div>
                """

            # Create an EPUB chapter
            chapter = epub.EpubHtml(
                title=chapter_title,
                file_name=f"{text_file.stem}.xhtml",
                content=chapter_html.encode('utf-8')  # Ensure content is bytes
            )

            # Add chapter to the book
            book.add_item(chapter)
            chapters.append(chapter)

            if i > 0:  # Add CSS only for chapters after the first one
                chapter.add_link(href="styles/nav.css", rel="stylesheet", type="text/css")


        # Define table of contents
        book.toc = chapters

        # Define spine
        spine.extend(chapters)
        book.spine = spine

        # Add navigation files
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # Add the CSS file
        css_file = folder_path / 'styles.css'
        if css_file.exists():
            css_content = read_file_content(css_file)
            nav_css = epub.EpubItem(
                uid="style_nav",
                file_name="styles/nav.css",
                media_type="text/css",
                content=css_content.encode('utf-8')  # Ensure content is bytes
            )
            book.add_item(nav_css)

        # Add the font file
        font_file = folder_path / 'Foglihtenno07calt-WpzEA.otf'
        if font_file.exists():
            with font_file.open('rb') as f:
                font_content = f.read()
            font_item = epub.EpubItem(
                uid="font_otf",
                file_name="fonts/Foglihtenno07calt-WpzEA.otf",
                media_type="application/vnd.ms-opentype",
                content=font_content
            )
            book.add_item(font_item)

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

    # Prompt the user for the EPUB title and output file name
    epub_title = input("Enter the title of the EPUB: ")
    output_filename = input("Enter the output filename (with .epub extension): ")

    # Optionally, specify a subdirectory (uncomment if needed)
    # folder_path = script_directory / "subfolder_name"

    # If all text files are directly in the script directory
    folder_path = script_directory

    # Ensure the folder exists
    if not folder_path.exists():
        print(f"The folder path does not exist: {folder_path}")
    else:
        create_epub_from_text_files(folder_path, epub_title, output_filename)
