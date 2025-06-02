# AI自主重构执行方案

## 📋 方案概述

本方案指导AI完成机械工程图纸工具的三天重构工作，将原有的1000+行巨类拆分为基于设计模式的模块化架构。

### 重构目标
- 将`RiceMillDrawingTools`拆分为策略组件
- 实现工厂模式管理组件
- 创建配置外置化系统
- 保持100%向后兼容性

### 执行原则
- 严格按步骤顺序执行
- 每个文件创建后立即验证语法
- 保持原有接口完全不变
- 所有硬编码配置必须外置

## 🗂️ 文件创建顺序

### 执行序列
```
1. 创建项目目录结构
2. 创建配置系统 (config/)
3. 创建策略基类 (core/strategies/base.py)
4. 创建具体策略组件 (core/strategies/)
5. 创建适配器 (core/adapters.py)
6. 创建工厂 (core/factory.py)
7. 创建模板系统 (core/templates.py)
8. 重构主门面类 (drawing_tools.py)
9. 创建使用示例 (examples/)
```

## 📂 Step 1: 创建项目目录结构

### 操作说明
创建完整的项目目录结构，为后续文件放置做准备。

### 目录结构
```
MechDrawKit/
├── mechdrawkit/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── strategies/
│   │       └── __init__.py
│   └── config/
│       └── __init__.py
├── examples/
└── docs/
```

### 执行要求
- 创建所有必要的目录
- 在每个Python包目录下创建`__init__.py`文件
- `__init__.py`文件内容暂时为空

## 📄 Step 2: 创建配置系统

### 2.1 创建GB标准配置文件

**文件**: `mechdrawkit/config/gb_standards.json`

**内容要求**:
```json
{
  "line_types": {
    "CONTINUOUS": {"description": "连续线", "pattern": []},
    "CENTER": {"description": "中心线", "pattern": [7.5, 5.0, -1.25, 0.0]},
    "HIDDEN": {"description": "虚线", "pattern": [1.25, -1.25]},
    "PHANTOM": {"description": "双点长划线", "pattern": [12.0, -3.0, 0.5, -3.0, 0.5, -3.0]},
    "DASHDOT": {"description": "点划线", "pattern": [5.0, -2.0, 0.0, -2.0]},
    "BORDER": {"description": "边界线", "pattern": [6.0, -2.0, 1.5, -2.0]},
    "DIVIDE": {"description": "分界线", "pattern": [1.0, -1.0]}
  },
  "layer_mapping": {
    "CENTERLINE": "4中心线",
    "HIDDEN": "5虚线",
    "DIMENSIONS": "1细实线",
    "TEXT": "3文字",
    "PARTS": "6外框",
    "HATCH": "3剖面线",
    "VISIBLE": "1细实线",
    "DETAIL": "2粗实线",
    "ANNOTATION": "3文字",
    "TABLE": "2粗实线",
    "AXIS": "4中心线",
    "SECTION": "2粗实线",
    "PHANTOM": "7双点长划线",
    "BORDER": "8边界线",
    "CUTTING_PLANE": "4中心线",
    "TOLERANCE": "3文字",
    "SURFACE_FINISH": "3文字",
    "WELD_SYMBOL": "3文字",
    "AUXILIARY": "9辅助线",
    "COORDINATE": "10坐标线",
    "TITLE_BLOCK": "2粗实线"
  },
  "line_weights": {
    "THIN": 0.25,
    "MEDIUM": 0.5,
    "THICK": 0.7,
    "EXTRA_THICK": 1.0
  },
  "text_heights": {
    "TITLE": 5.0,
    "SUBTITLE": 3.5,
    "NORMAL": 2.5,
    "SMALL": 1.8,
    "TINY": 1.4
  },
  "arrow_size": 3.0,
  "font_style": "chinese"
}
```

### 2.2 创建配置管理类

**文件**: `mechdrawkit/config/gb_standards.py`

**实现要求**:
- 创建`GBStandardConfig`类
- 支持JSON配置文件加载
- 提供获取线型、图层映射、文字高度等配置的方法
- 支持单例模式
- 包含`get_line_type()`, `get_layer_mapping()`, `get_text_height()`等方法

## 📄 Step 3: 创建策略基类

**文件**: `mechdrawkit/core/strategies/base.py`

**实现要求**:
- 创建抽象基类`DrawingStrategy`
- 定义抽象方法`draw(operation, **kwargs)`
- 包含`validate_params()`方法
- 构造函数接受`canvas_adapter`和`config_manager`参数
- 使用`from abc import ABC, abstractmethod`

## 📄 Step 4: 创建具体策略组件

### 4.1 基础图形策略

**文件**: `mechdrawkit/core/strategies/basic_shapes.py`

**实现要求**:
- 创建`BasicShapeDrawer`类继承`DrawingStrategy`
- 实现以下绘图操作:
  - `circle`: 绘制圆形
  - `rectangle`: 绘制矩形  
  - `line`: 绘制直线
  - `polyline`: 绘制多段线
  - `arc`: 绘制圆弧
  - `ellipse`: 绘制椭圆
  - `spline`: 绘制样条曲线
- 每个方法需要应用图层映射
- 使用`self.canvas`进行实际绘制

### 4.2 尺寸标注策略

**文件**: `mechdrawkit/core/strategies/dimensions.py`

**实现要求**:
- 创建`DimensionDrawer`类继承`DrawingStrategy`
- 实现以下标注操作:
  - `linear`: 线性尺寸标注
  - `radius`: 半径标注
  - `diameter`: 直径标注
  - `angular`: 角度标注
  - `aligned`: 对齐标注
  - `baseline`: 基准尺寸
  - `tolerance`: 公差标注
