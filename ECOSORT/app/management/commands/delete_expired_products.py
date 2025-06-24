# myapp/management/commands/delete_expired_products.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from app.models import Package

class Command(BaseCommand):
    help = 'Deletes expired products from the database'

    def handle(self, *args, **kwargs):
        current_time = timezone.now()
        expired_products = Package.objects.filter(expiry_date__lt=current_time)
        count = expired_products.count()
        expired_products.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} expired products.'))