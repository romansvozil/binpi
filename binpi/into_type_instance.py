from binpi import DeserializedT


def _get_value(type, value):
    if isinstance(value, list):
        item_type = type.type
        return [_get_value(item_type, item) for item in value]
    elif isinstance(value, dict):
        instance = type()
        for key, val in value.items():
            setattr(instance, key, _get_value(type.__dict__.get(key), val))
        return instance
    else:
        return value


def into_type_instance(type: type[DeserializedT], data) -> DeserializedT:
    return _get_value(type, data)
