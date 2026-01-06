from django.core.files.uploadedfile import UploadedFile
from django.core.validators import BaseValidator


class MaxFileSizeValidator(BaseValidator):
    message = 'Максимально разрешенный размер файла: %(limit_value)s байт.'
    code = 'max_file_size'

    def compare(self, file: UploadedFile, max_size: int) -> bool:
        return file.size >= max_size
