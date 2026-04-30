from django.core.management.base import BaseCommand
import os
import shutil
from datetime import datetime

class Command(BaseCommand):
    help = 'Создаёт резервную копию базы данных'

    def handle(self, *args, **options):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3')
        BACKUP_DIR = os.path.join(BASE_DIR, 'backups')

        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'db_backup_{timestamp}.sqlite3'
        backup_path = os.path.join(BACKUP_DIR, backup_name)

        try:
            shutil.copy2(DB_PATH, backup_path)
            self.stdout.write(self.style.SUCCESS(f'✅ Бэкап создан: {backup_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка: {e}'))