from PIL import Image

def resize_images(image_paths, new_width, new_height):
    for image_path in image_paths:
        try:
            # Open the image
            image = Image.open(image_path)

            # Resize the image
            resized_image = image.resize((new_width, new_height))

            # Save the resized image
            resized_image.save(image_path)

            print(f"Image {image_path} successfully resized and saved.")
        except FileNotFoundError:
            print(f"File {image_path} not found.")
        except Exception as e:
            print(f"An error occurred while resizing {image_path}: {e}")


# Get the image paths from the user as a newline-separated string
image_paths_string = input("Enter the image paths (one path per line, enter 'done' when finished): ")

# Collect the image paths until the user enters 'done'
image_paths = []
while image_paths_string != "done":
    image_paths.append(image_paths_string)
    image_paths_string = input()

# Get the new width and height from the user
new_width = int(input("Enter the new width: "))
new_height = int(input("Enter the new height: "))

# Resize the images
resize_images(image_paths, new_width, new_height)
