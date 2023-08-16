from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PokemaneForm(FlaskForm):
    pokemane = StringField('Enter Pokemon Names or Numbers:', validators=[DataRequired()])
    submit_btn = SubmitField(('Submit'))