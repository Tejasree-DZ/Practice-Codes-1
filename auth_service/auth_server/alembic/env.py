import sys
import os

# Add the parent folder (auth_service) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from auth_server.models.db_base import Base
target_metadata = Base.metadata