from docx import Document

def process_word_file(file_path):
    document = Document(file_path)
    recipes = []
    for paragraph in document.paragraphs:
        if paragraph.text.startswith("Receta:"):
            recipes.append(paragraph.text.split(":")[1].strip())
    # Lógica para actualizar DynamoDB
    return recipes

