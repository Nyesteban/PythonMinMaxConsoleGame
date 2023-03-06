class BoardValidatorError(Exception):
    pass


class BoardValidator:
    def _iscolumnvalid(self, c):
        # Checks if the column inputted by the human is valid (between 0 and 6), returns True if it is and False if not
        if c < 0 or c > 6:
            return False
        else:
            return True

    def validate(self, c):
        # Entry to the validator class
        # If one one of the conditions is False, it will raise an exception
        if self._iscolumnvalid(c) is False:
            raise BoardValidatorError("You must choose a column between 0 and 6!")
