"""
User Photo Organization Script
This script helps organize user photos for the face recognition system
"""

import os
import shutil
from pathlib import Path

def organize_user_photos():
    """
    Organize photos in the Faces directory for the new user photo matching system
    """
    faces_dir = "../Faces"
    
    if not os.path.exists(faces_dir):
        print(f"Faces directory {faces_dir} not found!")
        return
    
    print("Current photos in Faces directory:")
    print("=" * 50)
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    image_files = []
    
    for file in os.listdir(faces_dir):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            image_files.append(file)
    
    if len(image_files) == 0:
        print("No image files found!")
        return
    
    # Display current files
    for i, file in enumerate(image_files, 1):
        username = os.path.splitext(file)[0]
        print(f"{i}. {file} -> Username: '{username}'")
    
    print("\n" + "=" * 50)
    print("Photo Organization Guidelines:")
    print("1. Each user should have ONE photo named as: username.jpg")
    print("2. Examples: john.jpg, mary.png, alex.jpg")
    print("3. Photo should show clear frontal face with good lighting")
    print("4. Remove any duplicate or unclear photos")
    
    print(f"\nTotal photos found: {len(image_files)}")
    print("System will train on these photos for user recognition")

def rename_photo_interactive():
    """
    Interactive photo renaming for better organization
    """
    faces_dir = "../Faces"
    
    if not os.path.exists(faces_dir):
        print(f"Faces directory {faces_dir} not found!")
        return
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    image_files = [f for f in os.listdir(faces_dir) 
                   if any(f.lower().endswith(ext) for ext in image_extensions)]
    
    if len(image_files) == 0:
        print("No image files found!")
        return
    
    print("Photo Renaming Tool")
    print("=" * 30)
    
    for file in image_files:
        current_path = os.path.join(faces_dir, file)
        current_username = os.path.splitext(file)[0]
        
        print(f"\nCurrent file: {file}")
        print(f"Current username: {current_username}")
        
        choice = input("(r)ename, (k)eep, (d)elete, (q)uit: ").lower().strip()
        
        if choice == 'r':
            new_username = input("Enter new username: ").strip()
            if new_username:
                file_extension = os.path.splitext(file)[1]
                new_filename = f"{new_username}{file_extension}"
                new_path = os.path.join(faces_dir, new_filename)
                
                if os.path.exists(new_path):
                    print(f"File {new_filename} already exists!")
                else:
                    os.rename(current_path, new_path)
                    print(f"Renamed to: {new_filename}")
                    
        elif choice == 'd':
            confirm = input(f"Delete {file}? (y/n): ").lower().strip()
            if confirm == 'y':
                os.remove(current_path)
                print(f"Deleted: {file}")
                
        elif choice == 'q':
            break
        
        # 'k' or any other input keeps the file as is

if __name__ == "__main__":
    print("User Photo Management")
    print("1. View current photos")
    print("2. Rename photos interactively")
    
    choice = input("\nSelect option (1 or 2): ").strip()
    
    if choice == "1":
        organize_user_photos()
    elif choice == "2":
        rename_photo_interactive()
    else:
        print("Invalid choice")
