import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from report.models import ActionStatus, CrimeReport, PoliceStation


class Command(BaseCommand):
    help = "Seed database with Nepal police stations and crime reports"

    def handle(self, *args, **options):
        self.stdout.write("Clearing existing data...")
        CrimeReport.objects.all().delete()
        PoliceStation.objects.all().delete()

        self.stdout.write("Seeding police stations...")
        stations = self._seed_stations()
        self.stdout.write(self.style.SUCCESS(f"Created {len(stations)} police stations"))

        self.stdout.write("Seeding crime reports...")
        count = self._seed_reports(stations)
        self.stdout.write(self.style.SUCCESS(f"Created {count} crime reports"))

    def _seed_stations(self):
        stations_data = [
            {
                "name": "Kathmandu Metropolitan Police Office",
                "location": "Kathmandu, Bagmati",
                "latitude": 27.7172,
                "longitude": 85.3240,
            },
            {
                "name": "Lalitpur Metropolitan Police Office",
                "location": "Lalitpur, Bagmati",
                "latitude": 27.6644,
                "longitude": 85.3188,
            },
            {
                "name": "Bhaktapur District Police Office",
                "location": "Bhaktapur, Bagmati",
                "latitude": 27.6710,
                "longitude": 85.4298,
            },
            {
                "name": "Pokhara Metropolitan Police Office",
                "location": "Pokhara, Gandaki",
                "latitude": 28.2096,
                "longitude": 83.9856,
            },
            {
                "name": "Biratnagar Metropolitan Police Office",
                "location": "Biratnagar, Province 1",
                "latitude": 26.4525,
                "longitude": 87.2710,
            },
            {
                "name": "Birgunj Metropolitan Police Office",
                "location": "Birgunj, Province 2",
                "latitude": 27.0063,
                "longitude": 84.8809,
            },
            {
                "name": "Butwal Sub-Metropolitan Police Office",
                "location": "Butwal, Lumbini",
                "latitude": 27.7000,
                "longitude": 83.4484,
            },
            {
                "name": "Dharan Sub-Metropolitan Police Office",
                "location": "Dharan, Province 1",
                "latitude": 26.8144,
                "longitude": 87.2791,
            },
            {
                "name": "Hetauda Sub-Metropolitan Police Office",
                "location": "Hetauda, Bagmati",
                "latitude": 27.4287,
                "longitude": 84.9962,
            },
            {
                "name": "Nepalgunj Sub-Metropolitan Police Office",
                "location": "Nepalgunj, Lumbini",
                "latitude": 28.0833,
                "longitude": 81.6167,
            },
            {
                "name": "Janakpur Sub-Metropolitan Police Office",
                "location": "Janakpur, Province 2",
                "latitude": 26.7288,
                "longitude": 85.9263,
            },
            {
                "name": "Itahari Sub-Metropolitan Police Office",
                "location": "Itahari, Province 1",
                "latitude": 26.6667,
                "longitude": 87.2833,
            },
        ]

        stations = []
        for data in stations_data:
            station, _ = PoliceStation.objects.update_or_create(
                name=data["name"],
                defaults={
                    "location": data["location"],
                    "latitude": data["latitude"],
                    "longitude": data["longitude"],
                },
            )
            stations.append(station)
        return stations

    def _seed_reports(self, stations):
        names = [
            "Ram Bahadur Thapa", "Sita Devi Poudel", "Hari Prasad Sharma",
            "Gita Kumari Rai", "Krishna Prasad Adhikari", "Laxmi Devi Karki",
            "Bishnu Prasad Lamichhane", "Sarita Gurung", "Rajesh Kumar Thapa",
            "Anita Tamang", "Deepak Bahadur Magar", "Kamala Devi Bhattarai",
            "Suman Shrestha", "Rita Poudel", "Prakash Chandra Pandey",
            "Sunita Karki", "Manoj Kumar Dahal", "Pushpa Thapa",
            "Rabinra Basnet", "Bishakha Dangol", "Narayan Prasad Tiwari",
            "Mina Devi Khatiwada", "Sanjay K.C.", "Sabina Maharjan",
            "Arun Sigdel", "Lila Bhusal", "Dipak Bhandari",
            "Champa Devi Limbu", "Raju Giri", "Sangita Shrestha",
            "Binod Poudel", "Kamala Bhandari", "Ramesh Khadka",
            "Sarala Subedi", "Dinesh Koirala", "Anju Gurung",
            "Pradeep K.C.", "Mangala Devi Nyachhavane", "Tilak Bista",
            "Nirmala Poudel",
        ]

        emails = [
            "ram.thapa@email.com", "sita.poudel@email.com",
            "hari.sharma@email.com", "gita.rai@email.com",
            "krishna.adhikari@email.com", "laxmi.karki@email.com",
            "bishnu.lamichhane@email.com", "sarita.gurung@email.com",
            "rajesh.thapa@email.com", "anita.tamang@email.com",
            "deepak.magar@email.com", "kamala.bhattarai@email.com",
            "suman.shrestha@email.com", "rita.poudel@email.com",
            "prakash.pandey@email.com", "sunita.karki@email.com",
            "manoj.dahal@email.com", "pushpa.thapa@email.com",
            "rabinra.basnet@email.com", "bishakha.dangol@email.com",
        ]

        phones = [
            "9841000001", "9841000002", "9841000003", "9841000004",
            "9841000005", "9841000006", "9841000007", "9841000008",
            "9841000009", "9841000010", "9841000011", "9841000012",
            "9841000013", "9841000014", "9841000015", "9841000016",
            "9841000017", "9841000018", "9841000019", "9841000020",
        ]

        incidents = [
            {
                "title": "Armed Robbery at Local Tea Shop",
                "description": "Two masked individuals entered a tea shop in New Road and threatened the owner at knifepoint. Approximately Rs. 35,000 in cash and a mobile phone were stolen. The incident was captured on nearby CCTV. The suspects fled on foot towards Thamel.",
            },
            {
                "title": "Domestic Violence Complaint",
                "description": "A 28-year-old woman reported physical abuse by her husband at their residence in Baneshwor. Visible injuries were documented by responding officers. The victim has been provided with emergency shelter information and a protection order has been requested from the district court.",
            },
            {
                "title": "Motorcycle Theft",
                "description": "A black Bajaj Pulsar (Registration Ba. 42 Pa. 1234) was stolen from the parking area of Civil Mall overnight. The owner parked the vehicle at approximately 7:30 PM. No signs of forced ignition were found, suggesting a duplicate key may have been used.",
            },
            {
                "title": "Burglary at Residential Property",
                "description": "Break-in reported at a house in Jawalakhel during the owner's absence. Entry was forced through the back door. Gold jewelry worth approximately Rs. 1,50,000 and two mobile phones were stolen. Fingerprints were collected from the door handle.",
            },
            {
                "title": "Hit and Run Accident",
                "description": "A pedestrian was struck by a speeding vehicle at the Koteshwor crossing. The victim, a 50-year-old male, sustained fractures to both legs and was rushed to Tribhuvan University Teaching Hospital. Eyewitnesses described a white Toyota sedan with a damaged front bumper.",
            },
            {
                "title": "Online Banking Fraud",
                "description": "A 62-year-old retired government employee received a phishing SMS claiming to be from his bank. The victim clicked the link and entered his banking credentials. Rs. 2,20,000 was transferred to unknown accounts across three transactions. The complaint was filed within three hours.",
            },
            {
                "title": "Assault Near Thamel Nightlife District",
                "description": "A 24-year-old tourist was attacked by two individuals near a bar in Thamel at approximately 1:30 AM. The victim suffered a broken jaw and was treated at a private hospital. The altercation reportedly started over a dispute at the bar earlier in the evening.",
            },
            {
                "title": "Shoplifting at Bhat-Bhateni Supermarket",
                "description": "Security personnel at Bhat-Bhateni Supermarket detained a man attempting to conceal Rs. 8,500 worth of groceries and electronics in his bag. The suspect has been identified as a repeat offender with a prior shoplifting record at the same store.",
            },
            {
                "title": "Eve Teasing and Stalking",
                "description": "A 21-year-old college student at Tribhuvan University reported being followed and harassed by an unknown male on a motorcycle for the past five days during her commute. The suspect has been captured on multiple traffic cameras near Kirtipur.",
            },
            {
                "title": "Public Intoxication and Vandalism",
                "description": "Three individuals caused a disturbance at Garden of Dreams, damaging park benches, a fountain, and flower beds. Police responded to multiple complaints from nearby residents. The suspects were apprehended near the park entrance and found to be heavily intoxicated.",
            },
            {
                "title": "Missing Person - Elderly",
                "description": "A 75-year-old man suffering from early-stage dementia went missing from his residence in Satdobato at approximately 5:30 PM. Family last saw him wearing a daura suruwal. He was found safe at a bus park in Ratnapark 10 hours later.",
            },
            {
                "title": "Drug Possession - Hashish",
                "description": "During a routine patrol near Ratna Park, police found 1.8 kg of hashish in a backpack belonging to a 32-year-old male. The suspect was arrested and charges filed under the Narcotic Drugs (Control) Act, 2033.",
            },
            {
                "title": "Road Rage Incident on Ring Road",
                "description": "A verbal altercation between two drivers escalated to physical violence on the Bagmati section of Ring Road. One driver used a iron rod to damage the other's windshield and struck the victim on the arm. Both parties have filed counter-complaints at the local station.",
            },
            {
                "title": "Landlord-Tenant Dispute Turning Violent",
                "description": "A landlord physically assaulted his tenant during an argument over pending rent payments in New Baneshwor. The tenant, a single mother of two, suffered a sprained wrist. Neighbors intervened and called the police. Medical examination confirmed the injury.",
            },
            {
                "title": "Theft from Construction Site",
                "description": "Copper wiring worth Rs. 2,80,000 was stolen from an under-construction commercial building in Sanepa. The theft occurred over the weekend when the site was unguarded. Security footage from a nearby building shows a pickup truck parked near the site at 2:00 AM.",
            },
            {
                "title": "Suicide Attempt Rescue",
                "description": "A 22-year-old woman was found on the ledge of a 10-story building in Dilli Bazaar threatening to jump. Police and fire brigade responded. After a three-hour negotiation led by a trained counselor, the woman was safely brought down. She has been referred for mental health support.",
            },
            {
                "title": "Rash Driving and DUI",
                "description": "A 29-year-old man was stopped at a checkpoint in Ratnapark after driving erratically and nearly hitting two pedestrians. Breathalyzer test showed blood alcohol content of 0.16%, well above the legal limit. The vehicle was impounded and the driver's license has been suspended.",
            },
            {
                "title": "Property Encroachment and Threat",
                "description": "Unauthorized construction material was dumped on a private property belonging to a retired teacher in Kapan. When the owner confronted the encroachers, they threatened him with violence. The Kathmandu Metropolitan City office has been notified and a complaint filed.",
            },
            {
                "title": "Fake Travel Agency Scam",
                "description": "Multiple victims reported being defrauded by a fake travel agency in Thamel offering cheap Everest Base Camp trek packages. At least 12 people paid deposits totaling Rs. 3,75,000 via eSewa and IME but received no services. The office was found locked and the operators have fled.",
            },
            {
                "title": "Child Labour Found at Brick Kiln",
                "description": "An anonymous tip led to a raid at a brick kiln in Bhaktapur where four minors aged 9, 11, 13, and 15 were found working in hazardous conditions. The children were rescued and the kiln owner has been booked under the Child Labour Prohibition and Regulation Act.",
            },
        ]

        statuses = list(ActionStatus)
        count = 0

        for station in stations:
            shuffled_incidents = incidents.copy()
            random.shuffle(shuffled_incidents)
            selected = shuffled_incidents[:10]

            for i, incident in enumerate(selected):
                days_ago = random.randint(1, 60)
                hours_ago = random.randint(0, 23)
                crime_dt = timezone.now() - timedelta(days=days_ago, hours=hours_ago)

                name_idx = (stations.index(station) * 10 + i) % len(names)
                status = random.choice(statuses)

                CrimeReport.objects.create(
                    title=incident["title"],
                    description=incident["description"],
                    crime_datetime=crime_dt,
                    name=names[name_idx],
                    email=emails[name_idx % len(emails)],
                    phone_number=phones[name_idx % len(phones)],
                    status=status,
                    report_taken_by_station=station,
                    is_private=random.choice([True, False]),
                    is_granted=random.choice([True, False]),
                )
                count += 1

        return count
