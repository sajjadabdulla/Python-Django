import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from store.models import Region, Attraction


class Command(BaseCommand):
    help = "Seed database with 100 sample tourist attractions"


    def handle(self, *args, **options):
        region_data = {
        "Paris": "https://flagcdn.com/w320/fr.png",
        "Rome": "https://flagcdn.com/w320/it.png",
        "Barcelona": "https://flagcdn.com/w320/es.png",
        "London": "https://flagcdn.com/w320/gb.png",
        "New York": "https://flagcdn.com/w320/us.png",
        "Mumbai": "https://flagcdn.com/w320/in.png",
        "Goa": "https://flagcdn.com/w320/in.png",
        "Jaipur": "https://flagcdn.com/w320/in.png",
        "Kyoto": "https://flagcdn.com/w320/jp.png",
        "Bangkok": "https://flagcdn.com/w320/th.png",
        "Istanbul": "https://flagcdn.com/w320/tr.png",
        "Sydney": "https://flagcdn.com/w320/au.png",
    }

        regions = []
        for name, flag in region_data.items():
            r, _ = Region.objects.get_or_create(
                name=name,
                slug=slugify(name),
                defaults={"flag_url": flag},
            )
            regions.append(r)

        categories = ["Historical", "Beach", "Museum", "Park", "Temple", "Mountain", "Market", "Waterfall"]


        for i in range(1, 101):
            region = random.choice(regions)
            cat = random.choice(categories)
            name = f"{random.choice(['Old','New','Grand','Royal','Hidden','Sunset','Emerald'])} {random.choice(['Fort','Palace','Garden','Museum','Beach','Lookout','Market','Temple'])} of {region.name}"
            slug = f"{slugify(name)}-{i}"
            price = Decimal(random.randint(0, 2500))


            image_url = f"https://picsum.photos/seed/attraction{i}/1000/600"
            opening = random.choice([
            "09:00 - 18:00", "08:00 - 20:00", "10:00 - 17:00", "24 hours", "Sunrise - Sunset"
            ])
            lat = round(random.uniform(-35.0, 55.0), 6)
            lon = round(random.uniform(-180.0, 180.0), 6)


            Attraction.objects.create(
                name=name,
                slug=slug,
                region=region,
                category=cat,
                description=f"{name} is a popular {cat.lower()} in {region.name}. Great for visitors and photo-ops.",
                ticket_price=price,
                image_url=image_url,
                latitude=lat,
                longitude=lon,
                opening_hours=opening,
                available=True
            )


        self.stdout.write(self.style.SUCCESS("✅ Seeded 100 tourist attractions"))