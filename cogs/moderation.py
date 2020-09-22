from modules import *


class MODERATION(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie


def setup(dottie):
    dottie.add_cog(MODERATION(dottie))
