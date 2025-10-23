# Importing Required Modules
from rembg import remove
from PIL import Image


# Store path of the image in the variable input_path
input_path = "assets/nails1.png"

# Store path of the output image in the variable output_path
output_path = "assets/hands_no_bg3.png"

# Processing the image
input = Image.open(input_path)

# Resize
max_width = 1024
if input.width > max_width:
    new_height = int(input.height * max_width / input.width)
    input = input.resize((max_width, new_height), Image.LANCZOS)

# Removing the background from the given Image
output = remove(input)

# Saving the image in the given path
output.save(output_path)
