from django import template
from ..models import WEEKDAYS


register = template.Library()

@register.inclusion_tag("csm/index.html", takes_context=True)
def company_opening_hours(context, company):
    # группируем интервалы по дням недели
    day_map = {w[0]: {"label": w[1], "intervals": []} for w in WEEKDAYS}
    for oh in company.opening_hours.all().order_by("weekday", "start_time"):
        day_map[oh.weekday]["intervals"].append((oh.start_time, oh.end_time))
    return {"days": [day_map[i] for i, _ in enumerate(WEEKDAYS)], "company": company}
