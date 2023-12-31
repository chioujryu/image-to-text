# Extract image from paper

#Import required dependencies
import fitz
import os
from PIL import Image
import cv2
import numpy as np

def extract_image_from_pdf_paper(pdf_file_path: str, images_path: str) -> list:
    """
    Description:
        Extract image from pdf which made from word.
    
    Parameters:
        pdf_file_path (str): pdf的路徑. 
        images_path (str): pdf 轉換成 jpg 後的路徑.
        
    Returns:
        list: [是否成功轉換, 有幾張 JPG].
        
        
    Examples:
        >>> extract_image_from_pdf_paper(data/pdf/1_pic.pdf, data/image)
        [True, 5]

    Exception Handling:
        Raises a ValueError if the provided str is empty.
    """

    #Open PDF file
    pdf_file = fitz.open(pdf_file_path)

    #Get the number of pages in PDF file
    page_nums = len(pdf_file)

    #Create empty list to store images information
    images_list = []

    #Extract all images information from each page
    for page_num in range(page_nums):
        page_content = pdf_file[page_num]
        images_list.extend(page_content.get_images())

    #Raise error if PDF has no images
    if len(images_list)==0:
        raise ValueError(f'No images found in {pdf_file_path}')

    #Save all the extracted images
    for i, img in enumerate(images_list, start=1):
        #Extract the image object number
        xref = img[0]
        #Extract image
        base_image = pdf_file.extract_image(xref)
        #Store image bytes
        image_bytes = base_image['image']
        #Store image extension
        image_ext = base_image['ext']
        #Generate image file name
        image_name = str(i) + '.' + image_ext
        #Save image
        with open(os.path.join(images_path, image_name) , 'wb') as image_file:
            image_file.write(image_bytes)
            image_file.close()




def save_one_image(save_path: str, image_name: str, image: np.array) -> bool:
    # 構造完整的儲存路徑 
    save_file = os.path.join(save_path, image_name)
    # 寫入圖片
    image.save(save_file)

    return True



