# Doc AI Assistant

It is just a try to beat ChatGPT

# Setup

1. Install dependencies

   ```shell
   sudo apt install build-essential libpoppler-cpp-dev pkg-config python3-dev
   ```

2. Clone the repository and install python packages

   ```shell
   git clone git@github.com:ibraym/doc-ai-assistant.git
   cd doc-ai-assistant
   python3 -m venv .env
   . .env/bin/activate
   pip install -U pip wheel setuptools
   pip install \
    -r requirements/development.txt \
    -r requirements/production.txt
   ```
