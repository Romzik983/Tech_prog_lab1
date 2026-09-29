import os
import sys
import platform
import psutil
import json

system = platform.system()
memory = psutil.virtual_memory()
disk = psutil.disk_usage('/')
net = psutil.net_io_counters()
process = {}

for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
    try:
        pid = proc.info['pid']
        name = proc.info['name']
        proc_memory = proc.info['memory_info']
        proc_memory = proc_memory.rss / (1024**2)
        if proc_memory > 100:
            process[pid] = name
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, AttributeError):
        pass

data = {
    "ОС": system,
    "Детали ОС": None ,
    "Оболочка командной строки": None,
    "Версия ОС": platform.release(),
    
    "Архитектура CPU": platform.machine(),
    "Модель процессора": platform.processor(),
    "Доступно ядер CPU": os.cpu_count(),
    "Порядок байтов процессора": sys.byteorder,

    "Общая оперативная память": f"{memory.total / (1024**3):.2f} ГБ",
    "Доступная оперативная память": f"{memory.available / (1024**3):.2f} ГБ",
    "Использовано оперативной памяти": f"{memory.used / (1024**3):.2f} ГБ",

    "Всего памяти на диске": f"{disk.total / (1024**3):.2f} ГБ",
    "Свободно памяти на диске": f"{disk.free / (1024**3):.2f} ГБ",
    "Процент заполнения диска": f"{disk.percent}%",

    "Сеть: Отправлено": f"{net.bytes_sent / (1024**2):.2f} Мб",
    "Сеть: Получено": f"{net.bytes_recv / (1024**2):.2f} Мб",

    "Текущая рабочая директория": os.getcwd(),
    "Список пользователей, вошедших в систему (null - пользователи, к которым нет доступа; время - время с 1 января 1970 года)": psutil.users(),
    "Имя пользователя": None,
    "Hostname": platform.node(),
    "Список папок, где ОС ищет исполняемые файлы программы": os.environ.get('PATH'),
    "Путь к домашней папке пользователя": None,

    "Запущенные процессы, которые занимают больше 100 Мб оперативной памяти": process,

    "Версия Python": sys.version,
    "Компилятор Python": platform.python_compiler(),
    "Реализация Python": platform.python_implementation(),
    
    "ID процесса": os.getpid(),

    "Зарядка (ноутбук)": psutil.sensors_battery(),
}    

if system == 'Linux':
    data["ОС"] = 'Linux'
    data["Детали ОС"] = platform.libc_ver()
    data["Оболочка командной строки"] = os.environ.get('SHELL')
    data["Имя пользователя"] = os.environ.get('USER')
    data["Путь к домашней папке пользователя"] = os.environ.get('HOME')
elif system == 'Windows':
    data["ОС"] = 'Windows'
    data["Детали ОС"] = platform.win32_ver()
    data["Оболочка командной строки"] = os.environ.get('COMSPEC')
    data["Имя пользователя"] = os.environ.get('USERNAME')
    data["Путь к домашней папке пользователя"] = os.environ.get('USERPROFILE')
elif system == 'Darwin':
    data["ОС"] = 'MacOS'
    data["Детали ОС"] = platform.mac_ver()
    data["Оболочка командной строки"] = os.environ.get('SHELL')
    data["Имя пользователя"] = os.environ.get('USER')
    data["Путь к домашней папке пользователя"] = os.environ.get('HOME')



with open('system_info.json', 'w', encoding = 'utf-8') as file:
    json.dump(data, file, indent = 4, ensure_ascii = False)
