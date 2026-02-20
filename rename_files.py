import os
import shutil

rename_map = {
    "App 审核指南 - Apple 开发者.pdf": "apple_app_store_review_guidelines.pdf",
    "华为应用市场审核指南.pdf": "huawei_appgallery_review_guidelines.pdf",
    "开发者计划政策 - Play 管理中心帮助.pdf": "google_play_developer_program_policies.pdf"
}

delete_list = [
    "App 审核指南 - Apple 开发者.md",
    "华为应用市场审核指南.md",
    "开发者计划政策 - Play 管理中心帮助.md"
]

def rename_files():
    for old_name, new_name in rename_map.items():
        if os.path.exists(old_name):
            try:
                os.rename(old_name, new_name)
                print(f"Renamed: '{old_name}' -> '{new_name}'")
            except Exception as e:
                print(f"Error renaming '{old_name}': {e}")
        else:
            print(f"File not found: '{old_name}'")

def delete_files():
    for file in delete_list:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"Deleted: '{file}'")
            except Exception as e:
                print(f"Error deleting '{file}': {e}")
        else:
            print(f"File not found (already deleted?): '{file}'")

if __name__ == "__main__":
    rename_files()
    delete_files()
