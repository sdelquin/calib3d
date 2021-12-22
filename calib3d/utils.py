def format_value(
    value,
    lt_color='red',
    eq_color='green',
    gt_color='cyan',
    threshold=0,
    format='.2f',
    suffix='',
):
    if value < threshold:
        color = lt_color
    elif value > threshold:
        color = gt_color
    else:
        color = eq_color
    return f'[{color}]{value:{format}}{suffix}[/{color}]'
