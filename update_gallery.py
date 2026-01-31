import os

# Paths - use script's directory as base
base_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(base_dir, "assets", "images")
pdf_dir = os.path.join(base_dir, "assets", "pdf")
html_file = os.path.join(base_dir, "index.html")


def update_assets():
    print("Scanning assets...")
    
    # --- 1. Generate Image List ---
    images = []
    valid_img_exts = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp')
    
    if os.path.exists(image_dir):
        files = os.listdir(image_dir)
        files.sort(key=lambda x: x.lower())
        for f in files:
            if f.lower().endswith(valid_img_exts):
                clean_name = f.replace('"', '\\"') # Escape quotes
                images.append(f'    "assets/images/{clean_name}"')
    
    gallery_js_block = "const galleryImages = [\n" + ",\n".join(images) + "\n];"
    print(f"Found {len(images)} images.")

    # --- 2. Generate PDF List ---
    pdfs = []
    valid_pdf_exts = ('.pdf',)
    
    if os.path.exists(pdf_dir):
        files = os.listdir(pdf_dir)
        files.sort(key=lambda x: x.lower())
        for f in files:
            if f.lower().endswith(valid_pdf_exts):
                full_name = f
                # Generate a display name from the filename
                # Remove extension
                name_base = os.path.splitext(f)[0]
                # Replace underscores/hyphens with spaces
                temp_name = name_base.replace("_", " ").replace("-", " ")
                # Remove extra spaces and Title Case
                display_name = " ".join(temp_name.split()).title()
                
                file_esc = f.replace('"', '\\"')
                name_esc = display_name.replace('"', '\\"')
                
                pdfs.append(f'    {{ name: "{name_esc}", file: "{file_esc}" }}')
                
    pdf_js_block = "const pdfFiles = [\n" + ",\n".join(pdfs) + "\n];"
    print(f"Found {len(pdfs)} PDFs.")

    # --- 3. Generate 360 Image List ---
    pano_images = []
    pano_dir = os.path.join(base_dir, "assets", "360-images")
    
    if os.path.exists(pano_dir):
        files = os.listdir(pano_dir)
        files.sort(key=lambda x: x.lower())
        for i, f in enumerate(files):
            if f.lower().endswith(valid_img_exts):
                clean_name = f.replace('"', '\\"')
                # Generate a simple title
                title = f"View {i+1}"
                
                pano_images.append(f'    {{ src: "assets/360-images/{clean_name}", title: "{title}" }}')
                
    pano_js_block = "const panoImages = [\n" + ",\n".join(pano_images) + "\n];"
    print(f"Found {len(pano_images)} 360 Images.")

    # --- 4. Generate Video List ---
    videos = []
    valid_video_exts = ('.mp4', '.webm', '.ogg')
    video_dir = os.path.join(base_dir, "assets", "videos")
    
    if os.path.exists(video_dir):
        files = os.listdir(video_dir)
        files.sort(key=lambda x: x.lower())
        for f in files:
            if f.lower().endswith(valid_video_exts):
                clean_name = f.replace('"', '\\"')
                
                # Title generation
                name_base = os.path.splitext(f)[0]
                temp_name = name_base.replace("_", " ").replace("-", " ")
                display_name = " ".join(temp_name.split()).title()
                
                name_esc = display_name.replace('"', '\\"')
                
                videos.append(f'    {{ src: "assets/videos/{clean_name}", title: "{name_esc}" }}')
                
    video_js_block = "const videoFiles = [\n" + ",\n".join(videos) + "\n];"
    print(f"Found {len(videos)} Videos.")

    # --- 5. Update HTML ---
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated_content = content
        
        # Helper to replace content between js variable definition and closing bracket
        def replace_js_array(full_text, var_name, new_block):
            # precise start string
            start_str = f"const {var_name} = ["
            end_str = "];"
            
            start_idx = full_text.find(start_str)
            if start_idx == -1:
                print(f"Warning: Could not find variable '{var_name}' in HTML.")
                return full_text
            
            # Find the *matching* closing bracket.
            end_idx = full_text.find(end_str, start_idx)
            if end_idx == -1:
                print(f"Warning: Could not find closing for '{var_name}'.")
                return full_text
            
            # Replace
            return full_text[:start_idx] + new_block + full_text[end_idx + len(end_str):]

        updated_content = replace_js_array(updated_content, "galleryImages", gallery_js_block)
        updated_content = replace_js_array(updated_content, "pdfFiles", pdf_js_block)
        updated_content = replace_js_array(updated_content, "panoImages", pano_js_block)
        updated_content = replace_js_array(updated_content, "videoFiles", video_js_block)
        
        if updated_content != content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print("Successfully updated index.html!")
        else:
            print("Index.html is already up to date.")
            
    except Exception as e:
        print(f"Error reading/writing HTML file: {e}")

if __name__ == "__main__":
    update_assets()
