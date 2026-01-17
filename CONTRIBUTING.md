# Contributing to Healthcare SaaS Platform

Thank you for your interest in contributing to the Healthcare SaaS Platform!

## Code of Conduct

This project adheres to professional standards for healthcare software development. Please be respectful and constructive in all interactions.

## How to Contribute

### Reporting Issues

- Use the GitHub issue tracker
- Provide detailed information about the issue
- Include steps to reproduce
- Mention your environment (OS, Python version, etc.)

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Run linting (`black . && isort . && flake8 .`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use Black for code formatting
- Use isort for import sorting
- Write meaningful commit messages
- Add docstrings to all functions and classes
- Keep functions small and focused

### Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for high test coverage
- Test both success and failure scenarios

### Security

- Never commit secrets or credentials
- Follow HIPAA/GDPR compliance guidelines
- Report security vulnerabilities privately to security@healthcare-saas.com

## Development Setup

```bash
# Clone the repository
git clone https://github.com/sojipariola/healthcare-saas.git
cd healthcare-saas

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run tests
pytest
```

## Questions?

Feel free to open an issue for questions or reach out to the maintainers.
