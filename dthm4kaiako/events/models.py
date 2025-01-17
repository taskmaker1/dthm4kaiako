"""Models for resources application."""


from django.db import models
from django.contrib.gis.db import models as geomodels
from django.urls import reverse
from utils.get_upload_filepath import (
    get_event_organiser_upload_path,
    get_event_sponsor_upload_path,
    get_event_series_upload_path,
)
from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _


class Location(models.Model):
    """Model for a physical location."""

    room = models.CharField(
        max_length=200,
        blank=True,
        help_text='Name of room or space, for example: Room 134',
    )
    name = models.CharField(
        max_length=200,
        help_text='Name of location, for example: Middleton Grange School'
    )
    street_address = models.CharField(
        max_length=200,
        blank=True,
        help_text='Street address location, for example: 12 High Street'
    )
    suburb = models.CharField(
        max_length=200,
        blank=True,
        help_text='Suburb, for example: Riccarton'
    )
    city = models.CharField(
        max_length=200,
        help_text='Town or city, for example: Christchurch',
        default='Christchurch',
    )
    REGION_NORTHLAND = 1
    REGION_AUCKLAND = 2
    REGION_WAIKATO = 3
    REGION_BAY_OF_PLENTY = 4
    REGION_GISBORNE = 5
    REGION_HAWKES_BAY = 6
    REGION_TARANAKI = 7
    REGION_MANAWATU_WANGANUI = 8
    REGION_WELLINGTON = 9
    REGION_TASMAN = 10
    REGION_NELSON = 11
    REGION_MARLBOROUGH = 12
    REGION_WEST_COAST = 13
    REGION_CANTERBURY = 14
    REGION_OTAGO = 15
    REGION_SOUTHLAND = 16
    REGION_CHATHAM_ISLANDS = 17
    REGION_CHOICES = (
        (REGION_NORTHLAND, _('Northland')),
        (REGION_AUCKLAND, _('Auckland')),
        (REGION_WAIKATO, _('Waikato')),
        (REGION_BAY_OF_PLENTY, _('Bay of Plenty')),
        (REGION_GISBORNE, _('Gisborne')),
        (REGION_HAWKES_BAY, _("Hawke's Bay")),
        (REGION_TARANAKI, _('Taranaki')),
        (REGION_MANAWATU_WANGANUI, _('Manawatu-Wanganui')),
        (REGION_WELLINGTON, _('Wellington')),
        (REGION_TASMAN, _('Tasman')),
        (REGION_NELSON, _('Nelson')),
        (REGION_MARLBOROUGH, _('Marlborough')),
        (REGION_WEST_COAST, _('West Coast')),
        (REGION_CANTERBURY, _('Canterbury')),
        (REGION_OTAGO, _('Otago')),
        (REGION_SOUTHLAND, _('Southland')),
        (REGION_CHATHAM_ISLANDS, _('Chatman Islands')),
    )
    region = models.PositiveSmallIntegerField(
        choices=REGION_CHOICES,
        default=REGION_CANTERBURY,
    )
    description = RichTextUploadingField(blank=True)
    coords = geomodels.PointField()

    def __str__(self):
        """Text representation of a location."""
        return self.name

    def get_full_address(self):
        """Get full text representation of a location."""
        address = ''
        if self.room:
            address += self.room + ',\n'
        address += self.name + ',\n'
        if self.street_address:
            address += self.street_address + ',\n'
        if self.suburb:
            address += self.suburb + ', '
        address += self.city + ',\n'
        address += self.get_region_display()
        return address

    class Meta:
        """Meta options for class."""

        ordering = ['name', ]


class Organiser(models.Model):
    """Model for an event organiser."""

    name = models.CharField(max_length=100)
    url = models.URLField(blank=True)
    logo = models.ImageField(
        null=True,
        blank=True,
        upload_to=get_event_organiser_upload_path,
        help_text="Logo will be displayed instead of name if provided."
    )

    def __str__(self):
        """Text representation of an event organiser."""
        return self.name

    class Meta:
        """Meta options for class."""

        ordering = ['name', ]


class Sponsor(models.Model):
    """Model for an event sponsor."""

    name = models.CharField(max_length=100)
    url = models.URLField(blank=True)
    logo = models.ImageField(
        null=True,
        blank=True,
        upload_to=get_event_sponsor_upload_path,
        help_text="Logo will be displayed instead of name if provided."
    )

    def __str__(self):
        """Text representation of an sponsor."""
        return self.name

    class Meta:
        """Meta options for class."""

        ordering = ['name', ]


class Series(models.Model):
    """Model for an event series."""

    name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=30)
    description = RichTextUploadingField()
    logo = models.ImageField(
        null=True,
        blank=True,
        upload_to=get_event_series_upload_path,
        help_text="Logo will be displayed instead of name if provided."
    )

    def __str__(self):
        """Text representation of an event series."""
        return self.name

    class Meta:
        """Meta options for class."""

        verbose_name_plural = "series"


class Event(models.Model):
    """Model for an event."""

    name = models.CharField(max_length=200)
    description = RichTextUploadingField()
    slug = AutoSlugField(populate_from='get_short_name', always_update=True, null=True)
    registration_link = models.URLField(blank=True)
    # TODO: Only allow publishing if start and end are not null
    published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    accessible_online = models.BooleanField(
        default=False,
        help_text='Select if this event be attended online'
    )
    price = models.PositiveSmallIntegerField(default=0)
    locations = models.ManyToManyField(
        Location,
        related_name='events',
        blank=True,
    )
    sponsors = models.ManyToManyField(
        Sponsor,
        related_name='events',
        blank=True,
    )
    organisers = models.ManyToManyField(
        Organiser,
        related_name='events',
        blank=True,
    )
    series = models.ForeignKey(
        Series,
        on_delete=models.CASCADE,
        related_name='events',
        null=True,
        blank=True,
    )
    # TODO: Add validation that if no locations, then accessible_online must be true

    def update_datetimes(self):
        """Update datetimes of event."""
        self.start = self.sessions.order_by('start').first().start
        self.end = self.sessions.order_by('-end').first().end
        self.save()

    def get_absolute_url(self):
        """Return URL of event on website.

        Returns:
            URL as a string.
        """
        return reverse('events:event', kwargs={'pk': self.pk, 'slug': self.slug})

    def get_short_name(self):
        """Event name with series abbreviation if available.

        Returns:
            String of short event name.
        """
        if self.series:
            return '{}: {}'.format(self.series.abbreviation, self.name)
        else:
            return self.name

    def __str__(self):
        """Text representation of an event."""
        return self.name

    class Meta:
        """Meta options for class."""

        ordering = ['start', 'end']


class Session(models.Model):
    """Model for an event session."""

    name = models.CharField(max_length=200)
    description = RichTextUploadingField(blank=True)
    url = models.URLField(blank=True)
    url_label = models.CharField(max_length=200, blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='sessions',
    )
    locations = models.ManyToManyField(
        Location,
        related_name='sessions',
        blank=True,
    )

    def __str__(self):
        """Text representation of an session."""
        return self.name

    class Meta:
        """Meta options for class."""

        ordering = ['start', 'end']
