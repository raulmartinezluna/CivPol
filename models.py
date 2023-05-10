"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT, DATETIME
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    #Columns
    username = Column("username", TEXT, primary_key=True)
    email = Column("email", TEXT, nullable=False)
    display_name = Column("display_name", TEXT, nullable=False)
    password = Column("password", TEXT, nullable=False)
    creation_date = Column("creation_date", DATETIME, nullable=False)

    #Relationships

    likes = relationship("Like", back_populates="user")
    dislikes = relationship("Dislike", back_populates="user")
    issues = relationship("Issue", back_populates="user")
    policies = relationship("Policy", back_populates="user")


    def __init__(self, username, email, display_name, password, creation_date):
        self.username = username
        self.email = email
        self.display_name = display_name
        self.password = password
        self.creation_date = creation_date

class Issue(Base):
    __tablename__ = "issues"

    #Columns
    id = Column("id", INTEGER, primary_key=True)
    title =  Column("title", TEXT, nullable=False)
    content = Column("content", TEXT, nullable=False)
    creation_date = Column("creation_date", DATETIME, nullable=False)
    user_id = Column('user_id', TEXT, ForeignKey("users.username"))

    #Relationships
    user = relationship("User", back_populates="issues")
    policies = relationship("Policy", back_populates="issue")


    def __init__(self, title, content, creation_date, user_id):
        self.title = title
        self.content = content
        self.creation_date = creation_date
        self.user_id = user_id

class Policy(Base):
    __tablename__ = "policies"

    #Columns
    id = Column("id", INTEGER, primary_key=True)
    title =  Column("title", TEXT, nullable=False)
    content = Column("content", TEXT, nullable=False)
    creation_date = Column("creation_date", DATETIME, nullable=False)
    user_id = Column('user_id', TEXT, ForeignKey("users.username"))
    issue_id = Column('issue_id', INTEGER, ForeignKey("issues.id"))

    #Relationships
    likes = relationship("Like", back_populates="policy")
    dislikes = relationship("Dislike", back_populates="policy")
    user = relationship("User", back_populates="policies")
    issue = relationship("Issue", back_populates="policies")


    def __init__(self, title, content, creation_date, user_id, issue_id):
        self.title = title
        self.content = content
        self.creation_date = creation_date
        self.user_id = user_id
        self.issue_id = issue_id

class Like(Base):
    __tablename__ = "likes"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    policy_id = Column('policy_id', TEXT, ForeignKey("policies.id"))
    user_id = Column('user_id', TEXT, ForeignKey("users.username"))

    #Relationships
    policy = relationship("Policy", back_populates="likes")
    user = relationship("User", back_populates="likes")

    def __init__(self, policy_id, user_id):
        self.policy_id = policy_id
        self.user_id = user_id

class Dislike(Base):
    __tablename__ = "dislikes"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    policy_id = Column('policy_id', TEXT, ForeignKey("policies.id"))
    user_id = Column('user_id', TEXT, ForeignKey("users.username"))

    #Relationships
    policy = relationship("Policy", back_populates="dislikes")
    user = relationship("User", back_populates="dislikes")

    def __init__(self, policy_id, user_id):
        self.policy_id = policy_id
        self.user_id = user_id