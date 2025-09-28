# requina-bot

Originally made by Kuroneko, mantaining by Faber

## Installations

1. Clone the repository with submodules:

```bash
git clone --recurse-submodules https://github.com/faberuser/requina-bot.git
cd requina-bot
```

2. If already cloned without submodules, initialize them:

```bash
git submodule update --init --recursive
```

3. Install requirements from requirements.txt:

```bash
pip install -r requirements.txt
```

4. Set token:

```bash
export DISCORD_TOKEN=<token>
export GENAI_KEY=<gemini_token>
```

5. Run:

```bash
python main.py
```
