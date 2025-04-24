from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """
    # Перетворюємо словники завдань у об'єкти PrintJob
    jobs = [PrintJob(**job) for job in print_jobs]
    
    # Створюємо пари (початковий індекс, завдання) для збереження порядку
    jobs_with_index = [(i, job) for i, job in enumerate(jobs)]
    
    # Створюємо об'єкт обмежень принтера
    printer = PrinterConstraints(**constraints)
    
    # Сортуємо за пріоритетом, зберігаючи початковий порядок при однакових пріоритетах
    jobs_with_index.sort(key=lambda x: (x[1].priority, x[0]))
    
    # Отримуємо відсортований список завдань
    sorted_jobs = [job for _, job in jobs_with_index]
    
    # Списки для відстеження результатів
    print_order = []
    total_time = 0
    
    # Обробляємо завдання
    i = 0
    while i < len(sorted_jobs):
        
        # Поточна група для друку
        current_batch = []
        current_volume = 0
        max_print_time = 0
        
        # Спробуємо додати завдання до поточної групи
        j = i
        while j < len(sorted_jobs) and len(current_batch) < printer.max_items:
            job = sorted_jobs[j]
            
            # Перевіряємо, чи можна додати завдання до поточної групи
            if current_volume + job.volume <= printer.max_volume:
                current_batch.append(job)
                current_volume += job.volume
                max_print_time = max(max_print_time, job.print_time)
                j += 1
            else:
                # Якщо завдання не поміщається, але група порожня,додаємо його окремо
                if not current_batch:
                    current_batch.append(job)
                    max_print_time = job.print_time
                    j += 1
                else:
                    # Інакше завершуємо формування поточної групи
                    break
        
        # Додаємо ID завдань з поточної групи до порядку друку
        for job in current_batch:
            print_order.append(job.id)
        
        # Додаємо час друку поточної групи до загального часу
        total_time += max_print_time
        
        # Переходимо до наступної групи завдань
        i = j
    
    return {
        "print_order": print_order,
        "total_time": total_time
    }

# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # дипломна
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")

if __name__ == "__main__":
    test_printing_optimization()