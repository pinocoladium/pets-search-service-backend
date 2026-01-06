from django.core.validators import RegexValidator


phone_validator = RegexValidator(
    regex=r'^\d{11}$',
)

name_validator = RegexValidator(
    regex=r'^[a-zA-Zа-яёА-ЯЁ\s\-]*$',
)
