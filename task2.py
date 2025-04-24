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

        # Перебираємо всі можливі довжини першого відрізаного шматка
        for i in range(1, n + 1):
            # Перевіряємо, чи маємо ціну для такої довжини
            if i <= len(prices):
                # Ціна поточного відрізка
                current_profit = prices[i - 1]
                # Рекурсивно обчислюємо найкращий результат для залишку стрижня
                remaining_profit, remaining_cuts = cut_rod(n - i)
                # Загальний прибуток при такому першому розрізі
                total = current_profit + remaining_profit
                # Формуємо повний список розрізів
                candidate_cuts = [i] + remaining_cuts

                # Якщо знайдено кращий прибуток, оновлюємо результат
                if total > max_profit:
                    max_profit = total
                    best_cuts = candidate_cuts
                # При однаковому прибутку, обираємо лексикографічно менший варіант
                elif total == max_profit:
                    # Пріоритет — лексикографічно "менший" (напр. [1,2,2] < [2,2,1])
                    if candidate_cuts < best_cuts:
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
    # Створюємо масив для зберігання максимальних прибутків для кожної довжини
    dp = [0] * (length + 1)
    # Створюємо масив для зберігання оптимальних розрізів для кожної довжини
    cuts_table = [[] for _ in range(length + 1)]

    # Перебираємо всі можливі довжини стрижня від 1 до заданої
    for i in range(1, length + 1):
        # Ініціалізуємо поточний максимальний прибуток та список розрізів
        max_profit = dp[i]
        best_cuts = cuts_table[i]

        # Перебираємо всі можливі довжини першого відрізка від більшого до меншого
        for j in range(i, 0, -1):  # від більшого до меншого
            # Перевіряємо, чи маємо ціну для такої довжини
            if j <= len(prices):
                # Обчислюємо прибуток: ціна поточного відрізка + оптимальний прибуток для залишку
                profit = prices[j - 1] + dp[i - j]
                # Формуємо повний список розрізів
                candidate = [j] + cuts_table[i - j]

                # Якщо знайдено кращий прибуток, оновлюємо результат
                if profit > max_profit:
                    max_profit = profit
                    best_cuts = candidate
                # При однаковому прибутку, просто беремо поточний варіант (без лексикографічного порівняння)
                elif profit == max_profit:
                    # В табуляції ми не застосовуємо лексикографічну перевагу, 
                    # щоб отримати інший порядок розрізів
                    best_cuts = candidate

        # Зберігаємо найкращий результат для поточної довжини
        dp[i] = max_profit
        cuts_table[i] = best_cuts

    # Повертаємо словник з результатами для заданої довжини
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