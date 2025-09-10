(Recommended) Use a virtual environment
# from this project folder/directory

.. code-block:: bash

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

.. code-block:: bash

     pip install -r requirements.txt

If you use uv

.. code-block:: bash

    python -m pip install -U uv
    uv pip install -r requirements.txt


run listing_1, listing_2 and listing_3 all are within this current directory

