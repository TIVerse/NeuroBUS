# 📦 Publishing NeuroBUS

Guide for publishing NeuroBUS to PyPI and GitHub.

## Prerequisites

```bash
# Install build tools
pip install build twine

# Verify tests pass
pytest

# Verify code quality
black neurobus/ tests/
ruff check neurobus/ tests/
mypy neurobus/
```

## Building the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build source and wheel distributions
python -m build

# Verify the build
ls -lh dist/
# Should see:
#   neurobus-1.0.0-py3-none-any.whl
#   neurobus-1.0.0.tar.gz
```

## Testing the Package Locally

```bash
# Create a test virtualenv
python -m venv test_env
source test_env/bin/activate

# Install from local build
pip install dist/neurobus-1.0.0-py3-none-any.whl

# Test import
python -c "from neurobus import NeuroBus; print('✓ Import successful')"

# Deactivate and cleanup
deactivate
rm -rf test_env
```

## Publishing to TestPyPI (Optional)

```bash
# Upload to TestPyPI first
python -m twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ neurobus
```

## Publishing to PyPI

```bash
# Upload to PyPI
python -m twine upload dist/*

# Enter credentials when prompted
# Username: __token__
# Password: pypi-xxx... (your API token)
```

## Verify Published Package

```bash
# Check PyPI page
open https://pypi.org/project/neurobus/

# Install from PyPI
pip install neurobus

# Verify installation
python -c "from neurobus import NeuroBus, Event; print('✓ NeuroBUS installed')"
```

## GitHub Release

### 1. Create Git Tag

```bash
# Commit all changes
git add .
git commit -m "Release v1.0.0"

# Create tag
git tag -a v1.0.0 -m "NeuroBUS v1.0.0 - Production Release"

# Push tag
git push origin v1.0.0
```

### 2. Create GitHub Release

1. Go to: https://github.com/eshanized/neurobus/releases/new
2. Select tag: `v1.0.0`
3. Release title: `v1.0.0 - Production Release`
4. Description:

```markdown
# 🎉 NeuroBUS v1.0.0 - Production Release

**The World's First Neuro-Semantic Event Bus is now production-ready!**

## 🌟 Highlights

- ✅ 100% Specification Compliance
- ✅ 173 Tests Passing (95% Coverage)
- ✅ Full Type Safety (mypy strict)
- ✅ Production-Ready Features
- ✅ Comprehensive Documentation

## 🚀 Key Features

- 🎯 **Semantic Routing** - Events matched by meaning
- 🧠 **Context-Aware** - Hierarchical state management
- ⏰ **Temporal** - Time-travel debugging with causality
- 💾 **Memory** - Qdrant & LanceDB integration
- 🤖 **LLM Hooks** - OpenAI, Anthropic, Ollama support
- 🌐 **Distributed** - Redis clustering
- 📊 **Observable** - Comprehensive metrics

## 📦 Installation

```bash
pip install neurobus
```

## 📚 Documentation

- [README](./README.md)
- [Examples](./examples/)
- [API Docs](https://neurobus.readthedocs.io)

## 🔗 Links

- PyPI: https://pypi.org/project/neurobus/
- GitHub: https://github.com/eshanized/neurobus
- Docs: https://neurobus.readthedocs.io

**Full Changelog**: https://github.com/eshanized/neurobus/blob/main/CHANGELOG.md
```

5. Attach artifacts:
   - Upload `dist/neurobus-1.0.0-py3-none-any.whl`
   - Upload `dist/neurobus-1.0.0.tar.gz`

6. Click "Publish release"

## Post-Release Checklist

- [ ] Verify PyPI package page looks correct
- [ ] Test installation: `pip install neurobus`
- [ ] Verify GitHub release is visible
- [ ] Update documentation links
- [ ] Announce on social media/communities
- [ ] Update project badges in README
- [ ] Create release announcement blog post

## Troubleshooting

### Build Fails

```bash
# Check setup.py
python setup.py check

# Verify MANIFEST.in
python setup.py sdist
tar -tzf dist/neurobus-1.0.0.tar.gz | head -20
```

### Upload Fails

```bash
# Check credentials
cat ~/.pypirc

# Use API token instead of password
# Get token from: https://pypi.org/manage/account/token/

# Test with TestPyPI first
twine upload --repository testpypi dist/*
```

### Import Errors After Install

```bash
# Verify package structure
pip show neurobus

# Check installed files
pip show -f neurobus | grep neurobus

# Reinstall from source
pip install -e .
```

## API Tokens

### PyPI Token

1. Go to: https://pypi.org/manage/account/token/
2. Create token with scope: "Entire account"
3. Save to `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-AgENdGVzdC5...
```

### GitHub Token

For automated releases via GitHub Actions:

1. Go to: Settings → Developer settings → Personal access tokens
2. Create token with `repo` scope
3. Add as repository secret: `PYPI_API_TOKEN`

## Automated Release (GitHub Actions)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

## Support

For issues with publishing, contact:
- Email: eshanized@proton.me
- GitHub: @eshanized
