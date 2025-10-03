import os
from PIL import Image, UnidentifiedImageError
import argparse

# --- Configuration ---
# NOTE: Set this variable to your absolute path before running the script
DEFAULT_MAIN_DIR = r"C:\Users\lekhn\OneDrive\Desktop\Devanagari Conjuncts Few Shot\main"

def validate_image_integrity(img_path):
    """
    Checks if an image file can be opened and verified by Pillow.
    
    Returns: True if valid, False otherwise.
    """
    try:
        # 1. Open the file
        img = Image.open(img_path)
        # 2. Run verification (checks file integrity after loading header)
        img.verify() 
        # 3. Re-open (verify closes the file handler) and load the pixel data
        Image.open(img_path).load() 
        return True
    except (UnidentifiedImageError, IOError, OSError):
        return False
    except Exception:
        return False

def rescue_corrupted_images(main_dir):
    """
    Iterates through all subfolders in main_dir. If a JPEG file is corrupted,
    it attempts to re-save it to fix the header/file structure.
    """
    print(f"--- Starting Data Validation and Rescue in: {main_dir} ---")
    
    if not os.path.isdir(main_dir):
        print(f"FATAL ERROR: Directory not found at '{main_dir}'. Check your path.")
        return

    total_files_checked = 0
    total_files_rescued = 0
    files_failed_rescue = []

    # Get list of all class subfolders
    class_names = [d for d in os.listdir(main_dir) if os.path.isdir(os.path.join(main_dir, d))]
    print(f"Found {len(class_names)} class folders.")

    for class_name in class_names:
        class_path = os.path.join(main_dir, class_name)
        
        for filename in os.listdir(class_path):
            if filename.lower().endswith(('.jpeg', '.jpg')):
                filepath = os.path.join(class_path, filename)
                total_files_checked += 1
                
                # Check file integrity
                if not validate_image_integrity(filepath):
                    
                    # --- RESCUE ATTEMPT ---
                    print(f"\n[!] Corrupted File Detected: '{class_name}' / '{filename}'")
                    
                    try:
                        # 1. Load the file (sometimes forcing a load works)
                        img = Image.open(filepath)
                        
                        # 2. Convert to RGB (standard format)
                        if img.mode not in ['RGB', 'L']: # L for grayscale, use RGB for general safety
                            img = img.convert('RGB')
                            
                        # 3. Overwrite the file with a fresh, standard JPEG header
                        # Re-saving often fixes issues caused by non-standard writing.
                        img.save(filepath, "JPEG", quality=95)
                        total_files_rescued += 1
                        print(f"  ✅ RESCUE SUCCESSFUL. File overwritten with fresh JPEG format.")
                        
                    except Exception as e:
                        files_failed_rescue.append(filepath)
                        print(f"  ❌ RESCUE FAILED. File remains corrupted. Error: {e}")

    # --- Summary ---
    print("\n" + "="*50)
    print(f"DATA RESCUE COMPLETE.")
    print(f"Total files checked: {total_files_checked}")
    print(f"Total files rescued (fixed): {total_files_rescued}")
    
    if files_failed_rescue:
        print("\nACTION REQUIRED: The following files could not be fixed and must be manually inspected/removed:")
        for path in files_failed_rescue:
            print(f" - {path}")
    else:
        print("All corrupted files were successfully fixed or none were found.")
    print("="*50)
    
    
if __name__ == "__main__":
    
    # Use argparse for flexibility, allowing the user to pass the path as an argument
    parser = argparse.ArgumentParser(description="Validate and rescue corrupted JPEG files in the dataset.")
    parser.add_argument(
        '--path', 
        type=str, 
        default=DEFAULT_MAIN_DIR, 
        help=f"Path to the 'main' dataset folder. Default: {DEFAULT_MAIN_DIR}"
    )
    args = parser.parse_args()
    
    # Run the main process
    rescue_corrupted_images(args.path)