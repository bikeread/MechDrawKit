# MechDrawKit - 机械工程图纸生成工具包
# 重构版本基于策略模式和工厂模式

__version__ = "1.0.0"
__author__ = "MechDrawKit Team"
__description__ = "机械工程图纸生成辅助工具"

# 导入主要的重构组件
from .config.gb_standards import GBStandardConfig
from .core.adapters import EzdxfAdapter
from .core.factory import ComponentFactory

# 导入策略组件
from .core.strategies.base import DrawingStrategy
from .core.strategies.basic_shapes import BasicShapeDrawer
from .core.strategies.dimensions import DimensionDrawer
from .core.strategies.symbols import SymbolDrawer
from .core.strategies.views import ViewDrawer

# 导入模板系统
from .core.templates import DrawingTemplate, ShaftTemplate, GearTemplate

# 导入主要绘图工具
from .drawing_tools import RiceMillDrawingTools, generate_part_drawing, find_project_root

# 导入工具函数
from .tools import update_title_block, add_parts_table, add_part_to_table

# 主要的公共API
__all__ = [
    # 配置管理
    'GBStandardConfig',
    
    # 适配器和工厂
    'EzdxfAdapter',
    'ComponentFactory',
    
    # 策略组件基类
    'DrawingStrategy',
    
    # 具体策略组件
    'BasicShapeDrawer',
    'DimensionDrawer', 
    'SymbolDrawer',
    'ViewDrawer',
    
    # 模板系统
    'DrawingTemplate',
    'ShaftTemplate',
    'GearTemplate',
    
    # 主要绘图工具
    'RiceMillDrawingTools',
    'generate_part_drawing',
    'find_project_root',
    
    # 工具函数
    'update_title_block',
    'add_parts_table',
    'add_part_to_table',
] 