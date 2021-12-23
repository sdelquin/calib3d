def format_value(
    value,
    lt_color='green',
    eq_color='cyan',
    gt_color='red',
    threshold=0,
    format='.2f',
    suffix='',
):
    scale = abs(value)
    if scale < threshold:
        color = lt_color
    elif scale > threshold:
        color = gt_color
    else:
        color = eq_color
    return f'[{color}]{value:{format}}{suffix}[/{color}]'
