from flask import Blueprint
router = Blueprint("router", __name__)
from router.users import *
from router.videos import *
from router.utils import *