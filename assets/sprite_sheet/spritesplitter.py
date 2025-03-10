from PIL import Image
import os

def split_sprite_sheet(sheet_path, sprite_width, sprite_height, output_folder):
    """
    Splits a sprite sheet into individual sprite images.
    
    :param sheet_path: Path to the sprite sheet image file.
    :param sprite_width: Width of each individual sprite.
    :param sprite_height: Height of each individual sprite.
    :param output_folder: Folder where the extracted sprites will be saved.
    """
    # Open the sprite sheet
    sheet = Image.open(sheet_path)
    sheet_width, sheet_height = sheet.size
    
    # Calculate the number of sprites in each row and column
    cols = sheet_width // sprite_width
    rows = sheet_height // sprite_height
    
    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)
    
    sprite_count = 0
    for row in range(rows):
        for col in range(cols):
            # Define the bounding box for each sprite
            left = col * sprite_width
            upper = row * sprite_height
            right = left + sprite_width
            lower = upper + sprite_height
            
            # Extract the sprite
            sprite = sheet.crop((left, upper, right, lower))
            
            # Save the sprite
            sprite_filename = os.path.join(output_folder, f'sprite_{sprite_count}.png')
            sprite.save(sprite_filename)
            sprite_count += 1
    
    print(f"Successfully extracted {sprite_count} sprites to {output_folder}")

# Example usage:
split_sprite_sheet("roads2W.png", 64, 64, "assets/sprite_sheet")
