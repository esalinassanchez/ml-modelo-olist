install:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

train:
	python -m src.train --config configs/config.yaml

predict:
	python -m src.predict --config configs/config.yaml --input ./dataset/dataset_v4.csv --output ./artifacts/predictions.csv

test:
	pytest -q

format:
	# add formatters/linters as needed

e2e: train predict
	@echo "Run training then predict"
