def raise_type_error(arg_name, value, value_class):
    raise TypeError(
        f'Invalid value for {arg_name}! Got "{value}". Instance of "{value_class}" expected.')
