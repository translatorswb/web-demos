import os.path
import uuid
from pathlib import Path
import markdown
from ..config import settings

def openfile(filename):
    filepath = os.path.join("app/pages/", filename)
    with open(filepath, "r", encoding="utf-8") as input_file:
        text = input_file.read()

    html = markdown.markdown(text)
    data = {
        "text": html
    }
    return data

def create_workspace():
    """
    Return workspace path
    """
    # base directory
    work_dir = Path(settings.work_dir)
    # UUID to prevent file overwrite
    request_id = Path(str(uuid.uuid4())[:8])
    # path concat instead of work_dir + '/' + request_id
    workspace = work_dir / request_id
    if not os.path.exists(workspace):
        # recursively create workdir/unique_id
        os.makedirs(workspace)

    return workspace
