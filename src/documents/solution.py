from io import BytesIO

from docxtpl import DocxTemplate
from math import floor

from src.schemas.user import UserSchema
from src.schemas.applications.application import ApplicationForListViewSchema
from src.schemas.rups import GetRupDataResponseSchema
from src.models import Program
from src.gateways.dto.maps import MapsAupInfo

degree_level = {
    1: "СПО",
    2: "Бакалавриат",
    3: "Магистратура",
    4: "Специалитет",
    5: "Аспирантура",
}



class SolutionRenderer:
    def __init__(self, ):
        pass

    def _checkbox(self, state: bool) -> str:
        return "☒" if state else '☐'

    def solution(
        self,
        user: UserSchema,
        application_type: str,
        aup_num: str,
        aup_info: MapsAupInfo,
        target: Program,
        rup_data: GetRupDataResponseSchema
    ) -> tuple[BytesIO, str]:
        context = {
            "user_fullname": user.fullname,
            "sem_num": target.sem_num,
            "course_num": floor((target.sem_num + 1) / 2),
            "program": target.okso,
            "profile": target.profile,
            "study_group": user.study_group,
            "form": target.form,
            "base": target.base,
            "year_begin": aup_info.year_beg,
            "degree_level": degree_level[aup_info.id_degree],
            "full_study_period": aup_info.period_educ,
            "rup_num": aup_num,
            "reinstatement_symbol": self._checkbox(application_type == 'reinstatement'),
            "transfer_symbol": self._checkbox(application_type == 'transfer'),
            "change_symbol": self._checkbox(application_type == 'change'),
            "fired_university_symbol": self._checkbox(False),
            "fired_self_symbol": self._checkbox(True),
            "rups": self._get_rups(rup_data),
        }

        filename = f"/app/src/documents/templates/vm-solution-template.docx"
        doc = DocxTemplate(filename)
        doc.render(context)

        file = BytesIO()
        doc.save(file)
        file.seek(0)

        return file, filename


    def _get_rups(self, rup_data: GetRupDataResponseSchema):
        res = []
        discipline_num = 0
        for i, discipline in enumerate(rup_data.target):
            if discipline.title in rup_data.choosen and (rup_data.choosen[discipline.title].variants.values()):
                continue

            res.append(
                {
                    "num": 0,
                    "title": discipline.title,
                    "zet": f"{int(discipline.zet)} З.Е.",
                    "control": discipline.control,
                    "coursework": "Да" if discipline.coursework else "",
                    "sem": discipline.period,
                    "study_year": floor((discipline.period + 1) / 2),
                    "department": {
                        "title": '',
                        "address": '',
                        "phone": '',
                        "email": '',
                    }
                }
            )

        res = sorted(res, key=lambda x: x["sem"])
        for el in res:
            discipline_num += 1
            el['num'] = discipline_num
        return res

