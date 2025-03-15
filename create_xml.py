import os
import re
import xml.etree.ElementTree as ET


def sanitize_filename(filename):
    # Удаляем недопустимые символы
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def create_xml(images_data, filename="images_metadata.xml"):
    # Сначала очищаем имя файла
    filename = sanitize_filename(filename)

    # Формируем полный путь к файлу
    output_directory = os.path.join(os.getcwd(), 'output_directory')  # Укажите желаемую директорию
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)  # Создаём директорию, если она не существует

    file_path = os.path.join(output_directory, filename)

    print(f"Попытка создать XML файл: {file_path}")
    print(f"Текущая директория: {os.getcwd()}")

    # Создание XML
    metadata = ET.Element("metadata")

    for image in images_data:
        image_element = ET.SubElement(metadata, "image")
        ET.SubElement(image_element, "object").text = image['object']
        ET.SubElement(image_element, "text").text = image['text']

    # Запись XML в файл
    try:
        tree = ET.ElementTree(metadata)
        tree.write(file_path, encoding='utf-8', xml_declaration=True)
        print(f"XML файл успешно создан: {file_path}")
    except Exception as e:
        print(f"Ошибка при записи XML файла: {e}")

if __name__ == "__main__":
    images_data = [
        {
            "name": "image1",
            "object": "книга",
            "text": "джордж оруэлл 1984 книги изменившие мир писатели объединившие покления"
        },
        {
            "name": "image2",
            "object": "книга человек",
            "text": "федор достоевский двойник лабиринт.ру"
        },
        {
            "name": "image3",
            "object": "торт тарелка",
            "text": "happy day sweet biscuit"
        },
        {
            "name": "image4",
            "object": "человек футболка",
            "text": "levis"
        },
        {
            "name": "image5",
            "object": "книга",
            "text": "михаил булгаков мастер и маргарита"
        },
        {
            "name": "image6",
            "object": "знак",
            "text": "р"
        },
        {
            "name": "image7",
            "object": "книга стул",
            "text": "илья илья евгений петров двенадцать стульев"
        }
    ]

    create_xml(images_data)
