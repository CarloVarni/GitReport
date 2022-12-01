setup: requirements.txt
	pip3 install -r requirements.txt

run:
	python3 PrepareGitReport.py ${PARAMS}

clean:
	rm -rf __pycache__

.PHONY: run clean
