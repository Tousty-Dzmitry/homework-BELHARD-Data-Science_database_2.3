import sqlite3
import matplotlib.pyplot as plt
from sqlalchemy.sql import text
from sqlalchemy.dialects import sqlite
import csv


import pandas as pd

def load(data):
    # 1. Загрузка данных из CSV-файла
    # Укажите путь к вашему исходному файлу
    input_file = data  # замените на имя вашего исходного файла
    # Читаем CSV-файл в DataFrame
    df = pd.read_csv(input_file)
    # 2. Удаление строк с пропущенными значениями
    # Метод dropna() удаляет строки, содержащие хотя бы один пропуск (NaN)
    # Параметр inplace=True означает, что изменения применяются к исходному DataFrame
    df.dropna(inplace=True)    
    # 3. Сохранение очищенных данных в новый CSV-файл
    output_file = 'new_file.csv'  # можно задать любое имя
    # Сохраняем DataFrame в CSV без индекса (index=False)
    df.to_csv(output_file, index=False)
    return df, f"Загружено {len(df)} строк"
   




def percent(conn):
   
    cursor = conn.cursor()
    
    # 2. Запрашиваем данные для диаграммы (пример: распределение марок автомобилей)
    cursor.execute("""
        SELECT sports_car, COUNT(*) as count 
        FROM cars 
        GROUP BY sports_car  
        ORDER BY count DESC
    """)
    data = cursor.fetchall()
 
    # 3. Подготавливаем данные для диаграммы
    sports_car = [row[0] for row in data]
    counts = [row[1] for row in data]
    
    # 4. Создаем круговую диаграмму
    plt.figure(figsize=(8, 8))
    plt.pie(
        counts,
        labels=sports_car,
        autopct='%1.1f%%',
        startangle=90,
        shadow=True,
        explode=[0.1 if max(counts) == count else 0 for count in counts]  # Выделяем самый большой сегмент
    )
    
    # 5. Добавляем заголовок и настройки
    plt.title('Количество спортивных автомобилей', fontsize=16)
    plt.axis('equal')  # Чтобы диаграмма была круглой
    
    # 6.показываем диаграмму
   
    return plt.show()









