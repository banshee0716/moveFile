import os
import shutil
import re
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

def filter_files_with_content(src, content):
    # 使用正則表達式來過濾檔案
    pattern = re.compile(content)
    files = [f for f in os.listdir(src) if pattern.search(f)]
    return files

def move_files_with_content(src, dst, content, progress):
    # 檢查目標資料夾是否存在，不存在則創建
    if not os.path.exists(dst):
        os.makedirs(dst)

    files = filter_files_with_content(src, content)
    total_files = len(files)

    for i, filename in enumerate(files, 1):
        shutil.move(os.path.join(src, filename), os.path.join(dst, filename))
        progress["value"] = (i / total_files) * 100
        window.update_idletasks()

    messagebox.showinfo("完成", "所有檔案搬移完成！")

def delete_files_with_content(src, content, progress):
    files = filter_files_with_content(src, content)
    total_files = len(files)

    # 詢問是否確定刪除
    message = f"你現在要刪除的是「{src}」中關鍵字為「{content}」的文件，這個操作會讓你永久刪除此檔案，確定要刪除嗎？"
    answer = messagebox.askquestion("確認", message, icon="warning")
    if answer == "yes":
        for i, filename in enumerate(files, 1):
            full_path = os.path.join(src, filename)
            # 判斷是檔案還是資料夾，選擇適當的方法來刪除
            if os.path.isfile(full_path):
                os.remove(full_path)
            elif os.path.isdir(full_path):
                shutil.rmtree(full_path)
            progress["value"] = (i / total_files) * 100
            window.update_idletasks()

        messagebox.showinfo("完成", "所有檔案及資料夾刪除完成！")
    else:
        messagebox.showinfo("取消", "操作已取消！")

def rename_files_with_content(src, old_content, new_content, progress):
    # 使用正則表達式來過濾檔案
    pattern = re.compile(old_content)
    files = [f for f in os.listdir(src) if pattern.search(f)]
    total_files = len(files)

    for i, filename in enumerate(files, 1):
        # 進行替換操作，並修改檔案名稱
        new_filename = re.sub(old_content, new_content, filename)
        os.rename(os.path.join(src, filename), os.path.join(src, new_filename))
        progress['value'] = (i / total_files) * 100
        window.update_idletasks()

    messagebox.showinfo("完成", "所有檔案重新命名完成！")

def browse_directory():
    folder_selected = filedialog.askdirectory()
    return folder_selected

def create_gui():
    global window
    window = tk.Tk()
    window.title("檔案搬移與刪除工具")

    tk.Label(window, text="源資料夾:").grid(row=0)
    tk.Label(window, text="目標資料夾:").grid(row=1)
    tk.Label(window, text="檔案關鍵字/正則表達式:").grid(row=2)
    tk.Label(window, text="新的檔案名稱:").grid(row=3)

    src_entry = tk.Entry(window)
    dst_entry = tk.Entry(window)
    content_entry = tk.Entry(window)
    new_content_entry = tk.Entry(window)

    src_entry.grid(row=0, column=1)
    dst_entry.grid(row=1, column=1)
    content_entry.grid(row=2, column=1)
    new_content_entry.grid(row=3, column=1)

    src_browse_button = tk.Button(
        window, text="瀏覽", command=lambda: src_entry.insert(0, browse_directory())
    )
    dst_browse_button = tk.Button(
        window, text="瀏覽", command=lambda: dst_entry.insert(0, browse_directory())
    )

    src_browse_button.grid(row=0, column=2)
    dst_browse_button.grid(row=1, column=2)

    progress = ttk.Progressbar(window, length=200, mode="determinate")
    progress.grid(row=6, column=0, columnspan=3, pady=10)

    move_button = tk.Button(
        window,
        text="搬移檔案",
        command=lambda: move_files_with_content(
            src_entry.get(), dst_entry.get(), content_entry.get(), progress
        ),
    )
    move_button.grid(row=4, column=1, pady=10)

    delete_button = tk.Button(
        window,
        text="刪除檔案",
        command=lambda: delete_files_with_content(
            src_entry.get(), content_entry.get(), progress
        ),
    )
    delete_button.grid(row=5, column=1, pady=10)

    rename_button = tk.Button(
        window,
        text="修改檔案名稱",
        command=lambda: rename_files_with_content(
            src_entry.get(), content_entry.get(), new_content_entry.get(), progress
        ),
    )
    rename_button.grid(row=4, column=2, pady=10)

    window.mainloop()

create_gui()


"""
在這個新添加的 rename_files_with_content 函數中，我們使用 re.sub() 函數來將檔案名稱中的舊關鍵詞替換為新關鍵詞，然後使用 os.rename() 函數來修改檔案的名稱。我們還在 GUI 中添加了一個新的輸入框來讓用戶輸入新的關鍵詞，以及一個按鈕來觸發這個新的功能。
請注意，re.sub() 函數會替換檔案名稱中所有匹配到的關鍵詞。如果你只希望替換檔案名稱中的第一個關鍵詞，可以傳入一個額外的參數 count=1 給 re.sub() 函數。
另外，這段程式碼並未處理檔案名稱已存在的情況。如果新的檔案名稱已經存在於目標資料夾中，則 os.rename() 函數將會引發一個錯誤。如果需要處理這種情況，可以在重命名檔案之前先檢查新的檔案名稱是否已經存在。
"""