class User:
    def __init__(self, name, password, salt_p) -> None:
        """
        params:
            name: name of the user
            password: password of the user
            salt_p: salt for the password
        """
        self.__name = name
        self.__password = password  # la idea es que sea un hash
        self.__salt_p = salt_p

    @property
    def salt_p(self):
        return self.__salt_p

    @salt_p.setter
    def salt_p(self, salt_p):
        self.__salt_p = salt_p

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if name == "":
            raise ValueError("Name cannot be empty")
        elif len(name) > 50:
            raise ValueError("Name cannot be longer than 50 characters")

        self.__name = name

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        # check if password is hashed
        if password == "":
            raise ValueError("Password cannot be empty")
        self.__password = password

    def __dict__(self):
        return {
            "name": self.name,
            "password": self.password,
            "salt_p": self.salt_p
        }
