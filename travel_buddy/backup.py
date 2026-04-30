import os
import shutil
from datetime import datetime

# Пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3')
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')

# Создаём папку для бэкапов, если её нет
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# Имя файла бэкапа с датой
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
backup_name = f'db_backup_{timestamp}.sqlite3'
backup_path = os.path.join(BACKUP_DIR, backup_name)

# Копируем базу данных
try:
    shutil.copy2(DB_PATH, backup_path)
    print(f'✅ Бэкап создан: {backup_path}')
    
    # Удаляем старые бэкапы (оставляем только последние 10)
    backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith('db_backup_')])
    if len(backups) > 10:
        for old_backup in backups[:-10]:
            os.remove(os.path.join(BACKUP_DIR, old_backup))
            print(f'🗑️ Удалён старый бэкап: {old_backup}')
except Exception as e:
    print(f'❌ Ошибка при создании бэкапа: {e}')