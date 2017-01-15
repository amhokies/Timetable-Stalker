class Course:
    def __init__(self, crn, label, title, professor):
        self.crn = crn
        self.label = label
        self.title = title
        self.professor = professor

    def __repr__(self):
        return "[{}] {} - {} with {}".format(self.crn, self.label, self.title, self.professor)

    def __eq__(self, other):
        if isinstance(other, Course):
            return self.crn == other.crn
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__repr__())
