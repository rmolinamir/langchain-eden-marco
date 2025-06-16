.PHONY: lint format typecheck check-all run clean spell

gen_langchain_docs:
	wget -r -A.html -P langchain_docs https://python.langchain.com/api_reference/

# Linting
lint:
	uv run ruff check .

# Formatting
format:
	uv run ruff format .

# Type checking
typecheck:
	uv run mypy src

# Spell checking
spell:
	npx cspell "**/*.{py,md,json,yaml,yml,toml}"

# Run all checks
check_all: lint format typecheck spell

# Run chapter 6 (streamlit)
chapter_6:
	uv run --env-file .env streamlit run src/chapter_6/app.py

# Default rule for running chapters
chapter_%:
	uv run --env-file .env python src/chapter_$*/main.py

# Run the project
run:
	uv run --env-file .env python src/main.py $(filter-out $@,$(MAKECMDGOALS))

# Clean up Python cache files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +

# Allow passing arguments to make run
%:
	@: 