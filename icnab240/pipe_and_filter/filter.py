def filter_segment(fields, segment):
    """Filters segments given a string to filter check if on identifier

    :param fields: a list in that each element is type Field
    :param segment: str to be used in the filter
    :return: a list in that each element is type Field and was filtered
    """
    fields_filtered = [field for field in fields if segment in field.identifier]
    return fields_filtered


def filter_none(fields):
    fs = []
    for field in fields:
        if field.value is not None and ".5" in field.identifier:
            if "None" in field.value:
                fs.append(field)
    return fs


def filter_segment_and_value_none(fields, segment):
    """Filters segments given a string to filter check if on identifier

    :param fields: a list in that each element is type Field
    :param segment: str to used in the filter
    :return: a list in that each element is type Field and was filtered
    """
    fields_filtered = [
        field for field in fields if segment in field.identifier and field.value is None
    ]
    return fields_filtered


def generic_filter(fields, atribute_to_search, value_to_search):
    for field in fields:
        if getattr(field, atribute_to_search) == value_to_search:
            return field
