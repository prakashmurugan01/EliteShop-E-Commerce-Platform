from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Product

class Command(BaseCommand):
    help = "Normalize product slugs to URL-safe values"

    def handle(self, *args, **options):
        updated = 0
        for p in Product.objects.all():
            new_slug = slugify(p.name)
            slug = new_slug
            n = 1
            while Product.objects.filter(slug=slug).exclude(pk=p.pk).exists():
                slug = f"{new_slug}-{n}"
                n += 1
            if p.slug != slug:
                p.slug = slug
                p.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS(f"UPDATED {p.pk} -> {slug}"))
        if not updated:
            self.stdout.write(self.style.WARNING('No slugs needed updating'))
        else:
            self.stdout.write(self.style.SUCCESS(f"Total updated: {updated}"))