- 自动应用标注图层和样式

### 4.3 工程符号策略

**文件**: `mechdrawkit/core/strategies/symbols.py`

**实现要求**:
- 创建`SymbolDrawer`类继承`DrawingStrategy`
- 实现以下符号操作:
  - `roughness`: 表面粗糙度
  - `advanced_surface_finish`: 高级表面处理
  - `geometric_tolerance`: 几何公差
  - `welding_symbol`: 焊接符号
- 包含符号绘制的具体逻辑

### 4.4 视图处理策略

**文件**: `mechdrawkit/core/strategies/views.py`

**实现要求**:
- 创建`ViewDrawer`类继承`DrawingStrategy`
- 实现以下视图操作:
  - `section_line`: 剖面指示线
  - `section_view_label`: 剖视图标签
  - `detail_view`: 局部放大图
  - `leader_arrow`: 引出线
- 处理复杂的视图标注逻辑

## 📄 Step 5: 创建适配器

**文件**: `mechdrawkit/core/adapters.py`

**实现要求**:
- 创建`EzdxfAdapter`类
- 封装ezdxf的ModelSpace操作
- 构造函数接受`msp`和`doc`参数
- 实现以下方法:
  - `add_line(start, end, **attrs)`
  - `add_circle(center, radius, **attrs)`
  - `add_arc(center, radius, start_angle, end_angle, **attrs)`
  - `add_text(text, position, **attrs)`
  - `add_polyline(points, **attrs)`
- 自动应用GB标准配置
- 包含文档初始化方法`_setup_document()`

## 📄 Step 6: 创建工厂

**文件**: `mechdrawkit/core/factory.py`

**实现要求**:
- 创建`ComponentFactory`类
- 实现策略组件的注册和创建机制
- 包含以下类方法:
  - `register_strategy(name, strategy_class)`
  - `create_strategy(name, canvas, config)`
  - `list_strategies()`
- 支持懒加载和实例缓存
- 自动注册所有策略组件

## 📄 Step 7: 创建模板系统

**文件**: `mechdrawkit/core/templates.py`

**实现要求**:
- 创建抽象基类`DrawingTemplate`
- 实现模板方法`generate_drawing()`
- 定义标准绘图流程:
  - `_setup_document()`
  - `_create_title_block()`
  - `_setup_viewports()`
  - `_draw_main_view()` (抽象方法)
  - `_draw_auxiliary_views()` (抽象方法)
  - `_add_dimensions()`
  - `_add_annotations()`
  - `_finalize_drawing()`
- 创建具体模板类:
  - `ShaftTemplate`: 轴类零件模板
  - `GearTemplate`: 齿轮零件模板

## 📄 Step 8: 重构主门面类

**文件**: `drawing_tools.py` (重构现有文件)

**重构要求**:
- 保持`RiceMillDrawingTools`类名不变
- 保持所有公共方法签名完全一致
- 内部使用策略组件实现功能
- 构造函数初始化所有策略组件
- 每个原有方法委托给对应策略组件
- 保持所有常量定义(LINE_TYPES, LAYER_MAPPING等)为兼容性

**重构步骤**:
1. 导入新的组件
2. 修改`__init__`方法初始化策略组件
3. 逐一重构每个绘图方法，委托给策略组件
4. 保留所有原有类属性和常量

## 📄 Step 9: 创建使用示例

### 9.1 基础使用示例

**文件**: `examples/basic_usage.py`

**内容要求**:
- 展示重构后的基础使用方式
- 验证向后兼容性
- 包含图形绘制、标注、符号等示例

### 9.2 新架构特性示例

**文件**: `examples/advanced_usage.py`

**内容要求**:
- 展示工厂模式的使用
- 展示配置定制
- 展示模板的使用

## 🔍 验证检查点

### 每个文件创建后验证
- [ ] Python语法正确性
- [ ] 导入语句正确
- [ ] 类继承关系正确
- [ ] 方法签名符合要求

### 阶段性验证
- [ ] Step 2完成后: 配置系统可正常加载
- [ ] Step 4完成后: 所有策略组件可正常实例化
- [ ] Step 6完成后: 工厂可正常创建和管理组件
- [ ] Step 8完成后: 重构后的门面类保持原有接口

### 最终验证
- [ ] 原有使用方式完全兼容
- [ ] 所有绘图功能正常工作
- [ ] 新架构特性可正常使用
- [ ] 配置系统工作正常

## 📋 关键实现细节

### 策略组件实现
- 每个策略组件必须继承`DrawingStrategy`
- `draw()`方法第一个参数是操作类型
- 使用`**kwargs`接收操作参数
- 通过`self.canvas`调用适配器方法
- 通过`self.config`获取配置信息

### 门面类重构
- 构造函数创建适配器和配置对象
- 使用工厂创建所有策略组件
- 每个原有方法保持签名不变
- 方法内部委托给对应策略组件

### 配置系统
- 配置文件使用JSON格式
- 配置类支持单例模式
- 提供类型安全的配置访问方法

### 错误处理
- 策略组件中添加参数验证
- 适配器中处理ezdxf异常
- 工厂中处理组件创建异常

## 🚀 执行指令

**AI执行时遵循以下原则**:
1. 严格按照Step 1-9的顺序执行
2. 每个文件创建后验证语法正确性
3. 所有代码必须符合Python规范
4. 保持原有接口100%兼容
5. 充分利用现有代码逻辑，避免重写
6. 配置项必须从原代码中提取，不能遗漏

---

**执行版本**: v1.0  
**适用范围**: 机械工程图纸工具重构  