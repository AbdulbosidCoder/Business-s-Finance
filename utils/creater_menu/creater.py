import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def combine_images_with_titles(images, titles, space=100):
    # Calculate maximum height and width
    max_height = max(img.shape[0] for img in images)
    max_width = max(img.shape[1] for img in images)

    # Calculate the dimensions of the combined image
    combined_width = max_width * 3 + space * 2
    combined_height = max_height * 3 + space * 2 + 30 * len(images) // 3+space*2

    # Create a new blank image
    combined_image = np.ones((combined_height, combined_width, 3), dtype=np.uint8) * 255

    # Paste images onto the blank image with spacing and write titles
    x_offset = 0
    y_offset = 0
    for img, title in zip(images, titles):
        combined_image[y_offset:y_offset + max_height, x_offset:x_offset + max_width, :] = img

        # Write title under the image
        font = ImageFont.truetype("arial.ttf", 90)  # Load font with size 18
        img_pil = Image.fromarray(combined_image)
        draw = ImageDraw.Draw(img_pil)
        text_width = draw.textlength(title, font=font)
        draw.text((x_offset + (max_width - text_width) // 2, y_offset + max_height-10), title, font=font, fill=(0, 0, 0),embedded_color="RGB")
        combined_image = np.array(img_pil)

        x_offset += max_width + space
        if x_offset >= combined_width:  # Check if we've reached the end of a row
            x_offset = 0
            y_offset += max_height + space + 30

    return combined_image


def create_menu(take, skip, database):
    # Load images using cv2
    product_images= []
    prorducts = database.get_products_with_pagination(skip=skip, take=take)
    for i in prorducts:
        product_images.append(database.get_product_photo_by_product_id(product_id=i[0]))
    images = []
    titles = []
    l = 0
    for i in product_images:
        img = cv2.imread(i[2])
        images.append(img)
        titles.append(prorducts[l][1])
        l += 1

    # Resize images to have the same dimensions
    max_height = max(img.shape[0] for img in images)
    max_width = max(img.shape[1] for img in images)
    for i in range(len(images)):
        images[i] = cv2.resize(images[i], (max_width, max_height))

    # Combine images with white space and titles
    combined_image_cv2 = combine_images_with_titles(images, titles, space=50)

    # Convert combined image to PIL Image
    combined_image_pil = Image.fromarray(combined_image_cv2)

    # Save the combined image
    combined_image_pil.save("D:\\PycharmProjects\\Finance\\media\\menu_of_products\\menu.jpg")
    # Load the image in BGR format
    bgr_image = cv2.imread("D:\\PycharmProjects\\Finance\\media\\menu_of_products\\menu.jpg")

    # Convert BGR image to RGB
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
    cv2.imwrite("D:\\PycharmProjects\\Finance\\media\\menu_of_products\\menu.jpg", rgb_image)

    return titles

    # Display the combined image
    # combined_image_pil.show()

