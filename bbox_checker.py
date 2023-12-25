import os
from tkinter import filedialog, Button, Label, Tk, messagebox
from PIL import Image, ImageDraw, ImageTk
import xml.etree.ElementTree as ET

def draw_bounding_boxes(image_path, xml_path, output_folder):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    for obj in root.findall('.//object'):
        xmin = int(obj.find('bndbox/xmin').text)
        ymin = int(obj.find('bndbox/ymin').text)
        xmax = int(obj.find('bndbox/xmax').text)
        ymax = int(obj.find('bndbox/ymax').text)
        
        draw.rectangle([xmin, ymin, xmax, ymax], outline='red', width=2)
    
    output_path = os.path.join(output_folder, os.path.basename(image_path))
    image.save(output_path)
    print(f"Saved image with bounding box: {output_path}")


def validate_bbox(xmin, ymin, xmax, ymax):
    if xmin >= xmax or ymin >= ymax:
        return False
    return True

def select_xml_folder():
    global xml_folder
    xml_folder = filedialog.askdirectory(title="Select XML Folder")
    xml_label.config(text=f"XML Folder: {xml_folder}")

def select_images_folder():
    global images_folder
    images_folder = filedialog.askdirectory(title="Select Images Folder")
    images_label.config(text=f"Images Folder: {images_folder}")

def select_output_folder():
    global output_folder
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    output_label.config(text=f"Output Folder: {output_folder}")

def process_folders():
    global xml_folder, images_folder, output_folder
    
    if not (xml_folder and images_folder and output_folder):
        messagebox.showerror("Error", "Please select all folders.")
        return
    
    for xml_file in os.listdir(xml_folder):
        if xml_file.endswith('.xml'):
            image_name = os.path.splitext(xml_file)[0] + '.png'
            image_path = os.path.join(images_folder, image_name)
            xml_path = os.path.join(xml_folder, xml_file)
            
            if os.path.exists(image_path):
                tree = ET.parse(xml_path)
                root = tree.getroot()
                
                for obj in root.findall('.//object'):
                    xmin = int(obj.find('bndbox/xmin').text)
                    ymin = int(obj.find('bndbox/ymin').text)
                    xmax = int(obj.find('bndbox/xmax').text)
                    ymax = int(obj.find('bndbox/ymax').text)
                    
                    if not validate_bbox(xmin, ymin, xmax, ymax):
                        messagebox.showwarning("Warning", f"Invalid bbox coordinates in {xml_file}")
                        continue  # Skip processing this object
                
                    draw_bounding_boxes(image_path, xml_path, output_folder)
            else:
                messagebox.showwarning("Warning", f"Image not found for {xml_file}")
    
    messagebox.showinfo("Information", "Processing complete.")

# Create the main window
root = Tk()
root.title("bbox checker")

script_dir = os.path.dirname(os.path.abspath(__file__))

image_path = os.path.join(script_dir, "eye.png")

# Load and display an image in the UI
image = Image.open(image_path)
image = image.resize((600, 600), Image.ANTIALIAS)  # Resize the image
photo = ImageTk.PhotoImage(image)
image_label = Label(root, image=photo)
image_label.pack()


# UI components
select_xml_button = Button(root, text="Select XML Folder", command=select_xml_folder)
select_xml_button.pack()

select_images_button = Button(root, text="Select Images Folder", command=select_images_folder)
select_images_button.pack()

select_output_button = Button(root, text="Select Output Folder", command=select_output_folder)
select_output_button.pack()

process_button = Button(root, text="Process Folders", command=process_folders)
process_button.pack()

xml_label = Label(root, text="XML Folder: Not Selected")
xml_label.pack()

images_label = Label(root, text="Images Folder: Not Selected")
images_label.pack()

output_label = Label(root, text="Output Folder: Not Selected")
output_label.pack()

# Start the GUI event loop
root.mainloop()
