from models import *
from database import init_db, db_session
from datetime import datetime

class CivPol:

    currentUser = None
    currentIssue = None

    def registerUser(self, username, email, displayName, password):
        if len(username) != 0 and len(email) != 0 and len(displayName) != 0 and len(password) != 0:
            user = db_session.query(User).where(User.username == username).first()
            if user is None:
                db_session.add(User(username, email, displayName, password, datetime.now()))
                db_session.commit()
                self.currentUser = db_session.query(User).where(User.username == username).first()
                return 0
            else:
                return 1
        else:
            return 2

    def loginUser(self, username, password):
        if len(username) != 0 and len(password) != 0:
            user = db_session.query(User).where((User.username == username) & (User.password == password)).first()
            if user is not None:
                self.currentUser = user
                return 0
            else:
                return 1
        else:
            return 2

    def createIssue(self, title, content):
        issue = Issue(title, content, datetime.now(), self.currentUser.username)

        db_session.add(issue)
        db_session.commit()

        self.currentIssue = issue

    def createPolicy(self, title, content):
        policy = Policy(title, content, datetime.now(), self.currentUser.username, self.currentIssue.id)

        policy.dislikes

        db_session.add(policy)
        db_session.commit()

    def setIssue(self, issueNum):
        self.currentIssue = db_session.query(Issue).all()[-issueNum]

    def issueFeed(self):
        return reversed(db_session.query(Issue).all())

    #Madly Inefficient
    def policyFeed(self):
        return reversed(db_session.query(Policy).where(Policy.issue_id == self.currentIssue.id).all())
    
    def dateOfCreation(self):
        day = self.currentUser.creation_date.strftime("%m")
        month = self.currentUser.creation_date.strftime("%d")
        year = self.currentUser.creation_date.strftime("%Y")

        return day+"/"+month+"/"+year
    
    def issuesNum(self):
        return len(db_session.query(Issue).where(Issue.user_id == self.currentUser.username).all())
    
    def policiesNum(self):
        return len(db_session.query(Policy).where(Policy.user_id == self.currentUser.username).all())
    
    def run(self):
        init_db()