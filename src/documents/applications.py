from typing import Any, Dict, Optional, Union
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from io import BytesIO

from src.schemas.user import UserSchema
from src.schemas.applications.transfer import TransferApplicationSchema
from src.schemas.applications.change import ChangeApplicationSchema
from src.schemas.applications.reinstatement import ReinstatementApplicationSchema

from pprint import pprint


class ApplicationRendered:
    def __init__(self) -> None:
        self.template_dir = (
            Path(os.path.dirname(os.path.abspath(__file__))) / "applications"
        )
        self.env = Environment(loader=FileSystemLoader(self.template_dir))

    def transfer(
        self, user: UserSchema, application: TransferApplicationSchema
    ) -> BytesIO:
        template = self.env.get_template("/transfer/index.html")
        css_path = self.template_dir / "transfer" / "style.css"
        html_content = template.render(
            user=user,
            application=application,
            context={
                "user": user.model_dump(),
                "application": application.model_dump(),
            },
        )
        pdf_file = BytesIO()
        HTML(string=html_content, base_url=str(self.template_dir)).write_pdf(
            pdf_file, stylesheets=[css_path]
        )
        pdf_file.seek(0)

        return pdf_file

    def change(self, user: UserSchema, application: ChangeApplicationSchema) -> BytesIO:
        template = self.env.get_template("/change/index.html")
        css_path = self.template_dir / "change" / "style.css"
        html_content = template.render(
            user=user,
            application=application,
            context={
                "user": user.model_dump(),
                "application": application.model_dump(),
            },
        )
        pdf_file = BytesIO()
        HTML(string=html_content, base_url=str(self.template_dir)).write_pdf(
            pdf_file, stylesheets=[css_path]
        )
        pdf_file.seek(0)

        return pdf_file

    def reainstatement(
        self, user: UserSchema, application: ReinstatementApplicationSchema
    ) -> BytesIO:
        template = self.env.get_template("/reinstatement/index.html")
        css_path = self.template_dir / "reinstatement" / "style.css"
        html_content = template.render(
            user=user,
            application=application,
            context={
                "user": user.model_dump(),
                "application": application.model_dump(),
            },
        )
        pdf_file = BytesIO()
        HTML(string=html_content, base_url=str(self.template_dir)).write_pdf(
            pdf_file, stylesheets=[css_path]
        )
        pdf_file.seek(0)

        return pdf_file
