setup: requirements.txt
	pip install -r requirements.txt

run:
	python3 PrepareGitReport.py ${PARAMS}

clean:
	rm -rf __pycache__

.PHONY: run clean
