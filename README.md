# AI Phase 1 — Hello LLM Script

This project contains my first working LLM script as part of Phase 1 of my AI Engineering learning path.

## What this script does

`hello_llm.py` prompts the user for a brief description and returns generated marketing copy via the OpenAI Chat Completions API.

This demonstrates the basic model integration loop:

- local Python environment
- secure API key loading via `.env`
- user input → LLM request → formatted output

## Requirements

- Python 3.9+ (recommended 3.10 or 3.11)
- Virtual environment (`venv` recommended)
- OpenAI API key

## Setup

Clone or move into the project directory and install dependencies:

