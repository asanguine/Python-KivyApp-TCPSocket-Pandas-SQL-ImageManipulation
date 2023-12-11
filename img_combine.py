from PIL import Image
import os

def combine_images(image_paths):
    images = [Image.open(path) for path in image_paths]
    combined_image = Image.new('RGBA', images[0].size, (0, 0, 0, 0))

    for image in images:
        combined_image = Image.alpha_composite(combined_image, image.convert('RGBA'))

    combined_image.save('images/character/character.png', 'PNG')
    image_path = 'images/character/character.png'
    return image_path


def body_parts(selected_clothe, selected_hair, selected_expression):
    clothe_path = f'images/character/clothes/clothe{selected_clothe}.png'
    hair_path = f'images/character/hairs/hair{selected_hair}.png'
    expression_path = f'images/character/expressions/expression{selected_expression}.png'

    image_paths = [clothe_path, hair_path, expression_path]
    return image_paths


def images_count(folder_path):
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return len(files)
