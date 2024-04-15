import csv

def csv_extractor(file_path):
    text = ""
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for cell in row:
                text += cell + " "
    return text
