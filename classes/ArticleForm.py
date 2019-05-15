from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

class ArticleForm(FlaskForm):
    title = StringField('Titre :',validators =[Length(min=1, max=200)] )
    body = TextAreaField('Contenu :', validators=[Length(min=1,max=50)] )
