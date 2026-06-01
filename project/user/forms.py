# -*- coding: utf-8 -*-
"""
Forms
******

*Module* ``project.user.forms``

This module defines forms used inside User-System.

"""

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    TextAreaField,
    IntegerField,
    MultipleFileField,
    SelectField,
)
from wtforms.validators import InputRequired, Length, Email, Optional
from ..validators import InputValid, Unique, NotEqualTo, allowed_file
from ..models import User


class LoginForm(FlaskForm):
    """
    Extend :fform:`FlaskForm <flask_wtf.FlaskForm>`. Define login form.

    Attributes:
            username (:field:`StringField <wtforms.fields.StringField>`): username
            password (:field:`PasswordField <wtforms.fields.PasswordField>`): password of user
            remember (:field:`BooleanField <wtforms.fields.BooleanField>`): whether to remember
                                                                                                                            data of this account

    """

    username = StringField(
        "Username",
        validators=[
            InputRequired(message=""),
            Length(min=4, max=15),
            InputValid(model=User, field=User.username, message="Invalid username! Have you signed up?"),
        ],
    )
    password = PasswordField("Password", validators=[InputRequired(message=""), Length(min=8, max=80)])
    remember = BooleanField("Remember me")

    def validate(self, extra_validators=None):
        """
        Override :form:`validate() <wtforms.form.Form.validate>`.

        Check if given password is valid with given valid username.
        """
        if not FlaskForm.validate(self, extra_validators):
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user and self.password.data and user.check_password(self.password.data):
            return True
        self.password.errors.append("Invalid password!")
        return False


class RegisterForm(FlaskForm):
    """
    Extend :fform:`FlaskForm <flask_wtf.FlaskForm>`. Define registration form.

    Attributes:
            username (:field:`StringField <wtforms.fields.StringField>`): username
            email (:field:`StringField <wtforms.fields.StringField>`): user email
            password (:field:`PasswordField <wtforms.fields.PasswordField>`): user password

    """

    username = StringField(
        "Username",
        validators=[
            InputRequired(message=""),
            Length(min=4, max=15, message="Username must be between 4 and 15 characters long."),
            Unique(model=User, field=User.username, message="Username already exists! You can log in"),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            InputRequired(message=""),
            Email(message="Invalid email"),
            Length(max=50),
            Unique(
                model=User,
                field=User.email,
                message="Email already exists! Use another email if you want to be a new user",
            ),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(message=""),
            Length(min=8, max=80, message="Password must be between 8 and 80 characters long."),
        ],
    )

    def validate_username(form, self):
        """
        Validate :attr:`username`.

        Username is not allowed to have space or special character.
        """
        if not self.data.isalnum():
            self.errors.append("Username is not allowed to have space or special characters!")
            return False
        return True


