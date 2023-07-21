def refactor_data(input_str: str):
    PREFIX = '준'
    SUFFIX = '급'
    TARGET_SUBSTRING = 'ii'
    processed_str = input_str.strip('__')
    if processed_str.endswith(TARGET_SUBSTRING):
        processed_str = PREFIX + processed_str.strip('ii')
    return processed_str + SUFFIX