import warnings
from rpn_calc import RPNCalculator


def main() -> None:
    calculator = RPNCalculator()

    print("ДОБРО ПОЖАЛОВАТЬ В КАЛЬКУЛЯТОР ОБРАТНОЙ ПОЛЬСКОЙ НОТАЦИИ!")
    print("Для завершения работы калькулятора введите 'q/quit/exit'")

    while True:
        try:
            expression = input("Введите выражение> ").strip()

            if expression.lower() in ['q', 'quit', 'exit']:
                print("ДО СВИДАНИЯ!")
                break

            if not expression:
                with warnings.catch_warnings(record=True) as warning_list:
                    warnings.simplefilter("always")
                    calculator.evaluate_expression("")
                    for warning in warning_list:
                        print(f"Ахтунг: {warning.message}")
                continue

            with warnings.catch_warnings(record=True) as warning_list:
                warnings.simplefilter("always")
                result = calculator.evaluate_expression(expression)

                for warning in warning_list:
                    print(f"Ахтунг: {warning.message}")

                print(f"Ответ: {result}")

        except KeyboardInterrupt:
            print("\nДО СВИДАНИЯ!")
            break

        except Exception as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()