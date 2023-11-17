from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField
from django.urls import reverse
from PIL import Image
import uuid

User = get_user_model()

class Type(models.Model):
    name_en = models.CharField(_('name in English language'), max_length=100)
    name_lt = models.CharField(_('name in Lithuanian language'),max_length=100)
    description_en = models.TextField(_('description in English language'), max_length=1000, blank=True)
    description_lt = models.TextField(_('description in English language'), max_length=1000, blank=True)
    
    class Meta:
        verbose_name = _("type")
        verbose_name_plural = _("types")

    def __str__(self):
        return self.name_en

    def get_absolute_url(self):
        return reverse("type_detail", kwargs={"pk": self.pk})
    

class PlantTime(models.Model):
    month_en = models.IntegerField(
        choices=[
            (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'),
            (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'),
            (11, 'November'), (12, 'December'),
        ]
    )
    month_lt = models.IntegerField(
        choices=[
            (1, 'Sausis'), (2, 'Vasaris'), (3, 'Kovas'), (4, 'Balandis'), (5, 'Gegužė'),
            (6, 'Birželis'), (7, 'Liepa'), (8, 'Rugpjūtis'), (9, 'Rugsėjis'), (10, 'Spalis'),
            (11, 'Lapkritis'), (12, 'Gruodis'),
        ]
    )
    first_day = models.IntegerField(
        choices=[
            (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'),
            (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'),
            (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'),
            (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'),
            (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30'), (31, '31'),
        ])
    last_day = models.IntegerField(
        choices=[
            (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'),
            (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'),
            (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'),
            (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'),
            (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30'), (31, '31'),
        ])
    
    class Meta:
        verbose_name = _("plantTime")
        verbose_name_plural = _("plantTimes")

    def __str__(self):
        return f'{self.get_month_en_display()} ({self.get_month_lt_display()})'

    def get_absolute_url(self):
        return reverse("plantingday_detail", kwargs={"pk": self.pk})
    

class Color(models.Model):
    name_en = models.CharField(_("name in English language"),max_length=100)
    name_lt = models.CharField(_("name in Lithuanian language"),max_length=100)
    description_en = models.TextField(_("description in English language"), max_length=1000, blank=True)
    description_lt = models.TextField(_("description in Lithuanian language"), max_length=1000, blank=True)
    
    class Meta:
        verbose_name = _("color")
        verbose_name_plural = _("colors")

    def __str__(self):
        return self.name_en

    def get_absolute_url(self):
        return reverse("color_detail", kwargs={"pk": self.pk})
        

class Plant(models.Model):
    name_en = models.CharField(max_length=100)
    name_lt = models.CharField(max_length=100)
    description_en = models.TextField(max_length=1000, blank=True)
    description_lt = models.TextField(max_length=1000, blank=True)
    size = models
    type = models.ForeignKey(
        Type,
        verbose_name=_("type"),
        on_delete=models.CASCADE, 
        related_name=_("plants"),)
    colors = models.ManyToManyField(
        Color,
        verbose_name=_("color"), 
        related_name=_("plants"),
        )
    planting_time = models.ForeignKey(
        PlantTime, 
        verbose_name=_("planting time"),
        on_delete=models.CASCADE,
        related_name=_("plants"))
    
    class Meta:
        verbose_name = _("plant")
        verbose_name_plural = _("plants")

    def __str__(self):
        return self.name_en

    def get_absolute_url(self):
        return reverse("plant_detail", kwargs={"pk": self.pk})
    
#zemiau modelio dalis kuria manipuliuoja vartotojas virsuje
# modelio dalis kiri tvarkoma administratoriaus.

class Project(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name=_("projects"),
    )
    project_name = models.CharField(_("project name"), max_length=100)
    public = models.BooleanField(_("public"), default=False)
    description = HTMLField(_("enter description"), max_length=10000, default='', blank=True)

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")

    def __str__(self):
        return self.project_name

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"pk": self.pk})
    

class Zone(models.Model):
    name = models.CharField(_("name in Lithuanian language"), 
        max_length=50, blank=True
    )
    lenght = models.FloatField(_("enter lenght"))
    width = models.FloatField(_("enter width"))
    public = models.BooleanField(_("public"), default=False)
    project = models.ForeignKey(
        Project,
        verbose_name=_("garden project"),
        on_delete=models.CASCADE,
        related_name=_("zones"),
    )
    description = HTMLField(_("enter description"), max_length=10000, default='', blank=True)   
    
    class Meta:
        verbose_name = _("zone")
        verbose_name_plural = _("zones")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("zone_detail", kwargs={"pk": self.pk})


class ZonePlant(models.Model):
    blooming_period = models.CharField(_("enter blooming period"),
        max_length=100, 
        blank=True
    )
    qty = models.IntegerField(_('enter quantity'))
    price = models.FloatField(_('enter plants price of unit'),)
    zone = models.ForeignKey(
        Zone,
        verbose_name=_("zone"),
        on_delete=models.CASCADE,
        related_name=_("zone_plants")
        )
    plant = models.ForeignKey(
        Plant, 
        verbose_name=_("plant"),
        on_delete=models.CASCADE,
        related_name=_("zone_plants"))
    color = models.ForeignKey(
        Color,
        verbose_name=_("color"), 
        on_delete=models.CASCADE,
        related_name=_("zone_plants"))

    class Meta:
        verbose_name = _("zone plant")
        verbose_name_plural = _("zone plants")

    def __str__(self):
        return self.plant.name_en

    def get_absolute_url(self):
        return reverse("zoneplant_detail", kwargs={"pk": self.pk}) 
    

class Photo(models.Model):
    image = models.ImageField(_("add image"), upload_to='photos/',
        null=True, 
        blank=True
    )
    season = models.CharField(_("select season"), max_length=100, 
        choices=[
            ("SPRING", "SPRING"), 
            ("SUMMER", "SUMMER"), 
            ("AUTUMN", "AUTUMN"), 
            ("WINTER", "WINTER"),
        ])
    zone = models.ForeignKey(
        Zone,
        verbose_name=_("zone"),
        on_delete=models.CASCADE,
        related_name=_("photos")
        )
        
    class Meta:
        verbose_name = _("photo")
        verbose_name_plural = _("photos")

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        if self.image:
            image = Image.open(self.image.path)
            if image.height > 300 or image.width > 500:
                resized_dimensions = (500, 300)
                image.thumbnail(resized_dimensions)
                image.save(self.image.path)

    def __str__(self):
        return f"{self.image.url}"
    
    def get_absolute_url(self):
        if self.image:
            return reverse("zone_detail", kwargs={"pk": self.pk})
        else:
            return reverse("default_url")
    
