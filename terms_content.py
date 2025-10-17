from apps.cms.models import Page

# Get the terms page
terms_page = Page.objects.get(page_type='terms')

# Update with comprehensive content
terms_page.content = '''<h2>Terms & Conditions</h2>
<p><em>Last updated: October 17, 2025</em></p>

<p>Welcome to NutriHarvest. These terms and conditions outline the rules and regulations for the use of NutriHarvest's website, located at https://nutriharvest.com.</p>

<p>By accessing this website, we assume you accept these terms and conditions. Do not continue to use NutriHarvest if you do not agree to take all of the terms and conditions stated on this page.</p>

<h3 class="mt-4">Intellectual Property</h3>
<p>Unless otherwise stated, NutriHarvest and/or its licensors own the intellectual property rights for all material on NutriHarvest. All intellectual property rights are reserved. You may access this from NutriHarvest for your own personal use subjected to restrictions set in these terms and conditions.</p>

<h3 class="mt-4">User Content</h3>
<p>In these Terms and Conditions, "User Content" shall mean any audio, video text, images or other material you choose to display on this website. By displaying User Content, you grant NutriHarvest a non-exclusive, worldwide, irrevocable, sublicensable license to use, reproduce, adapt, publish, translate and distribute it in any and all media.</p>

<h3 class="mt-4">Orders and Payments</h3>
<p>By placing an order through our website, you are making an offer to purchase the products specified. All orders are subject to acceptance and availability. We reserve the right to refuse any order for any reason.</p>
<p>Prices for products are subject to change without notice. We endeavor to display accurate pricing information, but errors may occur. In the event of an error, we reserve the right to cancel any orders placed at the incorrect price.</p>

<h3 class="mt-4">Shipping and Delivery</h3>
<p>Shipping costs are additional to the product price and will be calculated at checkout. Delivery times are estimates only and are not guaranteed. Risk of loss and title for products pass to you upon our delivery to the carrier.</p>

<h3 class="mt-4">Returns and Refunds</h3>
<p>Our returns and refunds policy forms part of these terms and conditions. Please review our Returns & Refunds policy for complete information on returns and exchanges.</p>

<h3 class="mt-4">Limitation of Liability</h3>
<p>In no event shall NutriHarvest, nor its directors, employees, partners, agents, suppliers, or affiliates, be liable for any indirect, incidental, special, consequential or punitive damages, including without limitation, loss of profits, data, use, goodwill, or other intangible losses, resulting from your access to or use of or inability to access or use the service.</p>

<h3 class="mt-4">Changes to These Terms</h3>
<p>We reserve the right, at our sole discretion, to modify or replace these Terms at any time. If a revision is material, we will provide at least 30 days' notice prior to any new terms taking effect. What constitutes a material change will be determined at our sole discretion.</p>

<h3 class="mt-4">Governing Law</h3>
<p>These Terms shall be governed and construed in accordance with the laws of United States, without regard to its conflict of law provisions.</p>

<h3 class="mt-4">Contact Us</h3>
<p>If you have any questions about these Terms & Conditions, please contact us at:</p>
<p>Email: legal@nutriharvest.com<br>Phone: +1-234-567-8900</p>'''

terms_page.save()
print('Terms page content updated successfully')