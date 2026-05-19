import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from utils.validators import MaxFileSizeValidator


def test_max_file_size_validator_allows_file_smaller_than_limit():
    validator = MaxFileSizeValidator(limit_value=10)

    file = SimpleUploadedFile(
        name='test.txt',
        content=b'12345',  # 5 байт
        content_type='text/plain',
    )

    validator(file)


def test_max_file_size_validator_raises_error_when_file_equals_limit():
    validator = MaxFileSizeValidator(limit_value=5)

    file = SimpleUploadedFile(
        name='test.txt',
        content=b'12345',  # 5 байт
        content_type='text/plain',
    )

    with pytest.raises(ValidationError) as exc_info:
        validator(file)

    assert exc_info.value.code == 'max_file_size'


def test_max_file_size_validator_raises_error_when_file_larger_than_limit():
    validator = MaxFileSizeValidator(limit_value=5)

    file = SimpleUploadedFile(
        name='test.txt',
        content=b'123456',  # 6 байт
        content_type='text/plain',
    )

    with pytest.raises(ValidationError) as exc_info:
        validator(file)

    assert exc_info.value.code == 'max_file_size'
