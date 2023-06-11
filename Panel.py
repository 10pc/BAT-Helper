# KAP session / login handler by lk#2707
import requests


class InvalidCredentials(Exception):
    pass


class InvalidPassword(Exception):
    pass


# invoke a panel session with Panel() for each user. this ensures a unique session for each user.
# ex: session1 = Panel()
#     session2 = Panel()
# this way, user1 and user2 don't share the same session, and can login/logout independently.
# now it remains async and we can use this for multiple users at once.
# invoke functions via session1.login(),session2.logout() etc..
# if you want to add identifiers to each session, like a discord username, add variables starting with self. in the __init__ function.
# ex: self.username = message.author.id or something like that.
# then you can access it via session1.username, session2.username etc..
# u can log stuff from there and ta-da, u have a working panel session for each user.
# thank me later.
# -lk


class Panel:
    def __init__(self):
        # init a session for each user
        self.session = requests.session()
        self.logged_in = False

    def login(self, username: str, password: str):
        """Logs into KAP.
        :param username: The username to login with.
        :param password: The password to login with.
        """
        endpoint = "https://kap.kawata.pw/login"

        data = {"username": username, "password": password}

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        if self.session.cookies != None:
            print("Clearing cookies...")
            self.session.cookies.clear()

        try:
            response = self.session.post(endpoint, data=data, headers=headers)

            if (
                b"You do not have the required privileges to access this page."
                in response.content
            ):
                raise InvalidCredentials()

            elif b"The password you entered is incorrect." in response.content:
                raise InvalidPassword()

            return f"Logged in as {username} with Session ID {self.session.cookies['session']}."

        except InvalidCredentials:
            return "Invalid credentials."

        except InvalidPassword:
            return "Invalid password."

        except Exception as e:
            raise (e)

    def logout(self):
        """Logs out of KAP.
        Closes requests.Session() for user.
        """
        endpoint = "https://kap.kawata.pw/logout"

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        try:
            response = self.session.get(endpoint, headers=headers)
            return "Logged out."

            # Kill session after logging out
            self.session.close()

        except Exception as e:
            raise (e)

    def rank_map(self, map_id: int):
        """Ranks a map.
        :param map_id: The ID of the map to rank.
        """
        endpoint = f"https://kap.kawata.pw/rank/{map_id}"
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        data = {
            "bmapid-1": f"{map_id}",
            "rankstatus-1": "Ranked",
            "beatmapnumber": "1",
        }
        response = self.session.post(endpoint, data=data, headers=headers)
        if (
            "Successfully ranked a beatmap" in response.text
        ):  # why is this text the same no matter what
            return f"Ranked map {map_id}."
        else:
            return f"Failed to rank map {map_id}."

    def unrank_map(self, map_id: int):
        """Unranks a map.
        :param map_id: The ID of the map to unrank.
        """
        endpoint = f"https://kap.kawata.pw/rank/{map_id}"
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        data = {
            "bmapid-1": f"{map_id}",
            "rankstatus-1": "Unranked",
            "beatmapnumber": "1",
        }
        response = self.session.post(endpoint, data=data, headers=headers)
        if "Successfully ranked a beatmap" in response.text:
            return f"Unranked map {map_id}."
        else:
            return f"Failed to unrank map {map_id}."

    def love_map(self, map_id: int):
        """Loves a map.
        :param map_id: The ID of the map to love.
        """
        endpoint = f"https://kap.kawata.pw/rank/{map_id}"
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        data = {
            "bmapid-1": f"{map_id}",
            "rankstatus-1": "Loved",
            "beatmapnumber": "1",
        }
        response = self.session.post(endpoint, data=data, headers=headers)
        if "Successfully ranked a beatmap" in response.text:
            return f"Loved map {map_id}."
        else:
            return f"Failed to love map {map_id}."
