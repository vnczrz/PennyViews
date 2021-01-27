from django import template

register = template.Library()

@register.filter
def usd(value):
    if value in ['None', 'N/A']:
        return value
    else:
        v = float(value)
        return "${:,.2f}".format(v)

@register.filter
def human_format(num):
    if num in ['None', 'N/A']:
        return num
    else:
        num = float(num)
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        # add more suffixes if you need them
        return '%.2f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])