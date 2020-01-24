# essential-cosmic
Demonstration implemention of a kafka-like HTTP server.

## Setting up environment
`pipenv --three`

To access the virtual environment run:
`pipenv shell`

## Run development server
`adev runserver --livereload -v essential_cosmic`

## Run tests
`pytest --cov=essential_cosmic tests/`

## Check MYPY coverage
`mypy essential_cosmic`

## Notes / TODOs
Figure out how to customize error responses sent from HTTP Exceptions raised by handlers
Figure out if it's possible to associate a middleware with specefic routes rather than the entire application
Implement marshmello or some other libray to help create json representations of models
Define typing so we can reference types without triggering circular imports