from django import template

register = template.Library()

@register.filter
def humanize_number(number: int) -> str:
    try:
        number = int(number)
        if number >= 1000000:
            return f'{number//1000000:.1f} M'
        elif number >= 1000:
            return f'{number//1000:.2f} K'
        else:
            return number
    except (ValueError, TypeError):
        return number
