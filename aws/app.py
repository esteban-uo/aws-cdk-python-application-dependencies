import os
from aws_cdk import core

from stack import Stack

ENV = dict()

app = core.App()

Stack(app, 'app', env=ENV)

app.synth()