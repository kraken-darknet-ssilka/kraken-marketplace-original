# smart_zip.py
import os
import zipfile
from datetime import datetime

def zip_folder(source, ignore_file=".zipignore"):
    if not os.path.exists(source):
        print("❌ Папка не найдена.")
        return

    # Игнорируемые файлы/папки
    ignore_patterns = []
    if os.path.exists(ignore_file):
        with open(ignore_file) as f:
            ignore_patterns = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    # Имя архива
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"{os.path.basename(source)}_{timestamp}.zip"

    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source):
            # Убираем игнорируемые папки
            dirs[:] = [d for d in dirs if os.path.join(root, d) not in ignore_patterns]
            for file in files:
                filepath = os.path.join(root, file)
                # Проверка на игнор
                if any(pattern in filepath for pattern in ignore_patterns):
                    continue
                # Относительный путь в архиве
                arcname = os.path.relpath(filepath, start=source)
                zipf.write(filepath, arcname)
                print(f"✅ Добавлен: {arcname}")

    print(f"\n🎉 Архив создан: {zip_name}")

if __name__ == "__main__":
    folder = input("Папка для архивации: ").strip()
    zip_folder(folder)
