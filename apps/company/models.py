from django.db import models
from django.utils import timezone
from datetime import time

# --------------------------------------------
# Константа дней недели
# --------------------------------------------
WEEKDAYS = [
    (0, "Ponedelok"),
    (1, "Utorok"),
    (2, "Streda"),
    (3, "Četvrtok"),
    (4, "Piatok"),
    (5, "Sobota"),
    (6, "Nedeľa"),
]


# --------------------------------------------
# Основная информация о компании
# --------------------------------------------
class CompanyInfo(models.Model):
    name = models.CharField(max_length=255)
    ico = models.CharField("IČO", max_length=20, blank=True)
    dic = models.CharField("DIČ", max_length=20, blank=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    facebook_url = models.URLField(blank=True, null=True, default="facebook.com")
    instagram_url = models.URLField(blank=True, null=True, default="instagram.com")
    linkedin_url = models.URLField(blank=True, null=True, default="linkedin.com")
    x_url = models.URLField(blank=True, null=True, default="x.com")
    tiktok_url = models.URLField(blank=True, null=True, default="tiktok.com")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "csm_companyinfo"  # сохраняем связь с существующей таблицей
        verbose_name = "Informácie o firme"
        verbose_name_plural = "Informácie o firme"

    def __str__(self):
        return self.name


# --------------------------------------------
# Настройки подвала (footer)
# --------------------------------------------
class FooterInfo(models.Model):
    company = models.OneToOneField(
        "CompanyInfo",
        on_delete=models.CASCADE,
        related_name="footer_info",
        verbose_name="Company",
    )

    about_title = models.CharField(max_length=100, default="Agentúra Závodský")
    about_description = models.TextField()

    # Поля, которые могут переопределять данные компании
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    contact_address = models.CharField(max_length=255, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "csm_footerinfo"
        verbose_name = "footer settings"
        verbose_name_plural = "footer settings"

    def __str__(self):
        return f"Footer: {self.company.name}"


# --------------------------------------------
# Еженедельное расписание работы
# --------------------------------------------
class OpeningHour(models.Model):
    company = models.ForeignKey(
        "CompanyInfo",
        on_delete=models.CASCADE,
        related_name="opening_hours",
    )
    weekday = models.IntegerField(choices=WEEKDAYS)
    is_closed = models.BooleanField(default=False, help_text="Zakázané v tento deň")
    if is_closed:
        start_time = models.TimeField(null=True, blank=True)
        end_time = models.TimeField(null=True, blank=True)
    else:
        start_time = models.TimeField()
        end_time = models.TimeField()

    class Meta:
        db_table = "csm_openinghour"
        ordering = ("weekday", "start_time", "id")
        verbose_name = "Интервал работы"
        verbose_name_plural = "График по дням"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "weekday", "start_time", "end_time"],
                name="uniq_opening_hour",
            ),
        ]

    def __str__(self):
        return f"{self.get_weekday_display()} {self.start_time}–{self.end_time}"


# --------------------------------------------
# Исключения (праздники, сокращённые дни)
# --------------------------------------------
class SpecialOpening(models.Model):
    company = models.ForeignKey(
        "CompanyInfo",
        on_delete=models.CASCADE,
        related_name="special_openings",
    )
    date = models.DateField(help_text="Konkrétny dátum výnimky")
    is_closed = models.BooleanField(default=False, help_text="Zakázané v tento deň")
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "csm_specialopening"
        ordering = ("date", "start_time", "id")
        verbose_name = "Исключение (праздник/особый день)"
        verbose_name_plural = "Исключения по датам"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "date", "start_time", "end_time", "is_closed"],
                name="uniq_special_opening",
            ),
        ]

    def __str__(self):
        if self.is_closed:
            return f"{self.date} — закрыто"
        return f"{self.date} {self.start_time or '??'}–{self.end_time or '??'}"

    def clean(self):
        from django.core.exceptions import ValidationError

        if not self.is_closed and (not self.start_time or not self.end_time):
            raise ValidationError("Укажите время начала и конца или отметьте «закрыто».")


# --------------------------------------------
# Утилиты для проверки статуса компании
# --------------------------------------------
def _now_local():
    """Возвращает текущее локальное время с учётом TIME_ZONE."""
    return timezone.localtime()


def _is_time_in_any_interval(t: time, intervals: list[tuple[time, time]]) -> bool:
    """Проверяет, попадает ли время в один из интервалов (строго < end)."""
    return any(start <= t < end for start, end in intervals)


def _weekday_intervals(company, weekday: int) -> list[tuple[time, time]]:
    """Возвращает список интервалов для данного дня недели."""
    return [
        (oh.start_time, oh.end_time)
        for oh in company.opening_hours.filter(weekday=weekday)
    ]


def _special_for_today(company, today):
    """Возвращает все спец-интервалы (исключения) на конкретную дату."""
    return list(
        company.special_openings.filter(date=today).order_by("start_time")
    )


def company_is_open_now(company) -> bool:
    """Основная логика: определяет, открыта ли компания в текущий момент."""
    now = _now_local()
    today = now.date()
    t = now.time()

    # Сначала проверяем спец-расписание (праздники, исключения)
    specials = _special_for_today(company, today)
    if specials:
        # Если хоть одно исключение помечено как закрыто — весь день закрыт
        if any(s.is_closed for s in specials):
            return False

        # Иначе проверяем интервалы для исключений
        intervals = [
            (s.start_time, s.end_time)
            for s in specials
            if s.start_time and s.end_time
        ]
        return _is_time_in_any_interval(t, intervals)

    # Если спец-дней нет — проверяем обычное расписание
    intervals = _weekday_intervals(company, now.weekday())
    return _is_time_in_any_interval(t, intervals)


def company_status_text(company) -> str:
    """Возвращает удобный текстовый статус."""
    return "Открыто" if company_is_open_now(company) else "Закрыто"


# Добавляем свойства прямо на модель CompanyInfo
CompanyInfo.is_open_now = property(lambda self: company_is_open_now(self))
CompanyInfo.open_status_text = property(lambda self: company_status_text(self))


class AboutUsPage(models.Model):
    """this models will be used to store About Us page content and Company working hours including special opening hours for holidays or events."""
    company = models.OneToOneField(
        "CompanyInfo",
        on_delete=models.CASCADE,
        related_name="about_us_page",
        verbose_name="Компания",
    )
    content = models.TextField()

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "csm_aboutuspage"
        verbose_name = "Страница 'О нас'"
        verbose_name_plural = "Страницы 'О нас'"

    def __str__(self):
        return f"About Us: {self.company.name}"



