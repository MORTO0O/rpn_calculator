OPERATOR_PRIORITY = {
    '~': 4, '@': 4,
    '**': 3,
    '/': 2, '*': 2, '//': 2, '%': 2,
    '+': 1, '-': 1
}

ERROR_MESSAGES = {
    'empty_expression': "Пустое выражение.",
    'unknown_operator': "Неизвестный оператор: '{}'.",
    'insufficient_operands': "Нехватка операндов для выполнения операции: '{}'.",
    'invalid_expression': "Некорректное выражение. В стеке осталось значений: {}.",
    'unbalanced_brackets': "Неверно поставлены скобки.",
    'unknown_token': "Неизвестный токен: {}.",
    'division_by_zero': "Деление на ноль.",
    'integer_division_by_zero': "Целочисленное деление на ноль.",
    'modulo_by_zero': "Деление по модулю на ноль.",
    'integer_division_type_error': "Целочисленное деление требует целочисленные операнды.",
}

WARNING_MESSAGES = {
    'empty_expression': "Пустое выражение.",
    'zero_pow_zero': "0^0 - неопределенность, возвращаю '1'",
    'negative_base_fractional': "Отрицательное основание {} и дробная степень {} могут дать комплексное число",
    'result_too_large': "Результат {} слишком большой",
    'overflow': "Переполнение",
}