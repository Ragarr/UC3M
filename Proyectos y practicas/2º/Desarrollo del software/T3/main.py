
"""
This is the main file of the project. It is the entry point of the program.
It is the file that will be executed when the program is run.
"""
import string
from barcode import EAN13
from barcode.writer import ImageWriter
from UC3MLogistics import OrderManager
from UC3MLogistics import  OrderManagementException

# GLOBAL VARIABLES
LETTERS = string.ascii_letters + string.punctuation + string.digits
SHIFT = 3


def encode(word):
    """
    codifies a word
    """
    encoded = ""
    for letter in word:
        if letter == ' ':
            encoded = encoded + ' '
        else:
            x = (LETTERS.index(letter) + SHIFT) % len(LETTERS)
            encoded = encoded + LETTERS[x]
    return encoded

def decode(word):
    """
    decodes a word to a new
    """
    encoded = ""
    for letter in word:
        if letter == ' ':
            encoded = encoded + ' '
        else:
            x = (LETTERS.index(letter) - SHIFT) % len(LETTERS)
            encoded = encoded + LETTERS[x]
    return encoded

def main():
    """
    Main function of the program
    """
    generate_barcode("correct_code1.json")
    generate_barcode("incorrect_code1.json")


def generate_barcode(name: str):
    """generates the image from a json file name"""
    try:
        order_manager= OrderManager()
        product = order_manager.ReadproductcodefromJSON(name)
        print(str(product))
        encode_res = encode(str(product))
        print("Encoded Res " + encode_res)
        decode_res = decode(encode_res)
        print("Decoded Res: " + decode_res)
        print("Code: " + product.productCode)
        image_name = f"./barcodeEan13-{product.productCode}.jpg"
        with open(image_name, 'wb') as f:
            iw = ImageWriter()
            EAN13(product.productCode, writer=iw).write(f)
    except OrderManagementException as e:
        print(e)


if __name__ == "__main__":
    main()
