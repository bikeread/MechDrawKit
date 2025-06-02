# MechDrawKit - 项目管理Makefile

.PHONY: help install install-dev clean test lint format type-check docs build upload demo

# 默认目标
help:
	@echo "MechDrawKit - 机械工程图纸生成工具包"
	@echo ""
	@echo "可用命令:"
	@echo "  install       - 安装项目依赖"
	@echo "  install-dev   - 安装开发依赖"
	@echo "  clean         - 清理构建文件"
	@echo "  test          - 运行测试"
	@echo "  test-cov      - 运行测试并生成覆盖率报告"
	@echo "  lint          - 代码检查"
	@echo "  format        - 代码格式化"
	@echo "  type-check    - 类型检查"
	@echo "  docs          - 生成文档"
	@echo "  build         - 构建包"
	@echo "  upload        - 上传到PyPI"
	@echo "  demo          - 运行演示示例"
	@echo "  setup-dev     - 设置开发环境"

# 安装项目依赖
install:
	pip install -r requirements.txt

# 安装开发依赖
install-dev:
	pip install -r requirements-dev.txt

# 设置开发环境
setup-dev: install-dev
	pre-commit install
	@echo "开发环境设置完成！"

# 清理构建文件
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .tox/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# 运行测试
test:
	pytest

# 运行测试并生成覆盖率报告
test-cov:
	pytest --cov=mechdrawkit --cov-report=html --cov-report=term

# 代码检查
lint:
	flake8 mechdrawkit/ drawing_tools.py example_usage.py
	pylint mechdrawkit/ drawing_tools.py

# 代码格式化
format:
	black mechdrawkit/ drawing_tools.py example_usage.py
	isort mechdrawkit/ drawing_tools.py example_usage.py

# 类型检查
type-check:
	mypy mechdrawkit/

# 生成文档
docs:
	cd docs && make html

# 构建包
build: clean
	python -m build

# 检查包
check: build
	twine check dist/*

# 上传到测试PyPI
upload-test: build check
	twine upload --repository testpypi dist/*

# 上传到PyPI
upload: build check
	twine upload dist/*

# 运行演示示例
demo:
	python example_usage.py

# 运行所有检查
check-all: lint type-check test-cov
	@echo "所有检查完成！"

# 安装包到本地环境（开发模式）
install-local:
	pip install -e .

# 创建虚拟环境
venv:
	python -m venv venv
	@echo "虚拟环境已创建，请运行 'source venv/bin/activate' (Linux/Mac) 或 'venv\\Scripts\\activate' (Windows)"

# Git相关操作
git-push: check-all
	git add .
	git commit -m "Update: $(shell date)"
	git push

# 显示项目信息
info:
	@echo "项目名称: MechDrawKit"
	@echo "版本: 1.0.0"
	@echo "Python版本: $(shell python --version)"
	@echo "虚拟环境: $(VIRTUAL_ENV)"
	@echo "当前分支: $(shell git branch --show-current 2>/dev/null || echo 'Not a git repository')" 