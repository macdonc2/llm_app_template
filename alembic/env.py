import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
print("Effective sys.path:", sys.path)

from app.db import engine
from app.models import Base

target_metadata = Base.metadata