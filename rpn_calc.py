import warnings
from typing import Union, List, Tuple, Callable
from consts import (
    OPERATOR_PRIORITY,
    ERROR_MESSAGES,
    WARNING_MESSAGES
)

class RPNCalculator:

    def __init__(self) -> None:
        self.operators = {
            '+': (self._add, 2),
            '-': (self._sub, 2),
            '*': (self._mul, 2),
            '/': (self._true_divide, 2),
            '%': (self._modulo, 2),
            '//': (self._integer_divide, 2),
            '**': (self._pow, 2),
            '@': (self._unary_plus, 1),
            '~': (self._unary_minus, 1),
        }

    def _add(self, a: int | float, b: int | float) -> int | float:
        """
        Сложение двух чисел.
        Arguments:
            a: Первое число
            b: Второе число
        Returns:
            Результат сложения
        """
        return a + b

    def _sub(self, a: int | float, b: int | float) -> int | float:
        """
        Вычитание двух чисел.
        Arguments:
            a: Первое число
            b: Второе число
        Returns:
            Результат вычитания
        """
        return a - b

    def _mul(self, a: int | float, b: int | float) -> int | float:
        """
        Умножение двух чисел.
        Arguments:
            a: Первое число
            b: Второе число
        Returns:
            Результат умножения
        """
        return a * b

    def _modulo(self, a: int, b: int) -> int:
        """
        Остаток от деления.
        Arguments:
            a: Делимое
            b: Делитель

        Returns:
            Остаток от деления
        Raises:
            ZeroDivisionError: Если делитель равен нулю
            TypeError: Если операнды не целые числа
        """
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError(ERROR_MESSAGES['integer_division_type_error'])
        if b == 0:
            raise ZeroDivisionError(ERROR_MESSAGES['modulo_by_zero'])
        return a % b

    def _true_divide(self, a: Union[int, float], b: Union[int, float]) -> float:
        """
        Вещественное деление.
        Arguments:
            a: Делимое
            b: Делитель
        Returns:
            Результат деления
        Raises:
            ZeroDivisionError: Если делитель равен нулю
        """
        if b == 0:
            raise ZeroDivisionError(ERROR_MESSAGES['division_by_zero'])
        return a / b

    def _pow(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """
        Возведение в степень.
        Arguments:
            a: Основание
            b: Показатель степени
        Returns:
            Результат возведения в степень
        """
        if a == 0 and b == 0:
            warnings.warn(WARNING_MESSAGES['zero_pow_zero'], RuntimeWarning)
            return 1

        if a < 0 and not isinstance(b, int) and b != int(b):
            warnings.warn(
                WARNING_MESSAGES['negative_base_fractional'].format(a, b),
                RuntimeWarning
            )

        try:
            result = a ** b
            if abs(result) > 1e308:
                warnings.warn(
                    WARNING_MESSAGES['result_too_large'].format(result),
                    RuntimeWarning
                )
            return result
        except OverflowError:
            warnings.warn(WARNING_MESSAGES['overflow'], RuntimeWarning)
            return float('inf') if a > 0 else float('-inf')
        except ValueError as error:
            raise ValueError(f"Математическая ошибка: {error}")

    def _integer_divide(self, a: int, b: int) -> int:
        """
        Целочисленное деление.
        Arguments:
            a: Делимое
            b: Делитель
        Returns:
            Результат целочисленного деления
        Raises:
            ZeroDivisionError: Если делитель равен нулю
            TypeError: Если операнды не целые числа
        """
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError(ERROR_MESSAGES['integer_division_type_error'])
        if b == 0:
            raise ZeroDivisionError(ERROR_MESSAGES['integer_division_by_zero'])
        return a // b

    def _unary_minus(self, a: int | float) -> int | float:
        """
        Унарный минус.
        Arguments:
            a: Число
        Returns:
            Число с противоположным знаком
        """
        return -a

    def _unary_plus(self, a: int | float) -> int | float:
        """
        Унарный плюс.
        Arguments:
            a: Число
        Returns:
            То же число
        """
        return a

    def _tokenize(self, expression: str) -> List[int | float | str]:
        """
        Разбивает выражение на токены.
        Arguments:
            expression: Строка с выражением
        Returns:
            Список токенов (числа и операторы)
        """
        tokens = []
        for token in expression.split():
            if not token:
                continue

            try:
                if '.' in token:
                    tokens.append(float(token))
                else:
                    tokens.append(int(token))
            except ValueError:
                tokens.append(token)
        return tokens

    def _infix_to_rpn(self, expression: str) -> str:
        """
        Преобразует инфиксное выражение в обратную польскую нотацию.
        Arguments:
            expression: Инфиксное выражение
        Returns:
            Выражение в обратной польской нотации
        Raises:
            ValueError: При несбалансированных скобках или неизвестных токенах
        """
        output = []
        stack = []
        tokens = self._tokenize(expression)

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if isinstance(token, (int, float)):
                output.append(str(token))
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack:
                    raise ValueError(ERROR_MESSAGES['unbalanced_brackets'])
                stack.pop()
            elif token in self.operators:
                if token in ('~', '@'):
                    if (i == 0 or
                            (isinstance(tokens[i - 1], str) and tokens[i - 1] in '(+*/%-')):
                        stack.append(token)
                    else:
                        while (stack and stack[-1] != '(' and
                               OPERATOR_PRIORITY.get(token, 0) <= OPERATOR_PRIORITY.get(stack[-1], 0)):
                            output.append(stack.pop())
                        stack.append(token)
                else:
                    while (stack and stack[-1] != '(' and
                           OPERATOR_PRIORITY.get(token, 0) <= OPERATOR_PRIORITY.get(stack[-1], 0)):
                        output.append(stack.pop())
                    stack.append(token)
            else:
                raise ValueError(ERROR_MESSAGES['unknown_token'].format(token))
            i += 1

        while stack:
            if stack[-1] == '(':
                raise ValueError(ERROR_MESSAGES['unbalanced_brackets'])
            output.append(stack.pop())

        return ' '.join(output)

    def evaluate_expression(self, expression: str) -> int | float:
        """
        Вычисляет значение выражения.
        Arguments:
            expression: Выражение для вычисления
        Returns:
            Результат вычисления
        Raises:
            ValueError: При некорректном выражении
            ZeroDivisionError: При делении на ноль
            TypeError: При несовместимых типах операндов
        """
        if not expression.strip():
            warnings.warn(WARNING_MESSAGES['empty_expression'], UserWarning)
            return 0

        if '(' in expression and ')' in expression:
            expression = self._infix_to_rpn(expression)

        stack = []
        tokens = self._tokenize(expression)

        for token in tokens:
            if isinstance(token, (int, float)):
                stack.append(token)
            else:
                if token not in self.operators:
                    raise ValueError(ERROR_MESSAGES['unknown_operator'].format(token))

                func, num_args = self.operators[token]

                if len(stack) < num_args:
                    raise ValueError(ERROR_MESSAGES['insufficient_operands'].format(token))

                if num_args == 1:
                    operand = stack.pop()
                    result = func(operand)
                    stack.append(result)
                else:
                    right = stack.pop()
                    left = stack.pop()
                    result = func(left, right)
                    stack.append(result)

        if len(stack) != 1:
            raise ValueError(ERROR_MESSAGES['invalid_expression'].format(len(stack)))

        return stack[0]