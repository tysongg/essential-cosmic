# essential-cosmic
Demonstration implemention of a kafka-like HTTP server.

## Setting up environment
`pipenv sync --dev`

To access the virtual environment run:
`pipenv shell`

## Run development server
`adev runserver --livereload -v essential_cosmic`

## Run tests
`pytest --cov=essential_cosmic tests/`

## Check MYPY coverage
`mypy essential_cosmic`
