from typing import List
from .submission import Submission


class SubmissionTable:
    def __init__(self, submissions: List[Submission] = []):
        self.submissions: List[Submission] = submissions

    def save_session(self):
        return self.submissions

    def add_submission(self, submission: Submission):
        self.submissions.append(submission)

    def remove_submission(self, submission: Submission):
        self.submissions.remove(submission)

    def is_empty(self):
        return len(self.submissions) == 0

    def get_submission(self):
        return self.submissions
