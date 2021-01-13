from django.core.exceptions import ValidationError


def validate_correct_year_of_production(value):
    if value < 1888 or value >= 3000:
        raise ValidationError(
            '%(value)s is not a correct year',
            params={'value': value}
        )


def validate_correct_duration(value):
    if value < 0 or value > 600:
        raise ValidationError(
            '%(value)s is not a correct duration',
            params={'value': value}
        )


def validate_correct_no_places(value):
    if value < 0 or value > 400:
        raise ValidationError(
            '%(value)s is not a correct number of places',
            params={'value': value}
        )
