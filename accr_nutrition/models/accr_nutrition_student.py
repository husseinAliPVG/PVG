import datetime
from odoo import models, fields, api, _

class accrNutritionStudent(models.Model):
    _name = 'accr.nutrition.student'
    _description = 'Student Nutrition Details'
    _sql_constraints = [('student_unique', 'unique(student)', 'Can not be duplicate value for this field!')]

    name = fields.Char(string=u'Name', compute='_compute_name', )

    student = fields.Many2one('x_student', string=u'Student', required=True, index=True, )
    student_photo = fields.Binary(related='student.x_studio_student_image', string=u'Photo', store=False, readonly=True, )
    student_birth_date = fields.Date(related='student.x_studio_birthdate', string=u'Birth Date', store=False, readonly=True, )
    student_age = fields.Char(string=u'Age', compute='_compute_age', readonly=True,  )
    student_gander = fields.Selection(related='student.x_studio_gander', string=u'Gander', store=False, readonly=True, )
    student_nationality = fields.Many2one(related='student.x_studio_country', string=u'Nationality', store=False, readonly=True, )
    student_medical_diagnosis = fields.Char(related='student.x_studio_medical_diagnosis', string=u'Medical Diagnosis', store=False, readonly=True, )
    student_diagnosis = fields.Text(related='student.x_studio_diagnosis', string=u'Diagnosis', store=False, readonly=True, )
    student_guardians = fields.Many2many(related='student.x_guardians', string=u'Guardians', store=False, readonly=True, )
    student_file_no = fields.Char(related='student.x_studio_file_no', string=u'File No', store=False, readonly=True, )
    student_admission_date = fields.Date(related='student.x_studio_joining_date', string=u'Admission Date', store=False, readonly=True, )
    student_residential_section = fields.Many2one(related='student.x_studio_residential_sections', string=u'Residential Section', readonly=True, store=False, )
    # student_medications = fields.One2many(related='student.x_medications', string=u'Medications', store=False)

    food_intolerance = fields.One2many('accr.student.food.intolerance', 'nutrition_student', string=u'Food Intolerance', )
    nutrition_details = fields.One2many('accr.student.nutrition.details', 'nutrition_student', string=u'Nutrition Assessment', )
    food_preferences = fields.One2many('accr.student.food.preferences', 'nutrition_student', string=u'Food Preferences', )

    @api.multi
    @api.depends('student')
    def _compute_name(self):
        for record in self:
            record.name = record.student.display_name


    @api.onchange()
    def _on_change_age(self):
        nowdate = datetime.datetime.today()
        birthdate = self.student_birth_date
        for record in self:
            if record.student_birth_date:
                record.student_age = str(nowdate.year - birthdate.year - ((nowdate.month, nowdate.day) < (birthdate.month, birthdate.day))) + ' years'

    # @api.onchange(student_medications)
    # def _compute_medications_intolerance(self):
    #     for record in self:
    #         food_types = []
    #         current_date = datetime.datetime.now()
    #         for medication in record.student_medications:
    #             if current_date < medication.end_date_time:
    #                 medicine = medication.medicine
    #                 for medical_contraindication in medicine.medical_contraindication:
    #                     for food_type in medical_contraindication.food_types:
    #                         food_types.append({'student': record.student.id, 'nutrition_details': record.id, 'food_type':food_type.id})
            
    #         record.food_intolerance = self.env['accr.student.food.intolerance'].create(food_types)