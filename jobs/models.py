from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    name = models.CharField(
        verbose_name=_('name'),
        max_length=50,
        unique=True,
    )
    part_code = models.CharField(
        verbose_name=_('part code'),
        help_text=_('Maximum 3 characters. Client part code must be unique.'),
        max_length=3,
        unique=True,
    )

    @property
    def num_sites(self):
        return self.sites.count()
    num_sites.fget.short_description = 'number of sites'

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('client')
        verbose_name_plural = _('clients')
        ordering = ['name']
        constraints = [
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_name_not_blank',
                check=~models.Q(name='')
            ),
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_part_code_not_blank',
                check=~models.Q(part_code='')
            ),
        ]


class Region(models.TextChoices):
    """
    Used as choices for Development Site Region.
    Housebuild clients operate under regional divisions.
    A particular site will be managed by one division.
    """
    BRI = 'BRI', _('Bristol')
    NA = 'NA', _('Not Applicable')
    NR = 'NR', _('Non-Regional')
    SW = 'SW', _('South West')
    TV = 'TV', _('Thames Valley')
    W = 'W', _('Western')


class DevelopmentSite(models.Model):
    client = models.ForeignKey(
        verbose_name=_('client'),
        to=Client,
        on_delete=models.CASCADE,
        related_name='sites',
    )
    name = models.CharField(
        verbose_name=_('name'),
        max_length=100,
    )
    part_code = models.CharField(
        verbose_name=_('part code'),
        help_text=_('Maximum 3 characters. Site part code does not need to be unique.'),
        max_length=3,
    )
    region = models.CharField(
        verbose_name=_('region'),
        help_text=_('Regional division'),
        max_length=3,
        choices=Region.choices,
        default=Region.SW,
    )

    @property
    def full_code(self):
        return f'{self.client.part_code}{self.region}{self.part_code}'
    full_code.fget.short_description = 'full code'

    @property
    def num_jobs(self):
        return self.jobs.count()
    num_jobs.fget.short_description = 'number of jobs'

    def __str__(self):
        return f'{self.client.part_code} {self.name}'
    
    class Meta:
        verbose_name = _('development site')
        verbose_name_plural = _('development sites')
        ordering = ['client', 'name',]
        constraints = [
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_name_not_blank',
                check=~models.Q(name='')
            ),
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_part_code_not_blank',
                check=~models.Q(part_code='')
            ),
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_region_not_blank',
                check=~models.Q(region='')
            ),
        ]


class Tenure(models.TextChoices):
    """
    Property ownership type.
    """
    P = 'Private', _('Private')
    HA = 'HA', _('HA')


class Job(models.Model):
    date_created = models.DateTimeField(
        auto_now_add = True,
    )
    site = models.ForeignKey(
        to=DevelopmentSite,
        verbose_name=_('development site'),
        related_name='jobs',
        on_delete=models.CASCADE,
    )
    tenure = models.CharField(
        verbose_name=_('tenure'),
        max_length=7,
        choices=Tenure.choices,
        default=Tenure.P,
    )
    plot_number = models.CharField(
        verbose_name=_('plot number'),
        max_length=50,
    )
    full_code = models.CharField(
        verbose_name=_('full code'),
        help_text=_('Maximum 20 characters.'),
        max_length=20,
    )

    @property
    def client(self):
        return self.site.client
    client.fget.short_description = 'client'

    def __str__(self):
        if self.tenure == 'Private':
            return f'{self.site.client} {self.site} {self.plot_number}'
        return f'{self.site.client} {self.site} {self.tenure} {self.plot_number}'
    
    class Meta:
        verbose_name = _('job')
        verbose_name_plural = _('jobs')
        ordering = ['site', 'plot_number',]
        constraints = [
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_tenure_not_blank',
                check=~models.Q(tenure='')
            ),
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_plot_number_not_blank',
                check=~models.Q(plot_number='')
            ),
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_full_code_not_blank',
                check=~models.Q(full_code='')
            ),
        ]