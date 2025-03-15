from registration_form import app
from registration_form.routes import *
from registration_form.models import db
from flask import Flask, request, render_template, redirect, url_for, send_file
import os
import cv2
import torch
import torchvision
from symspellpy import SymSpell, Verbosity
import easyocr
from create_xml import create_xml
import re

app = Flask(__name__)

# Инициализация SymSpell
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
sym_spell.load_dictionary("russian-words.txt", term_index=0, count_index=1)

# Инициализация EasyOCR
reader = easyocr.Reader(['ru'])

# Загрузка модели Faster R-CNN с ResNet-50
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
model.eval().to(device)

# Словарь классов COCO
COCO_INSTANCE_CATEGORY_NAMES = [
    "__background__", "person", "bicycle", "car", "motorcycle", "airplane",
    "bus", "train", "truck", "boat", "traffic light", "fire hydrant",
    "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse",
    "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
    "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
    "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
    "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork",
    "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
    "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
    "couch", "potted plant", "bed", "dining table", "toilet", "TV",
    "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave",
    "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase",
    "scissors", "teddy bear", "hair drier", "toothbrush"
]

# Функция для очистки имени файла
def sanitize_filename(filename):
    # Удаляем недопустимые символы и заменяем их на "_"
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def main():
    # Пример данных изображений
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
    try:
        # Создаем XML файл
        create_xml(images_data)
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Функция для обнаружения объектов
def detect_objects(image, confidence_threshold=0.5):
    transform = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
    ])
    image_tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        predictions = model(image_tensor)

    detected_objects = []
    for i in range(len(predictions[0]['labels'])):
        score = predictions[0]['scores'][i].item()
        label = predictions[0]['labels'][i].item()

        if label < len(COCO_INSTANCE_CATEGORY_NAMES) and score > confidence_threshold:
            box = predictions[0]['boxes'][i].cpu().numpy().tolist()
            detected_objects.append({
                'label': COCO_INSTANCE_CATEGORY_NAMES[label],
                'score': score,
                'box': box
            })

    return detected_objects

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/pomosh')
def pomosh():
    return render_template('pomosh.html')

@app.route('/profil')
def profil():
    return render_template('profil.html')

@app.route('/vxod_reg')
def vxod_reg():
    return render_template('vxod_reg.html')

@app.route('/download')
def download_file():
    try:
        # Укажите правильный путь к файлу
        file_path = os.path.join('output_directory', 'output.xml')
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        print("Файл не найден.")
        return "Файл не найден", 404
    except Exception as e:
        print(f"Ошибка при скачивании файла: {e}")
        return "Ошибка при скачивании файла", 500

@app.route('/upload', methods=['POST'])
def upload_file():
    output_directory = 'uploads'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    if 'files' in request.files:
        files = request.files.getlist('files')

        if not files:
            return "No selected files", 400

        all_results = []
        images_data = []

        for file in files:
            if file.filename == '':
                return "No selected file", 400

            # Очистка имени файла
            clean_filename = sanitize_filename(file.filename)
            print(f"Cleaned filename: {clean_filename}")  # Логирование очищенного имени

            if not clean_filename or clean_filename.isspace():
                return "Invalid file name", 400

            file_path = os.path.join(output_directory, clean_filename)
            print(f"Saving file to: {file_path}")  # Логирование пути

            try:
                file.save(file_path)
            except Exception as e:
                print(f"Error saving file: {e}")
                return "Error saving file", 500

            if not os.path.exists(file_path):
                print(f"File not found after saving: {file_path}")
                continue

            img = cv2.imread(file_path)

            if img is None:
                print(f"Error loading image with OpenCV: {file_path}")
                continue

            detected_objects = detect_objects(img, confidence_threshold=0.5)

            results = reader.readtext(file_path)

            if not results:
                print(f"No text found in the image: {file.filename}")
                extracted_text = "не обнаружено"
            else:
                extracted_text = " ".join([result[1] for result in results])

            corrected_words = []
            for word in extracted_text.split():
                suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, include_unknown=True)
                corrected_words.append(suggestions[0].term if suggestions else word)

            corrected_text = " ".join(corrected_words)

            all_results.append({
                'corrected_text': corrected_text,
                'extracted_text': extracted_text,
                'detected_objects': detected_objects
            })

            images_data.append({
                'name': clean_filename,
                'object': detected_objects[0]['label'] if detected_objects else "не обнаружено",
                'text': corrected_text
            })

        try:
            create_xml(images_data, filename='output.xml')
        except Exception as e:
            print(f"Произошла ошибка при создании XML: {e}")

        return render_template('index.html', results=all_results)

    return "No files or text input found", 400

@app.route('/upload-xml', methods=['POST'])
def upload_xml():
    if 'xml_file' not in request.files:
        return "No file part", 400

    xml_file = request.files['xml_file']

    if xml_file.filename == '':
        return "No selected file", 400

    # Сохранение XML файла
    save_path = os.path.join('uploads', xml_file.filename)
    xml_file.save(save_path)

    return "XML файл успешно загружен!", 200


if __name__ == '__main__':
    app.run(debug=True)

