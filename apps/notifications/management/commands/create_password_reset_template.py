from django.core.management.base import BaseCommand
from apps.notifications.models import EmailTemplate


class Command(BaseCommand):
    help = 'Create password reset email template'

    def handle(self, *args, **options):
        # Create password reset email template
        template, created = EmailTemplate.objects.get_or_create(
            template_type='password_reset',
            defaults={
                'subject': 'Password Reset Request - DRY FRUITS DELIGHT',
                'body_html': '''
                <html>
                <body>
                    <h2>Password Reset Request</h2>
                    <p>Hello {{ user.get_full_name|default:user.username }},</p>
                    <p>You have requested a password reset for your DRY FRUITS DELIGHT account.</p>
                    <p>Click the link below to reset your password:</p>
                    <p><a href="{{ protocol }}://{{ domain }}{% url 'core:password_reset_confirm' uidb64=uid token=token %}" 
                         style="background-color: #0d6efd; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                         Reset Password</a></p>
                    <p>If the button doesn't work, copy and paste the following link into your browser:</p>
                    <p>{{ protocol }}://{{ domain }}{% url 'core:password_reset_confirm' uidb64=uid token=token %}</p>
                    <p>This link will expire in 24 hours.</p>
                    <p>If you didn't request this password reset, please ignore this email.</p>
                    <br>
                    <p>Best regards,<br>The DRY FRUITS DELIGHT Team</p>
                </body>
                </html>
                ''',
                'body_text': '''
                Password Reset Request

                Hello {{ user.get_full_name|default:user.username }},

                You have requested a password reset for your DRY FRUITS DELIGHT account.

                Click the link below to reset your password:\n
                {{ protocol }}://{{ domain }}{% url 'core:password_reset_confirm' uidb64=uid token=token %}

                This link will expire in 24 hours.

                If you didn't request this password reset, please ignore this email.

                Best regards,
                The DRY FRUITS DELIGHT Team
                ''',
                'is_active': True
            }
        )

        if created:
            self.stdout.write(
                'Successfully created password reset email template'
            )
        else:
            self.stdout.write(
                'Password reset email template already exists'
            )