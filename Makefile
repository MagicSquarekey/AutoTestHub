.PHONY: help setup clean new-project

# 默认目标
help: ## 显示帮助信息
	@echo "可用命令："
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## 初始化项目
	pip install -r requirements.txt
	@echo "项目初始化完成！"

clean: ## 清理临时文件
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf reports/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

new-project: ## 创建新项目
	python utils/create_project.py
