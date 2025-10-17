from apps.cms.models import Page

# Get the privacy page
privacy_page = Page.objects.get(page_type='privacy')

# Update with comprehensive content
privacy_page.content = '''<h2>Privacy Policy</h2>
<p><em>Last updated: October 17, 2025</em></p>

<p>Your privacy is important to us. It is NutriHarvest's policy to respect your privacy regarding any information we may collect from you across our website, https://nutriharvest.com, and other sites we own and operate.</p>

<h3 class="mt-4">Information We Collect</h3>

<h4 class="mt-3">Personal Information</h4>
<p>While using our website, we may ask you to provide us with certain personally identifiable information that can be used to contact or identify you. Personally identifiable information may include, but is not limited to:</p>
<ul>
<li>Name</li>
<li>Email address</li>
<li>Phone number</li>
<li>Address</li>
<li>Payment information</li>
<li>Order history</li>
</ul>

<h4 class="mt-3">Non-Personal Information</h4>
<p>We may also collect non-personal information about how you access and use our website, including:</p>
<ul>
<li>Browser type and version</li>
<li>Device information</li>
<li>Operating system</li>
<li>Pages viewed and time spent on pages</li>
<li>Referring website</li>
<li>IP address</li>
</ul>

<h3 class="mt-4">How We Use Your Information</h3>
<p>We use the information we collect to provide, maintain, and improve our services, including:</p>
<ul>
<li>Process and fulfill your orders</li>
<li>Communicate with you about your orders and inquiries</li>
<li>Send you marketing communications (with your consent)</li>
<li>Improve our website and customer service</li>
<li>Prevent fraud and ensure security</li>
<li>Comply with legal obligations</li>
</ul>

<h3 class="mt-4">Cookies and Tracking Technologies</h3>
<p>We use cookies and similar tracking technologies to track activity on our website and hold certain information. Cookies are files with a small amount of data which may include an anonymous unique identifier. You can instruct your browser to refuse all cookies or to indicate when a cookie is being sent.</p>

<h3 class="mt-4">Data Security</h3>
<p>We implement appropriate security measures to protect against unauthorized access, alteration, disclosure, or destruction of your personal information. However, no method of transmission over the Internet or electronic storage is 100% secure.</p>

<h3 class="mt-4">Data Sharing</h3>
<p>We do not sell, trade, or otherwise transfer your personally identifiable information to outside parties without your consent, except as required by law or to trusted third parties who assist us in operating our website or conducting our business.</p>

<h3 class="mt-4">Your Rights</h3>
<p>You have the right to access, update, or delete your personal information. You may also have the right to object to or restrict certain processing of your data. To exercise these rights, please contact us using the information below.</p>

<h3 class="mt-4">Changes to This Policy</h3>
<p>We may update our Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page and updating the "Last updated" date.</p>

<h3 class="mt-4">Contact Us</h3>
<p>If you have any questions about this Privacy Policy, please contact us at:</p>
<p>Email: privacy@nutriharvest.com<br>Phone: +1-234-567-8900</p>'''

privacy_page.save()
print('Privacy page content updated successfully')