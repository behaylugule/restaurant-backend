import os
from restaurant import settings
from weasyprint import HTML
import base64
from django.template.loader import get_template


def render_to_pdf(template_name, context_dict, as_base64=True):
    template_path = os.path.join(settings.BASE_DIR, "templates",  template_name)
    context = {"data": context_dict}
    template = get_template(template_path)
    html = template.render(context)

    # Provide a fixed base URL (for static files or assets)
    base_url = settings.SITE_URL

    pdf_file = HTML(string=html, base_url=base_url).write_pdf()

    if as_base64:
        # Return base64-encoded string
        return base64.b64encode(pdf_file).decode('utf-8')
    else:
        # Return a regular HttpResponse (for download via view)
        from django.http import HttpResponse
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="output.pdf"'
        return response
