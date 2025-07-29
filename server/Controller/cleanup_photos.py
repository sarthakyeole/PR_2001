"""
Automated Photo Cleanup Script
This script will clean up the messy photo directory and keep only one photo per user
"""

import os
import shutil
from pathlib import Path

def cleanup_photos():
    """
    Clean up the Faces directory by:
    1. Keeping only the clear named photos (Nitin.jpg, Rutuja.jpg, etc.)
    2. Deleting all WIN_20250... photos
    3. Renaming photos to lowercase for consistency
    """
    faces_dir = "../Faces"
    backup_dir = "../Faces_backup"
    
    if not os.path.exists(faces_dir):
        print(f"Faces directory {faces_dir} not found!")
        return
    
    # Create backup first
    if not os.path.exists(backup_dir):
        print("Creating backup of all photos...")
        shutil.copytree(faces_dir, backup_dir)
        print(f"Backup created at: {backup_dir}")
    
    # Define the photos to keep (clean names)
    keep_photos = {
        "Nitin.jpg": "nitin.jpg",
        "Rutuja.jpg": "rutuja.jpg", 
        "Sarthak.jpg": "sarthak.jpg",
        "Vansh.jpg": "vansh.jpg"
    }
    
    # Find the best photo for 'sarth' from all WIN photos
    win_photos = []
    all_files = os.listdir(faces_dir)
    
    for file in all_files:
        if file.startswith("WIN_20250728_22_18_51"):  # Your main photos
            win_photos.append(file)
    
    print("\nCleaning up photos...")
    print("=" * 40)
    
    # Keep and rename the clean photos
    for old_name, new_name in keep_photos.items():
        old_path = os.path.join(faces_dir, old_name)
        new_path = os.path.join(faces_dir, new_name)
        
        if os.path.exists(old_path):
            if old_path != new_path:
                os.rename(old_path, new_path)
                print(f"✅ Renamed: {old_name} → {new_name}")
            else:
                print(f"✅ Kept: {new_name}")
        else:
            print(f"❌ Not found: {old_name}")
    
    # Pick the best photo for 'sarth'
    if win_photos:
        best_photo = win_photos[0]  # Use the first WIN photo found
        old_path = os.path.join(faces_dir, best_photo)
        new_path = os.path.join(faces_dir, "sarth.jpg")
        
        shutil.copy2(old_path, new_path)
        print(f"✅ Created: sarth.jpg (from {best_photo})")
    
    # Delete all WIN photos and other junk
    deleted_count = 0
    for file in all_files:
        file_path = os.path.join(faces_dir, file)
        
        # Delete if it's a WIN photo or not in our keep list
        if (file.startswith("WIN_") or 
            file not in [list(keep_photos.values()) + ["sarth.jpg"]] and
            file not in ["nitin.jpg", "rutuja.jpg", "sarthak.jpg", "vansh.jpg", "sarth.jpg"]):
            
            try:
                os.remove(file_path)
                deleted_count += 1
            except:
                pass
    
    print(f"🗑️  Deleted {deleted_count} duplicate/unnecessary photos")
    
    # Show final result
    print("\n" + "=" * 40)
    print("Final photo directory:")
    
    remaining_files = [f for f in os.listdir(faces_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    for i, file in enumerate(remaining_files, 1):
        username = os.path.splitext(file)[0]
        print(f"{i}. {file} → Username: '{username}'")
    
    print(f"\nTotal users: {len(remaining_files)}")
    print("✅ Cleanup completed!")
    
    if len(remaining_files) <= 10:
        print("👍 Perfect! Now you have a clean, manageable set of user photos.")
    else:
        print("⚠️  Still too many photos. Consider manual cleanup.")

def main():
    print("Photo Cleanup Tool")
    print("=" * 30)
    print("This will:")
    print("1. Create a backup of all photos")
    print("2. Keep only clean user photos")
    print("3. Delete all WIN_20250... duplicates")
    print("4. Rename photos to lowercase")
    
    confirm = input("\nProceed with cleanup? (y/n): ").lower().strip()
    
    if confirm == 'y':
        cleanup_photos()
    else:
        print("Cleanup cancelled.")

if __name__ == "__main__":
    main()
