import os
from PIL import Image, ImageEnhance, ImageFilter

# Paths
input_dir = '/Users/collisonmarks/Library/Application Support/minecraft/versions/1.21.5/1.21.5/assets/minecraft/textures'
output_dir = 'cartoon_pack/textures'

# Cartoonify function
def cartoonify_image(image_path, output_path):
    img = Image.open(image_path).convert('RGBA')

    # Increase saturation
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(2.0)  # 2.0 = 200% saturation
    img.save(output_path[:-4]+"1"+output_path[-4:])
    print(output_path[:-4]+"1"+output_path[-4:])
    # Increase contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)
    img.save(output_path[:-4]+"2"+output_path[-4:])
    print(output_path[:-4]+"2"+output_path[-4:])
    # Detect edges and blend as "outline"
    edges = img.convert('L').filter(ImageFilter.FIND_EDGES)
    edges = edges.point(lambda x: 255 if x < 1 else 0)  # threshold
    edges = edges.convert('RGBA')
    outline = Image.new('RGBA', img.size, (0, 0, 0, 0))
    outline.paste((0, 0, 0, 0), mask=edges)

    # Blend the outline over the image
    cartoon_img = Image.alpha_composite(img, outline)
    
    

    cartoon_img.save(output_path)

# Process all textures
for subdir, _, files in os.walk(input_dir):
    for file in files:
        if file.endswith('.png'):
            relative_path = os.path.relpath(subdir, input_dir)
            output_subdir = os.path.join(output_dir, relative_path)
            os.makedirs(output_subdir, exist_ok=True)

            input_path = os.path.join(subdir, file)
            output_path = os.path.join(output_subdir, file)

            cartoonify_image(input_path, output_path)
            print(f"Converted: {input_path} → {output_path}")
