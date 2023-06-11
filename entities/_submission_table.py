from typing import List
from ._submission import Submission


class SubmissionTable:
    def __init__(self, submissions=None):
        if submissions is None:
            submissions = []
        self.submissions: List[Submission] = submissions

    def save_session(self):
        return self.submissions

    def add_submission(self, submission: Submission):
        self.submissions.append(submission)
        print("added submission")

    def remove_submission(self, submission: Submission):
        for i, sub in enumerate(self.submissions):
            if sub.name == submission.name:
                self.submissions.pop(i)
    def is_empty(self):
        return len(self.submissions) == 0

    def get_submissions(self):
        return self.submissions

    def get_submission_names(self):
        return [sub.name for sub in self.submissions]
    def get_submission_uids(self):
        return [sub.uid for sub in self.submissions]

    def deserialize_submissions(self):
        subs = []

        if isinstance(self.submissions, dict):
            serialized_submissions = self.submissions["submissions"]
            for ss in serialized_submissions:
                # TODO: make init better
                subs.append(Submission(name=ss["name"],
                                       file_type=ss["file_type"],
                                       uid=ss["uid"],
                                       file_count=ss["file_count"],
                                       status=ss["status"],
                                       hash_table=ss["hash_table"]))
            self.submissions = subs

    def update_submissions(self, new_sub: Submission):
        if new_sub.uid not in self.get_submission_uids():
            self.add_submission(new_sub)
        else:
            i, _ = self.get_submission(new_sub.uid)
            self.submissions[i] = new_sub

    def get_submission(self, uid) -> (int, Submission):
        for i, sub in enumerate(self.submissions):
            if sub.uid == uid:
                return i, sub
        else:
            raise Exception("No submission of that name in DB")