#! /usr/bin/env python3


# Helper class to store query and its title
class LogQuery():
    """
            # docstring for LogQuery
        # title -> the question asked
        # query -> the database query designed for the ques
    """
    def __init__(self, title, query):
        self.title = title
        self.query = query
