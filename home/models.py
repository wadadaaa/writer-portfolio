from datetime import date

from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django import forms

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, \
    InlinePanel, PageChooserPanel, StreamFieldPanel

from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from wagtail.wagtailsearch import index

from wagtail.wagtailcore.blocks import TextBlock, StructBlock, StreamBlock, FieldBlock, CharBlock, RichTextBlock, RawHTMLBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock


from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase


class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('left', 'Wrap left'), ('right', 'Wrap right'), ('mid', 'Mid width'), ('full', 'Full width'),
    ))


class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = RichTextBlock()
    alignment = ImageFormatChoiceBlock()


# A couple of abstract classes that contain commonly used fields

class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document'),
    ]

    class Meta:
        abstract = True


# Intro items

class IntroItem(LinkFields):
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    label = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    hero = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    intro_h1 = models.CharField(max_length=255, blank=True)
    intro_h2 = models.CharField(max_length=255, blank=True)

    panels = [
        ImageChooserPanel('logo'),
        ImageChooserPanel('label'),
        ImageChooserPanel('hero'),
        FieldPanel('intro_h1'),
        FieldPanel('intro_h2'),
    ]

    class Meta:
        abstract = True


# Skills items

class SkillItem(LinkFields):
    skill_name = models.CharField(max_length=255, blank=True)
    percent = models.PositiveSmallIntegerField(blank=True)

    panels = [
        FieldPanel('skill_name'),
        FieldPanel('percent'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    def __unicode__(self):
        return self.skill_name


# Video items

class VideoItem(LinkFields):
    embed_url = models.URLField("Embed URL", blank=True)
    caption = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel('embed_url'),
        FieldPanel('caption'),
        FieldPanel('description'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


# Related links

class RelatedLink(LinkFields):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


# Product item

class AboutItem(models.Model):
    photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    header = models.CharField(max_length=255, blank=True)
    about_h1 = models.CharField(max_length=255, blank=True)
    description = RichTextField()
    skills = models.ForeignKey(SkillItem)

    panels = [
        ImageChooserPanel('photo'),
        FieldPanel('header'),
        FieldPanel('description'),
        FieldPanel('about_h1'),
        FieldPanel('description'),
        FieldPanel('skills'),
    ]

    def __unicode__(self):
        return self.header


# Service item

class ServiceItem(models.Model):
    header = models.CharField(max_length=255, blank=True)
    icon = models.CharField(max_length=255, blank=True)
    service_h1 = models.CharField(max_length=255, blank=True)
    service_h2 = models.CharField(max_length=255, blank=True)
    description = RichTextField()

    panels = [
        FieldPanel('header'),
        FieldPanel('icon'),
        FieldPanel('service_h1'),
        FieldPanel('service_h2'),
        FieldPanel('description'),
    ]

    def __unicode__(self):
        return self.service_h1


# Testimonials item

class TestimonialItem(models.Model):
    avatar = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    header = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=255, blank=True)
    general_description = RichTextField()
    testimonial = RichTextField()
    fb = models.URLField("Embed video URL", blank=True)

    panels = [
        ImageChooserPanel('avatar'),
        FieldPanel('position'),
        FieldPanel('name'),
        FieldPanel('testimonial'),
        FieldPanel('fb'),
    ]

    def __unicode__(self):
        return self.name


# Work items

class WorkItem(models.Model):
    project_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    header = models.CharField(max_length=255, blank=True)
    general_description = RichTextField()
    description = RichTextField()
    tag = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    link = models.URLField("work URL", blank=True)

    panels = [
        ImageChooserPanel('project_image'),
        FieldPanel('header'),
        FieldPanel('general_description'),
        FieldPanel('description'),
        FieldPanel('tag'),
        FieldPanel('name'),
        FieldPanel('link'),
    ]

    def __unicode__(self):
        return self.name


# Clients items

class ClientItem(models.Model):
    client_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    name = models.CharField(max_length=255, blank=True)
    link = models.URLField("Client URL", blank=True)

    panels = [
        ImageChooserPanel('client_logo'),
        FieldPanel('name'),
        FieldPanel('link'),
    ]

    def __unicode__(self):
        return self.name


# Home Page

class HomePageIntroItem(Orderable, IntroItem):
    page = ParentalKey('home.HomePage', related_name='intro_items')


class HomePageVideoItem(Orderable, VideoItem):
    page = ParentalKey('home.HomePage', related_name='video_items')


class HomePageSkillItem(Orderable, SkillItem):
    page = ParentalKey('home.HomePage', related_name='skill_items')


class HomePageAboutItem(Orderable, AboutItem):
    page = ParentalKey('home.HomePage', related_name='about_items')


class HomePageServiceItem(Orderable, ServiceItem):
    page = ParentalKey('home.HomePage', related_name='service_items')


class HomePageTestimonialItem(Orderable, TestimonialItem):
    page = ParentalKey('home.HomePage', related_name='testimonial_items')


class HomePageWorkItem(Orderable, WorkItem):
    page = ParentalKey('home.HomePage', related_name='work_items')


class HomePageClientItem(Orderable, ClientItem):
    page = ParentalKey('home.HomePage', related_name='client_items')


class HomePageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('home.HomePage', related_name='related_links')


class HomePage(Page):

    class Meta:
        verbose_name = "Homepage"

HomePage.content_panels = [
    InlinePanel('intro_items', label="Intro items"),
    InlinePanel('skill_items', label="Skill items"),
    InlinePanel('about_items', label="About items"),
    InlinePanel('service_items', label="Service items"),
    InlinePanel('work_items', label="Work items"),
    InlinePanel('testimonial_items', label="Testimonial items"),
    InlinePanel('client_items', label="Client items"),
    InlinePanel('related_links', label="Related links"),
    InlinePanel('video_items', label="Video items"),

]

HomePage.promote_panels = Page.promote_panels



