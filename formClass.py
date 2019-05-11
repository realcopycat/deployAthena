from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class QuestionForm(Form):
    question = StringField('直接说出你的疑问吧~~', validators=[Required()])
    submit = SubmitField('搜索')
