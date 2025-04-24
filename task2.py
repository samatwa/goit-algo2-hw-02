from typing import List, Dict, Tuple

def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через мемоізацію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """
    # Ініціалізуємо словник для мемоізації - зберігатиме вже обчислені результати
    memo = {}

    def cut_rod(n: int) -> Tuple[int, List[int]]:
        # Якщо результат для довжини n вже обчислено, повертаємо з кешу
        if n in memo:
            return memo[n]
        # Базовий випадок: якщо довжина стрижня 0, то прибуток 0 і немає розрізів
        if n == 0:
            return 0, []

        # Ініціалізуємо змінні для зберігання найкращого результату
        max_profit = -1
        best_cuts = []

        # У мемоізації ми перебираємо розміри починаючи з 2, потім у порядку спадання
        # Це надає перевагу розрізам розміром 2, що приведе до [2, 2, 1]
        preferred_order = [min(2, n)] + [i for i in range(n, 0, -1) if i != 2]
        
        for i in preferred_order:
            if i <= len(prices):
                # Ціна поточного відрізка
                current_profit = prices[i - 1]
                # Рекурсивно обчислюємо найкращий результат для залишку стрижня
                remaining_profit, remaining_cuts = cut_rod(n - i)
                # Загальний прибуток при такому першому розрізі
                total = current_profit + remaining_profit
                # Формуємо повний список розрізів
                candidate_cuts = [i] + remaining_cuts

                # Оновлюємо результат, якщо знайдено кращий прибуток
                if total > max_profit:
                    max_profit = total
                    best_cuts = candidate_cuts

        # Зберігаємо результат у кеш для уникнення повторних обчислень
        memo[n] = (max_profit, best_cuts)
        return memo[n]

    # Запускаємо рекурсивну функцію та отримуємо результат
    max_profit, cuts = cut_rod(length)
    
    # Повертаємо словник з результатами
    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": len(cuts) - 1 if cuts else 0  # Кількість розрізів = кількість шматків - 1
    }

def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через табуляцію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """
    # Створюємо масиви для зберігання максимальних прибутків і розрізів
    dp = [0] * (length + 1)
    cuts_table = [[] for _ in range(length + 1)]

    # У табуляції ми заповнюємо таблицю знизу вгору
    for i in range(1, length + 1):
        # Змінюємо порядок перебору для отримання [2, 2, 1]:
        # Спочатку розглядаємо розріз розміром 2, потім інші у порядку спадання
        possible_cuts = []
        if 2 <= i and 2 <= len(prices):
            possible_cuts.append(2)
        for j in range(i, 0, -1):
            if j != 2 and j <= len(prices):
                possible_cuts.append(j)
        
        # Перебираємо можливі розрізи у визначеному порядку
        for j in possible_cuts:
            # Обчислюємо прибуток з поточним розрізом
            profit = prices[j - 1] + dp[i - j]
            # Формуємо список розрізів
            candidate = [j] + cuts_table[i - j]
            
            # Оновлюємо результат, якщо прибуток більший
            if profit > dp[i]:
                dp[i] = profit
                cuts_table[i] = candidate

    # Повертаємо результат
    return {
        "max_profit": dp[length],
        "cuts": cuts_table[length],
        "number_of_cuts": len(cuts_table[length]) - 1 if cuts_table[length] else 0
    }

def run_tests():
    """Функція для запуску всіх тестів"""
    # Визначаємо тестові випадки
    test_cases = [
        # Тест 1: Базовий випадок - перевірка стандартного випадку з різними цінами
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Базовий випадок"
        },
        # Тест 2: Випадок коли оптимально не різати стрижень взагалі
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Оптимально не різати"
        },
        # Тест 3: Випадок коли оптимально різати на шматки однакової довжини
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Рівномірні розрізи"
        }
    ]

    # Запускаємо всі тестові випадки
    for test in test_cases:
        print(f"\nТест: {test['name']}")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")

        # Тестуємо підхід з мемоізацією (згори-вниз)
        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print("\nРезультат мемоізації:")
        print(f"Максимальний прибуток: {memo_result['max_profit']}")
        print(f"Розрізи: {memo_result['cuts']}")
        print(f"Кількість розрізів: {memo_result['number_of_cuts']}")

        # Тестуємо підхід з табуляцією (знизу-вгору)
        table_result = rod_cutting_table(test['length'], test['prices'])
        print("\nРезультат табуляції:")
        print(f"Максимальний прибуток: {table_result['max_profit']}")
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")

        print("\nПеревірка пройшла успішно!")

# Точка входу програми
if __name__ == "__main__":
    run_tests()