(Recommended) Use a virtual environment
# from this project folder
python -m venv .venv
# activate it
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate


Upgrade pip (optional but helpful)

.. code-block:: bash

   python -m pip install --upgrade pip setuptools wheel

Install the frozen requirements

     pip install -r requirements.txt

python -m pip install -U uv
uv pip install -r requirements.txt