from datetime import datetime, timedelta
from django.db import models
from django.utils.timesince import timesince
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.db.models import Sum
from django.template.defaultfilters import slugify
from common.models import User


class Tag(models.Model):
    name = models.CharField(max_length=500)
    color = models.CharField(max_length=20,
                             default="#999999", verbose_name=_("color"))
    created_by = models.ForeignKey(User,
                                   related_name="marketing_tags",
                                   null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)

    @property
    def created_by_user(self):
        return self.created_by if self.created_by else None


class EmailTemplate(models.Model):
    created_by = models.ForeignKey(
        User, related_name="marketing_emailtemplates",
        null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=5000)
    subject = models.CharField(max_length=5000)
    html = models.TextField()

    @property
    def created_by_user(self):
        return self.created_by if self.created_by else None


class ContactList(models.Model):
    created_by = models.ForeignKey(
        User, related_name="marketing_contactlist",
        null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=500)
    tags = models.ManyToManyField(Tag)
    # is_public = models.BooleanField(default=False)
    visible_to = models.ManyToManyField(
        User, related_name="contact_lists_visible_to")

    @property
    def created_by_user(self):
        return self.created_by if self.created_by else None

    @property
    def created_on_format(self):
        return self.created_on.strftime('%b %d, %Y %I:%M %p')

    @property
    def created_on_since(self):
        now = datetime.now()
        difference = now.replace(tzinfo=None) - \
            self.created_on.replace(tzinfo=None)

        if difference <= timedelta(minutes=1):
            return 'just now'
        return '%(time)s ago' % {
            'time': timesince(self.created_on).split(', ')[0]}

    @property
    def tags_data(self):
        return self.tags.all()

    @property
    def no_of_contacts(self):
        return self.contacts.all().count()

    @property
    def no_of_campaigns(self):
        return self.campaigns.all().count()

    @property
    def unsubscribe_contacts(self):
        return self.contacts.filter(is_unsubscribed=True).count()

    @property
    def bounced_contacts(self):
        return self.contacts.filter(is_bounced=True).count()

    @property
    def no_of_clicks(self):
        clicks = CampaignLog.objects.filter(
            contact__contact_list__in=[self]).aggregate(Sum(
                'no_of_clicks'))['no_of_clicks__sum']
        return clicks


class Contact(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. \
        Up to 20 digits allowed."
    )
    created_by = models.ForeignKey(
        User, related_name="marketing_contacts_created_by",
        null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    contact_list = models.ManyToManyField(ContactList, related_name="contacts")
    name = models.CharField(max_length=500)
    email = models.EmailField()
    contact_number = models.CharField(
        validators=[phone_regex], max_length=20, blank=True, null=True)
    is_unsubscribed = models.BooleanField(default=False)
    is_bounced = models.BooleanField(default=False)
    company_name = models.CharField(max_length=500, null=True, blank=True)
    last_name = models.CharField(max_length=500, null=True, blank=True)
    city = models.CharField(max_length=500, null=True, blank=True)
    state = models.CharField(max_length=500, null=True, blank=True)
    contry = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.email


class FailedContact(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'.\
        Up to 20 digits allowed."
    )
    created_by = models.ForeignKey(
        User, related_name="marketing_failed_contacts_created_by", null=True,
        on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    contact_list = models.ManyToManyField(
        ContactList, related_name="failed_contacts")
    name = models.CharField(max_length=500, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    contact_number = models.CharField(
        validators=[phone_regex], max_length=20, blank=True, null=True)
    company_name = models.CharField(max_length=500, null=True, blank=True)
    last_name = models.CharField(max_length=500, null=True, blank=True)
    city = models.CharField(max_length=500, null=True, blank=True)
    state = models.CharField(max_length=500, null=True, blank=True)
    contry = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.email


class Campaign(models.Model):
    STATUS_CHOICES = (
        ('Scheduled', 'Scheduled'),
        ('Cancelled', 'Cancelled'),
        ('Sending', 'Sending'),
        ('Preparing', 'Preparing'),
        ('Sent', 'Sent'),
    )

    title = models.CharField(max_length=5000)
    created_by = models.ForeignKey(
        User, related_name="marketing_campaigns_created_by",
        null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    contact_lists = models.ManyToManyField(
        ContactList, related_name="campaigns")
    email_template = models.ForeignKey(
        EmailTemplate, blank=True, null=True, on_delete=models.SET_NULL)
    schedule_date_time = models.DateTimeField(blank=True, null=True)
    reply_to_email = models.EmailField(blank=True, null=True)
    subject = models.CharField(max_length=5000)
    html = models.TextField()
    html_processed = models.TextField(default="", blank=True)
    from_email = models.EmailField(blank=True, null=True)
    from_name = models.EmailField(blank=True, null=True)
    sent = models.IntegerField(default='0', blank=True)
    opens = models.IntegerField(default='0', blank=True)
    opens_unique = models.IntegerField(default='0', blank=True)
    bounced = models.IntegerField(default='0')
    status = models.CharField(
        default="Preparing", choices=STATUS_CHOICES, max_length=20)

    @property
    def no_of_unsubscribers(self):
        unsubscribers = self.campaign_contacts.filter(
            contact__is_unsubscribed=True).count()
        return unsubscribers

    @property
    def no_of_bounces(self):
        bounces = self.campaign_contacts.filter(
            contact__is_bounced=True).count()
        return bounces

    @property
    def no_of_clicks(self):
        clicks = self.marketing_links.aggregate(Sum('clicks'))['clicks__sum']
        return clicks

    @property
    def no_of_sent_emails(self):
        contacts = self.campaign_contacts.count()
        return contacts

    @property
    def created_on_format(self):
        return self.created_on.strftime('%b %d, %Y %I:%M %p')


class Link(models.Model):
    campaign = models.ForeignKey(
        Campaign, related_name="marketing_links", on_delete=models.CASCADE)
    original = models.URLField(max_length=2100)
    clicks = models.IntegerField(default='0')
    unique = models.IntegerField(default='0')


class CampaignLog(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    campaign = models.ForeignKey(
        Campaign, related_name='campaign_contacts', on_delete=models.CASCADE)
    contact = models.ForeignKey(
        Contact, related_name="marketing_campaign_logs",
        null=True, on_delete=models.SET_NULL)
    message_id = models.CharField(max_length=1000, null=True, blank=True)


class CampaignLinkClick(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    link = models.ForeignKey(
        Link, blank=True, null=True, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    created_on = models.DateTimeField(auto_now_add=True)
    user_agent = models.CharField(max_length=2000, blank=True, null=True)
    contact = models.ForeignKey(
        Contact, blank=True, null=True, on_delete=models.CASCADE)


class CampaignOpen(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    created_on = models.DateTimeField(auto_now_add=True)
    user_agent = models.CharField(max_length=2000, blank=True, null=True)
    contact = models.ForeignKey(
        Contact, blank=True, null=True, on_delete=models.CASCADE)
