from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Email, Regexp, Optional
from flask_babel import gettext, lazy_gettext
from dateutil.relativedelta import relativedelta
import datetime
from app.main.helpers import construct_county_choices
import os

class FormStep0(FlaskForm):
    name_first = StringField(lazy_gettext('0_first'), validators=[DataRequired(message=lazy_gettext('Required'))])
    name_last = StringField(lazy_gettext('0_last'), validators=[DataRequired(message=lazy_gettext('Required'))])
    dob = StringField(lazy_gettext('0_dob'), validators=[DataRequired(message=lazy_gettext('Required')), Regexp('^\d{2}\/\d{2}\/\d{4}$', message=lazy_gettext('0_dob_flag'))])
    county = SelectField(lazy_gettext('0_county'),
                         validators=[DataRequired(message=lazy_gettext('Required'))],
                         choices=construct_county_choices(lazy_gettext('0_county'))
                         )
    email = StringField(lazy_gettext('0_email'), validators=[DataRequired(message=lazy_gettext('Required')), Email(message=lazy_gettext('0_email_flag'))])
    phone = StringField(lazy_gettext('0_phone'), validators=[Optional(), Regexp('^\d{3}[\-\.]?\d{3}[\-\.]?\d{4}$', message=lazy_gettext('0_phone_help'))])

    if os.getenv('RECAPTCHA_KEY'):
        recaptcha = RecaptchaField()

    def validate_dob(self, field):
        time_now = datetime.datetime.utcnow()
        time_dob = datetime.datetime.strptime(field.data, '%m/%d/%Y')
        diff = relativedelta(time_now, time_dob).years
        if diff <= 15:
            field.errors.append(lazy_gettext('0_dob_help'))
            return False
        return True