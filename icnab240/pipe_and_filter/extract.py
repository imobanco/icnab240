from .filter import filter_segment


def extract_identifiers(fields, patterns):
    """

    :param fields:
    :param patterns:
    :return:
    """
    filtered_fields = []
    for pattern in patterns:
        filtered_fields.extend(filter_segment(fields, pattern))

    identifiers_list = [field.identifier for field in filtered_fields]

    identifiers = set(identifiers_list)

    return identifiers


def extract_identifiers_default(fields):
    """Extracts identifiers from fields that have default or reasonable_default

    :param fields: a list in that each element is type Field
    :return: set of identifiers from the given fields
    """
    filtered_fields = []
    for field in fields:
        if (
            field.reasonable_default is not None and field.reasonable_default != ""
        ) or (field.default is not None and field.default != ""):
            filtered_fields.append(field)

    identifiers_list = [field.identifier for field in filtered_fields]

    identifiers = set(identifiers_list)

    if len(identifiers_list) != len(identifiers):
        raise ValueError(
            f"The list identifiers_list have repeated values: {identifiers_list}"
        )

    return identifiers
