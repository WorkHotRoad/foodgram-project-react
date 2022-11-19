from django.core.exceptions import ValidationError
import os.path

def validate_size(value):
    max_upload_size = 5242880
    if os.path.getsize(value) > max_upload_size:
        raise ValidationError('Максимальный размер картинки не более 5мб')
    return value
