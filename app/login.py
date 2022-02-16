from app.auth import Authenticate


class LoginUser:
    def userLogin(
        self,
        username,
        password,
    ):
        auth = Authenticate()

        result = auth.authenticate(username, password)

        return (result[0], result[1], result[2])

    pass