class ProjectInformationForm(FlaskForm):
    """
    Extend :fform:`FlaskForm <flask_wtf.FlaskForm>`. Define form to upload a project.

    Attributes:
            upload (:field:`MultipleFileField <wtforms.fields.MultipleFileField>`): files of items
            name (:field:`StringField <wtforms.fields.StringField>`): project name
            description (:field:`TextAreaField <wtforms.fields.TextAreaField>`): project description
            anno_number (:field:`IntegerField <wtforms.fields.IntegerField>`): number of expected annotators
                                                                                                                                                    for this project
            best_def (:field:`StringField <wtforms.fields.StringField>`): Definition of '**best**'
                                                                                                                                    in this project
            worst_def (:field:`StringField <wtforms.fields.StringField>`): Definition of '**worst**'
                                                                                                                                    in this project
            mturk (:field:`BooleanField <wtforms.fields.BooleanField>`): Whether to upload this project
                                                                                                                                    on Mechanical Turk
            aws_access_key_id (:field:`StringField <wtforms.fields.StringField>`, optional): IAM AWS access key id,
                                                                                                                            *only provide if set* :attr:`mturk` == ``True``
            aws_secret_access_key (:field:`StringField <wtforms.fields.StringField>`, optional): IAM AWS secret access key,
                                                                                                                            *only provide if set* :attr:`mturk` == ``True``
            keywords (:field:`StringField <wtforms.fields.StringField>`, optional): keywords to describe the project
                                                                                                                            on Mechanical Turk, *default:* ``e.g. quick, sentiment, labeling``,
                                                                                                                            *only provide if set* :attr:`mturk` == ``True``
            reward (:field:`StringField <wtforms.fields.StringField>`, optional): reward for an annotator/turker
                                                                                                                            to annotate a HIT, *default:* ``0.15``,
                                                                                                                            *only provide if set* :attr:`mturk` == ``True``
            lifetime (:field:`IntegerField <wtforms.fields.IntegerField>`, optional): duration of the project
                                                                                                                            to be availabe on Mechanical Turk, *default:* ``1``,
                                                                                                                            *only provide if set* :attr:`mturk` == ``True``
            lifetimeunit (:field:`SelectField <wtforms.fields.SelectField>`, optional): duration unit for :attr:`lifetime`,
                                                                                                                            *default:* ``month``,
                                                                                                                            *only provide if set* :attr:`mturk` == ``True``
            hit_duration (:field:`IntegerField <wtforms.fields.IntegerField>`, optional): duration of a HIT annotation
                                                                                                                            for each annotator, *default:* ``1``,
                                                                                                                            *only provide if set* :attr:`mturk` == ``True``
            duration_unit (:field:`SelectField <wtforms.fields.SelectField>`, optional): duration unit for :attr:`hit_duration`,
                                                                                                                            *default:* ``month``,
                                                                                                                            *only provide if set* :attr:`mturk` == ``True``

    """

    upload = MultipleFileField("Upload file(s) of items (.txt)", validators=[InputRequired(message="")])
    name = StringField("Name of this project", validators=[Optional()])
    description = TextAreaField(
        "Description of this project (min. 20 characters)", validators=[InputRequired(message=""), Length(min=20)]
    )
    anno_number = IntegerField("Number of expected annotators for this project", validators=[InputRequired(message="")])
    best_def = StringField(
        "What does 'best' literally mean in this project?",
        validators=[InputRequired(message=""), NotEqualTo("worst_def", message="Both definitions are not the same!")],
    )
    worst_def = StringField(
        "What does 'worst' literally mean in this project?",
        validators=[InputRequired(message=""), NotEqualTo("best_def", message="Both definitions are not the same!")],
    )
    mturk = BooleanField("Upload project on Mechanical Turk Platform?", validators=[Optional()], default=False)

    # optional extra values if mturk == True
    aws_access_key_id = StringField(
        "Your IAM AWS access key", validators=[InputRequired("")], default="your_aws_access_key_id"
    )
    aws_secret_access_key = StringField(
        "Your IAM AWS secret access key", validators=[InputRequired("")], default="your_aws_secret_access_key"
    )
    keywords = StringField(
        "Keywords describing this project", validators=[InputRequired("")], default="quick, sentiment, labeling"
    )
    reward = StringField("Reward for each HIT", validators=[InputRequired("")], default="0.15")
    lifetime = IntegerField("Project lifetime", validators=[InputRequired("")], default=1)
    lifetimeunit = SelectField(
        "In unit",
        choices=[("m", "month(s)"), ("d", "day(s)"), ("h", "hour(s)"), ("min", "minute(s)")],
        default="h",
        validators=[Optional()],
    )
    hit_duration = IntegerField("HIT duration", validators=[InputRequired("")], default=1)
    duration_unit = SelectField(
        "In unit",
        choices=[("m", "month(s)"), ("d", "day(s)"), ("h", "hour(s)"), ("min", "minute(s)")],
        default="h",
        validators=[Optional()],
    )

    def validate_upload(form, self):
        """
        Validate uploaded files :attr:`upload`.

        Check if uploaded file(s) has/have one of the allowed extensions (*default:* ``{'txt'}``).
        """
        ALLOWED_EXTENSIONS = set(["txt"])
        if not any([allowed_file(file.filename) for file in self.data]):
            self.errors.append("No %s file(s)" % (", ".join(ALLOWED_EXTENSIONS)))
            return False

        return True
