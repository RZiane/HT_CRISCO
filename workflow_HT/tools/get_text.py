import xml.etree.ElementTree as ET

def extract_text_from_tei(xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    paragraphs = []

    for paragraph in root.iter('p'):
        paragraph_text = ' '.join(paragraph.itertext())
        paragraphs.append(paragraph_text)

    return '\n\n'.join(paragraphs).replace('\t', '')

if __name__ == "__main__":
    xml_file_path = "/home/ziane212/Téléchargements/Guernsey_Crime_I_2_lemma_30.11.23.xml"
    extracted_text = extract_text_from_tei(xml_file_path)

    with open("/home/ziane212/Téléchargements/Guernsey_Crime_I_2_lemma_30.11.23.txt", "w", encoding="utf-8") as output_file:
        output_file.write(extracted_text)

    print("Extraction réussie. Le texte extrait a été enregistré dans le fichier texte_extrait.txt.")
