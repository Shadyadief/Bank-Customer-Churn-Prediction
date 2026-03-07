.PHONY: install run test lint clean

# ── Setup ─────────────────────────────────────────────────────
install:
	pip install -r requirements.txt

# ── Run Streamlit App ─────────────────────────────────────────
run:
	streamlit run app/streamlit_app.py

# ── Tests ─────────────────────────────────────────────────────
test:
	pytest tests/ -v

# ── Lint ──────────────────────────────────────────────────────
lint:
	flake8 src/ app/ --max-line-length=100

# ── Train Models ──────────────────────────────────────────────
train:
	python src/models/train_model.py

# ── Clean ─────────────────────────────────────────────────────
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +
	echo "✅ Cleaned!"
