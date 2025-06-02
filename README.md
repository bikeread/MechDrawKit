# MechDrawKit 1.0 - 机械工程图纸生成工具包

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

基于策略模式的模块化机械工程图纸生成工具，完全符合GB/T制图标准。

## ✨ 特性

- 🏗️ **模块化架构**: 基于策略模式、工厂模式等设计模式
- 🔄 **100%向后兼容**: 原有代码无需任何修改
- 📏 **GB标准合规**: 完全符合GB/T制图标准
- 🎨 **丰富的绘图功能**: 基础图形、尺寸标注、工程符号、视图处理
- 📋 **模板系统**: 预定义的零件绘图模板
- ⚙️ **配置外化**: JSON格式的GB标准配置管理

## 🚀 快速开始

### 安装

```bash
# 基础安装
pip install -r requirements.txt

# 开发环境安装
pip install -r requirements-dev.txt

# 或使用Makefile
make install      # 基础安装
make install-dev  # 开发安装
```

### 基本使用

```python
import ezdxf
from drawing_tools import RiceMillDrawingTools

# 创建DXF文档
doc = ezdxf.new('R2010')
msp = doc.modelspace()

# 创建绘图工具（向后兼容）
tools = RiceMillDrawingTools(msp, doc)

# 绘制基础图形
tools.draw_circle((50, 50), 20)
tools.draw_rectangle((0, 0), 100, 60)
tools.add_dimension((0, 0), (100, 0), 15)

# 保存文件
doc.saveas("my_drawing.dxf")
```

### 新架构特性

```python
from mechdrawkit import ComponentFactory, EzdxfAdapter, GBStandardConfig

# 使用新架构组件
config = GBStandardConfig()
canvas = EzdxfAdapter(msp, doc, config)
basic_shapes = ComponentFactory.create_strategy('basic_shapes', canvas, config)

# 策略组件绘图
basic_shapes.draw('circle', center=(50, 50), radius=20)
```

## 📁 项目结构

```
MechDrawKit/
├── mechdrawkit/                    # 📦 主包目录
│   ├── __init__.py                 # 包初始化，导出所有主要接口
│   ├── drawing_tools.py            # 🎨 主绘图工具类（RiceMillDrawingTools）
│   ├── tools/                      # 🔧 工具模块
│   │   ├── __init__.py             # 工具包初始化
│   │   └── table_methods.py        # 表格处理工具（原universal_table_methods.py）
│   ├── core/                       # 🏗️ 核心架构
│   │   ├── strategies/             # 策略模式组件
│   │   ├── adapters.py             # 适配器模式
│   │   ├── factory.py              # 工厂模式
│   │   └── templates.py            # 模板系统
│   └── config/                     # ⚙️ 配置管理
│       ├── gb_standards.json       # GB标准配置
│       └── gb_standards.py         # 配置管理器
├── templates/                      # 📋 DXF模板文件目录
├── output/                         # 📤 输出文件目录
├── drawing_tools.py               # 🔄 向后兼容接口
├── universal_table_methods.py     # 🔄 向后兼容接口
├── example_usage.py               # 📚 使用示例
├── requirements.txt               # 📋 运行依赖
├── requirements-dev.txt           # 📋 开发依赖
├── setup.py                       # 📦 安装配置
├── pyproject.toml                 # ⚙️ 现代Python配置
├── Makefile                       # 🔨 项目管理命令
└── README.md                      # 📖 项目文档
```

## 🛠️ 开发环境设置

### 使用Makefile（推荐）

```bash
# 一键设置开发环境
make setup-dev

# 或分步操作
make venv          # 创建虚拟环境
make install-dev   # 安装开发依赖
```

### 手动设置

```bash
# 1. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 2. 安装依赖
pip install -r requirements-dev.txt

# 3. 设置pre-commit钩子
pre-commit install
```

## 🧪 测试和检查

```bash
# 运行测试
make test

# 运行测试并生成覆盖率
make test-cov

# 代码检查
make lint

# 类型检查
make type-check

# 代码格式化
make format

# 运行所有检查
make check-all
```

## 📖 使用示例

运行完整的演示示例：

```bash
# 运行演示
make demo
# 或
python example_usage.py
```

演示包括：
1. 向后兼容性演示
2. 新架构特性演示  
3. 模板系统使用
4. 混合使用模式
5. 配置系统展示

## 📦 构建和发布

```bash
# 构建包
make build

# 检查包
make check

# 上传到测试PyPI
make upload-test

# 上传到PyPI
make upload
```

## 🏗️ 架构设计

### 设计模式

- **策略模式**: 4个绘图策略组件，按职责分离
- **工厂模式**: 统一组件创建和管理
- **适配器模式**: 封装ezdxf接口，自动应用GB标准
- **单例模式**: 全局配置管理
- **模板方法模式**: 标准化绘图流程
- **门面模式**: 保持简单的外部接口

### 架构分层

```
应用层: RiceMillDrawingTools (门面类)
模板层: DrawingTemplate (绘图模板)
策略层: 4个策略组件 (基础图形、尺寸、符号、视图)
基础设施层: Factory + Adapter + Config
```

## 🔧 配置说明

### GB标准配置 (`mechdrawkit/config/gb_standards.json`)

包含完整的GB制图标准配置：
- 线型定义
- 图层映射  
- 文字高度
- 线宽标准
- 箭头尺寸
- 比例列表

### 工具配置 (`pyproject.toml`)

现代Python项目配置，包含：
- Black代码格式化
- isort导入排序
- pytest测试配置
- mypy类型检查
- pylint代码检查
- coverage覆盖率

## 📄 依赖说明

### 运行时依赖
- `ezdxf>=1.0.0`: DXF文件处理核心库
- `numpy>=1.21.0`: 数学计算和几何操作

### 开发依赖
- 测试: `pytest`, `pytest-cov`, `pytest-mock`
- 文档: `sphinx`, `sphinx-rtd-theme`
- 工具: `pre-commit`, `jupyter`, `ipython`

## 📜 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🆘 支持

- 📖 [完整文档](https://bikeread.github.io/MechDrawKit/)
- 🐛 [问题反馈](https://github.com/MechDrawKit/mechdrawkit/issues)
- 💬 [讨论区](https://github.com/MechDrawKit/mechdrawkit/discussions)
