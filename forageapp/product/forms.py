from flask_wtf import FlaskForm
from wtforms import (BooleanField, RadioField, StringField, SubmitField,
                     TextAreaField, TextField)
from wtforms.validators import Required


class FeedbackForm(FlaskForm):
    occupation = StringField('What is your occupation?', validators=[Required()])

    number_labels = {1: '    Not at all', 5: '    Extremely'}
    radio_choices = [(i, str(i) + {1: '    Not at all', 5: '    Extremely'}\
                    .get(i, '')) for i in range(1, 6)]

    op_index_useful = RadioField('How useful was the investment opportunity heatmap?', choices=radio_choices, validators=[Required()])
    op_index_easy = RadioField('How easy to use was the investment opportunity heatmap?', choices=radio_choices, validators=[Required()])
    custom_search_useful = RadioField('How useful was the custom search feature?', choices=radio_choices, validators=[Required()])
    custom_search_easy = RadioField('How easy to use was the custom search feature?', choices=radio_choices, validators=[Required()])
    auto_rent_useful = RadioField('How useful was the auto rent predictor?', choices=radio_choices, validators=[Required()])
    auto_rent_easy = RadioField('How easy to use was the auto rent predictor?', choices=radio_choices, validators=[Required()])

    feature_feedback = TextAreaField('Any comments about usefulness or useability of any of the features?')

    cities = TextField('What other cities would you like to see in future product offerings? (seperate responses with a comma)')

    submit = SubmitField('Submit Feedback')
