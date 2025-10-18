from django.core.management.base import BaseCommand
import requests


class Command(BaseCommand):
    help = 'Ping search engines to notify them of sitemap updates'

    def add_arguments(self, parser):
        parser.add_argument(
            '--sitemap-url',
            type=str,
            default='https://dryfruithouse.com/sitemap.xml',
            help='URL of the sitemap (default: https://dryfruithouse.com/sitemap.xml)'
        )

    def handle(self, *args, **options):
        sitemap_url = options['sitemap_url']
        
        # Ping Google
        try:
            google_url = f'https://www.google.com/ping?sitemap={sitemap_url}'
            response = requests.get(google_url)
            if response.status_code == 200:
                self.stdout.write('Successfully pinged Google')
            else:
                self.stdout.write(f'Failed to ping Google: HTTP {response.status_code}')
        except Exception as e:
            self.stdout.write(f'Failed to ping Google: {e}')
        
        # Ping Bing
        try:
            bing_url = f'https://www.bing.com/ping?sitemap={sitemap_url}'
            response = requests.get(bing_url)
            if response.status_code == 200:
                self.stdout.write('Successfully pinged Bing')
            else:
                self.stdout.write(f'Failed to ping Bing: HTTP {response.status_code}')
        except Exception as e:
            self.stdout.write(f'Failed to ping Bing: {e}')
        
        self.stdout.write('Sitemap ping command completed')