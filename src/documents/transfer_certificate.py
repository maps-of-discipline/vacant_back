from docxtpl import DocxTemplate
from io import BytesIO


class TransferCertificateRenderer:
    def __init__(self):
        self.template_path = '/app/src/documents/templates/transfer-certificate-template.docx'

    def render(self, fullname: str, program: str) -> BytesIO:
        context = {
            "user_fullname": fullname,
            "program": program,
        }

        file = BytesIO()
        template = DocxTemplate(self.template_path)
        template.render(context)
        template.save(file)
        file.seek(0)
        return file
