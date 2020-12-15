from imports import *


class LEVELS(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie


    with open("json/leveldata.json"):
        


def setup(dottie):
    dottie.add_cog(LEVELS(dottie))