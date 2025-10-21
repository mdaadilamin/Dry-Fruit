from django.core.management.base import BaseCommand
from apps.cms.models import CareersSection, CareersCultureItem, CareersTestimonial, CareersBenefit, CareersJobOpening

class Command(BaseCommand):
    help = 'Populate default careers page data'

    def handle(self, *args, **options):
        # Create default sections
        sections_data = [
            {'section_type': 'hero', 'title': 'Join Our Growing Team', 'subtitle': 'Join our mission to deliver premium quality dry fruits and nuts from farms around the world directly to your doorstep.', 'order': 0},
            {'section_type': 'culture', 'title': 'Our Culture', 'order': 1},
            {'section_type': 'testimonials', 'title': 'What Our Team Says', 'order': 2},
            {'section_type': 'benefits', 'title': 'Employee Benefits', 'order': 3},
            {'section_type': 'openings', 'title': 'Current Openings', 'order': 4},
            {'section_type': 'cta', 'title': 'Ready to Join Our Team?', 'subtitle': 'Send your resume to hr@dryfruithouse.com', 'content': 'Apply Now', 'order': 5},
        ]

        for data in sections_data:
            section, created = CareersSection.objects.get_or_create(
                section_type=data['section_type'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created section: {section.title}')

        # Create default culture items
        culture_items_data = [
            {'title': 'Health & Wellness', 'description': 'We promote a healthy lifestyle with access to our premium products and wellness programs.', 'icon_name': 'heart', 'order': 0},
            {'title': 'Collaboration', 'description': 'Work with talented professionals in a supportive, inclusive environment.', 'icon_name': 'users', 'order': 1},
            {'title': 'Growth Opportunities', 'description': 'Unleash your potential with continuous learning and development programs.', 'icon_name': 'trending-up', 'order': 2},
            {'title': 'Recognition', 'description': 'We celebrate achievements and reward outstanding performance.', 'icon_name': 'award', 'order': 3},
        ]

        for data in culture_items_data:
            item, created = CareersCultureItem.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created culture item: {item.title}')

        # Create default testimonials
        testimonials_data = [
            {'name': 'Sarah Johnson', 'position': 'Marketing Manager', 'testimonial': 'Working at DRY FRUITS DELIGHT has been transformative. The company truly values employee growth and provides amazing opportunities to innovate.', 'order': 0},
            {'name': 'Michael Chen', 'position': 'Product Specialist', 'testimonial': 'The collaborative environment and focus on quality products make this a truly rewarding place to work. I\'ve grown both professionally and personally.', 'order': 1},
            {'name': 'Priya Sharma', 'position': 'Customer Experience Lead', 'testimonial': 'DRY FRUITS DELIGHT\'s commitment to quality and customer satisfaction aligns perfectly with my values. It\'s fulfilling to work for a company that makes a positive impact.', 'order': 2},
        ]

        for data in testimonials_data:
            testimonial, created = CareersTestimonial.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created testimonial: {testimonial.name}')

        # Create default benefits
        benefits_data = [
            {'title': 'Health Insurance', 'description': 'Comprehensive medical, dental, and vision coverage for you and your family.', 'icon_name': 'heart-pulse', 'order': 0},
            {'title': 'Flexible Time Off', 'description': 'Generous PTO policy and flexible work arrangements to support work-life balance.', 'icon_name': 'calendar', 'order': 1},
            {'title': 'Professional Development', 'description': 'Tuition reimbursement and learning opportunities to advance your career.', 'icon_name': 'graduation-cap', 'order': 2},
            {'title': 'Product Discounts', 'description': 'Enjoy exclusive discounts on our premium dry fruits and nuts.', 'icon_name': 'shopping-bag', 'order': 3},
            {'title': 'Competitive Compensation', 'description': 'Market-leading salaries with performance-based bonuses and equity options.', 'icon_name': 'dollar-sign', 'order': 4},
            {'title': 'Remote Options', 'description': 'Hybrid and remote work options for eligible positions to support flexibility.', 'icon_name': 'home', 'order': 5},
        ]

        for data in benefits_data:
            benefit, created = CareersBenefit.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created benefit: {benefit.title}')

        # Create default job openings
        openings_data = [
            {
                'title': 'E-commerce Manager',
                'department': 'Sales & Marketing',
                'location': 'Remote/Office',
                'description': 'We\'re looking for an experienced E-commerce Manager to lead our online sales strategy and drive growth across our digital platforms.',
                'responsibilities': 'Develop and execute e-commerce strategy to increase sales and customer engagement\nManage product listings, pricing, and promotional campaigns\nAnalyze sales data and customer behavior to optimize performance\nCollaborate with marketing team on digital campaigns and SEO',
                'requirements': '3+ years of e-commerce management experience\nBachelor\'s degree in Business, Marketing, or related field\nStrong analytical skills and data-driven approach\nExperience with Shopify, WooCommerce, or similar platforms',
                'order': 0
            },
            {
                'title': 'Quality Assurance Specialist',
                'department': 'Operations',
                'location': 'Warehouse Facility',
                'description': 'Join our team as a Quality Assurance Specialist to ensure our products meet the highest standards of quality and freshness.',
                'responsibilities': 'Inspect incoming products for quality and compliance with standards\nMonitor storage conditions and expiration dates\nDocument quality control processes and findings\nCoordinate with suppliers to resolve quality issues',
                'requirements': '2+ years of quality assurance experience in food industry\nKnowledge of food safety regulations and standards\nAttention to detail and strong organizational skills\nAbility to work in a fast-paced warehouse environment',
                'order': 1
            },
            {
                'title': 'Software Engineer',
                'department': 'Technology',
                'location': 'Remote/Office',
                'description': 'We\'re seeking a talented Software Engineer to help build and maintain our e-commerce platform and internal tools.',
                'responsibilities': 'Develop and maintain web applications using Django and JavaScript\nCollaborate with cross-functional teams to implement new features\nOptimize application performance and scalability\nWrite clean, maintainable, and well-documented code',
                'requirements': '3+ years of experience with Python/Django development\nProficiency in JavaScript, HTML, and CSS\nExperience with database design and optimization\nBachelor\'s degree in Computer Science or related field',
                'order': 2
            },
        ]

        for data in openings_data:
            opening, created = CareersJobOpening.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created job opening: {opening.title}')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated default careers content!')
        )