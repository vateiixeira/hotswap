from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa
from io import BytesIO

def render_to_pdf(template_src, contextdict={}):
   template = get_template(template_src)
   html = template.render(context_dict)
   result = BytesIO()
   pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
   if not pdf.err:
      return HttpResponse(result.getvalue(), content_type = 'application/pdf')
   return None

class Render:
    @staticmethod
    def render(path: str, params: dict):
      template = get_template(path)
      html = template.render(params)
      response = BytesIO()
      pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
      if not pdf.err:
         return HttpResponse(response.getvalue(), content_type = 'application/pdf')
      else:
         return HttpResponse("Error Rendering PDF", status = 400)


#VERIFICA SE USUARIO É STAFF 

def is_staff(user):
   context = {}
   if user.is_staff == True:
      return True
   else:
      return False

