import warnings
from src.rpn_calc import RpnCalculator


def main() -> None:
    calculator = RpnCalculator()

    print("ДОБРО ПОЖАЛОВАТЬ В КАЛЬКУЛЯТОР ОБРАТНОЙ ПОЛЬСКОЙ НОТАЦИИ!")
    print("Для завершения работы калькулятора введите 'q'")

    while True:
        try:
            expression = input("Введите выражение: ").strip()

            if expression.lower() == 'q':
                print("ДО СВИДАНИЯ!")
                break

            if not expression:
                with warnings.catch_warnings(record=True) as warning_list:
                    warnings.simplefilter("always")
                    calculator.evaluate_expression("")
                    for warning in warning_list:
                        print(f"Предупреждение: {warning.message}")
                continue

            with warnings.catch_warnings(record=True) as warning_list:
                warnings.simplefilter("always")
                result = calculator.evaluate_expression(expression)

                for warning in warning_list:
                    print(f"Предупреждение: {warning.message}")

                print(f"Ответ: {result}")

        except KeyboardInterrupt:
            print("\nДО СВИДАНИЯ!")
            break

        except Exception as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()