import warnings
from src.consts import (
    OPERATOR_PRIORITY,
    ERROR_MESSAGES,
    WARNING_MESSAGES
)

class RpnCalculator:
    def __init__(self):
        self.operators = {
            '+': (self._add, 2),
            '-': (self._subtract, 2),
            '*': (self._multiply, 2),
            '/': (self._true_divide, 2),
            '%': (self._modulo, 2),
            '//': (self._int_divide, 2),
            '**': (self._pow, 2),
            '@': (self._unary_plus, 1),
            '~': (self._unary_minus, 1),
        }

    def _add(self, a, b):
        """
        Сложение двух чисел.
        """
        return a + b

    def _subtract(self, a, b):
        """
        Вычитание двух чисел.
        """
        return a - b

    def _multiply(self, a, b):
        """
        Умножение двух чисел.
        """
        return a * b

    def _modulo(self, a, b):
        """
        Остаток от деления.
        """
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError(ERROR_MESSAGES['integer_division_type_error'])
        if b == 0:
            raise ZeroDivisionError(ERROR_MESSAGES['modulo_by_zero'])
        return a % b

    def _true_divide(self, a, b):
        """
        Вещественное деление.
        """
        if b == 0:
            raise ZeroDivisionError(ERROR_MESSAGES['division_by_zero'])
        return a / b

    def _pow(self, base, exponent):
        """
        Возведение в степень.
        """
        if base == 0 and exponent == 0:
            warnings.warn(WARNING_MESSAGES['zero_power_zero'], RuntimeWarning)
            return 1

        if base < 0 and not isinstance(exponent, int) and exponent != int(exponent):
            warnings.warn(
                WARNING_MESSAGES['negative_base_fractional'].format(base, exponent),
                RuntimeWarning
            )

        try:
            result = base ** exponent
            if abs(result) > 1e308:
                warnings.warn(
                    WARNING_MESSAGES['result_too_large'].format(result),
                    RuntimeWarning
                )
            return result
        except OverflowError:
            warnings.warn(WARNING_MESSAGES['overflow'], RuntimeWarning)
            return float('inf') if base > 0 else float('-inf')
        except ValueError as error:
            raise ValueError(f"Математическая ошибка: {error}")

    def _int_divide(self, a, b):
        """
        Целочисленное деление.
        """
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError(ERROR_MESSAGES['integer_division_type_error'])
        if b == 0:
            raise ZeroDivisionError(ERROR_MESSAGES['integer_division_by_zero'])
        return a // b

    def _unary_minus(self, operand):
        """
        Унарный минус.
        """
        return -operand

    def _unary_plus(self, operand):
        """
        Унарный плюс.
        """
        return operand

    def _tokenize(self, expression):
        """
        Разбивает выражение на токены.
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

    def _infix_to_rpn(self, expression):
        """
        Инфиксное -> RPN.
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

    def evaluate_expression(self, expression):
        """
        Вычисление значения выражения.
        """
        if not expression.strip():
            warnings.warn(WARNING_MESSAGES['empty_expression'], UserWarning)
            return 0

        # Если есть скобки, преобразуем в RPN.
        if '(' in expression or ')' in expression:
            expression = self._infix_to_rpn(expression)

        stack = []
        tokens = self._tokenize(expression)

        for token in tokens:
            if isinstance(token, (int, float)):
                stack.append(token)
            else:
                if token not in self.operators:
                    raise ValueError(ERROR_MESSAGES['unknown_operator'].format(token))

                operation_function, num_arguments = self.operators[token]

                if len(stack) < num_arguments:
                    raise ValueError(ERROR_MESSAGES['insufficient_operands'].format(token))

                if num_arguments == 1:
                    operand = stack.pop()
                    result = operation_function(operand)
                    stack.append(result)
                else:
                    b = stack.pop()
                    a = stack.pop()
                    result = operation_function(a, b)
                    stack.append(result)

        if len(stack) != 1:
            raise ValueError(ERROR_MESSAGES['invalid_expression'].format(len(stack)))

        return stack[0]