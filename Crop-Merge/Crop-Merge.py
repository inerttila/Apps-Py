import os
from PIL import Image

def crop_image(image_path, save_folder, crop_width=1500, crop_height=820):
    """
    Crops an orthophoto into smaller chunks and saves them.

    :param image_path: Path to the orthophoto image.
    :param save_folder: Path to the folder where cropped images will be saved.
    :param crop_width: Width of each crop.
    :param crop_height: Height of each crop.
    """
    # Open the orthophoto
    with Image.open(image_path) as img:
        # Calculate number of chunks
        x_chunks = img.width // crop_width
        y_chunks = img.height // crop_height
        
        # Create the save folder if it doesn't exist
        if not os.path.isdir(save_folder):
            os.makedirs(save_folder, exist_ok=True)
        
        # Iterate over each chunk
        for i in range(x_chunks):
            for j in range(y_chunks):
                left = i * crop_width
                upper = j * crop_height
                right = left + crop_width
                lower = upper + crop_height
                
                # Crop the image
                img_chunk = img.crop((left, upper, right, lower))
                
                # Save the chunk
                base_image_name = os.path.splitext(os.path.basename(image_path))[0]
                cropped_image_path = os.path.join(save_folder, base_image_name + f"_{i}_{j}.tif")
                img_chunk.save(cropped_image_path)
                print(f"Saved: {cropped_image_path}")

def merge_images(input_folder, output_path):
    """
    Merges cropped images into a single image.

    :param input_folder: Path to the folder containing cropped images.
    :param output_path: Path to save the merged orthophoto.
    """
    images = {}
    max_col = 0
    max_row = 0

    # Read and organize images by their (col, row) indices
    for image in os.listdir(input_folder):
        if image.endswith((".tif", ".jpg", ".png")):
            parts = image.split("_")
            if len(parts) >= 3:
                try:
                    col = int(parts[-2])  # Column index
                    row = int(parts[-1].split(".")[0])  # Row index
                    max_col = max(max_col, col)
                    max_row = max(max_row, row)
                    images[(col, row)] = Image.open(os.path.join(input_folder, image))
                except ValueError:
                    print(f"Skipping invalid image name format: {image}")

    # Check if there are any images
    if not images:
        raise ValueError("No valid images found in the input folder.")

    # Verify all images are the same size
    img_width, img_height = next(iter(images.values())).size
    for img in images.values():
        if img.size != (img_width, img_height):
            raise ValueError("All images must have the same dimensions.")

    # Create a blank canvas for the final merged image
    total_width = (max_col + 1) * img_width
    total_height = (max_row + 1) * img_height
    merged_image = Image.new("RGB", (total_width, total_height))

    # Paste images into the merged canvas
    for (col, row), img in images.items():
        x_offset = col * img_width
        y_offset = row * img_height
        merged_image.paste(img, (x_offset, y_offset))

    # Save the final merged image
    try:
        merged_image.save(output_path)
        print(f"Merged orthophoto saved to: {output_path}")
    except Exception as e:
        print(f"Error saving merged orthophoto: {e}")

# Main logic for the app
def main():
    print("""
Welcome to the Orthophoto Processor!
Options:
  crop  - Crop the orthophoto into smaller chunks
  merge - Merge cropped images into a single orthophoto
""")

    mode = input("Enter mode (crop/merge): ").strip().lower()

    if mode == "crop":
        image_path = input("Enter the path to the orthophoto: ").strip()
        save_folder = input("Enter the folder to save the cropped images: ").strip()

        # Validate inputs
        if not os.path.isfile(image_path):
            print("Error: The specified image file does not exist.")
            return

        # Create the save folder if it doesn't exist
        if not os.path.isdir(save_folder):
            os.makedirs(save_folder, exist_ok=True)

        # Crop the image
        print("Cropping the orthophoto...")
        crop_image(image_path, save_folder)
        print("Cropping completed successfully!")

    elif mode == "merge":
        input_folder = input("Enter the folder containing cropped images: ").strip()
        output_folder = input("Enter the folder to save the merged image: ").strip()

        # Validate input
        if not os.path.isdir(input_folder):
            print("Error: The specified folder does not exist.")
            return

        # Create the output folder if it doesn't exist
        if not os.path.isdir(output_folder):
            os.makedirs(output_folder, exist_ok=True)

        # Generate output path
        output_path = os.path.join(output_folder, "merged_image.tif")

        # Merge the images
        print("Merging cropped images...")
        merge_images(input_folder, output_path)
        print("Merging completed successfully!")

    else:
        print("Invalid mode. Please enter 'crop' or 'merge'.")

if __name__ == "__main__":
    main()
