import sqlite3
import matplotlib.pyplot as plt
import pandas as pd

def get_car_stats(db_path):
    """Получаем статистику по первому слову в названии автомобилей"""
    conn = sqlite3.connect(db_path)
    
    query = """
        WITH split_names AS (
            SELECT 
                CASE 
                    WHEN INSTR(TRIM(name), ' ') > 0 
                    THEN SUBSTR(TRIM(name), 1, INSTR(TRIM(name), ' ') - 1)
                    ELSE TRIM(name)
                END as brand
            FROM cars
        )
        SELECT 
            brand,
            COUNT(*) as count
        FROM split_names
        GROUP BY brand
        ORDER BY count DESC
    """
    
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def plot_brand_distribution(df, top_n=15):
    """Строим столбчатую диаграмму распределения марок"""
    plt.figure(figsize=(14, 7))
    plt.style.use('seaborn-v0_8')
    
    if len(df) > top_n:
        top = df.head(top_n)
        others = pd.DataFrame({
            'brand': ['Другие'],
            'count': [df['count'].iloc[top_n:].sum()]
        })
        df = pd.concat([top, others])
    
    colors = plt.cm.tab20c(range(len(df)))
    bars = plt.bar(df['brand'], df['count'], color=colors)
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:,}',
                ha='center', va='bottom',
                fontsize=9)
    
    plt.title(f'Распределение автомобилей по маркам (первые слова, топ-{top_n})', 
              fontsize=16, pad=20)
    plt.xlabel('Первое слово в названии', fontsize=12)
    plt.ylabel('Количество', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.gca().yaxis.set_major_formatter(plt.ticker.StrMethodFormatter('{x:,.0f}'))
    plt.tight_layout()
    plt.savefig('car_brands_first_word.png', dpi=120, bbox_inches='tight')
    plt.show()

def analyze_car_brands(db_path='cars.db', top_n=15):
    """
    Анализ и визуализация распределения автомобилей по маркам
    Параметры:
        db_path (str): путь к файлу базы данных (по умолчанию 'cars.db')
        top_n (int): количество топовых марок для отображения (по умолчанию 15)
    """
    try:
        car_data = get_car_stats(db_path)
        print("Топ-10 первых слов в названиях марок:")
        print(car_data.head(10))
        plot_brand_distribution(car_data, top_n)
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")