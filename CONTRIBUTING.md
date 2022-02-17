# Contribute to Timexy

## Issues and bug reports
Bug reports, issues, feature requests and general improvement ideas are highly welcomed. Please open an appropriate and descriptive issue. 

## Contributing to the code base

1. Fork the repo
2. Clone the forked repo onto your local machine
3. Install the dependencies with
    ```bash
    poetry install
    ```
4. Create a new branch to hold your development changes
5. Implement changes and additions in your branch
6. Validate that all [tests](#running-the-tests) are passing and that your code follows the [code conventions](#code-conventions)
7. Push your changes to your fork and create a pull request from your fork to the main repository

### Code conventions

#### Code formatting

```bash
make style
```

#### Code linting

```bash
make lint
```

#### Pre-commit
After installing the dependencies, run ``pre-commit install`` to set up the git hook scripts.
Now ``pre-commit`` will run automatically on every commit and ensures that code style follows the [Timexy convention](#code-conventions).

### Running the tests
```bash
make test
```

### Adding a new language
🚧