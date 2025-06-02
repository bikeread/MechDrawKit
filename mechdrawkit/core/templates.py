from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple
from .factory import ComponentFactory
from .adapters import EzdxfAdapter
from ..config.gb_standards import GBStandardConfig


class DrawingTemplate(ABC):
    """绘图模板抽象基类
    
    实现模板方法模式，定义标准绘图流程
    """
    
    def __init__(self, msp, doc, config_manager: GBStandardConfig = None):
        """初始化绘图模板
        
        Args:
            msp: ezdxf模型空间对象
            doc: ezdxf文档对象
            config_manager: 配置管理器对象
        """
        self.msp = msp
        self.doc = doc
        self.config = config_manager or GBStandardConfig()
        self.canvas = EzdxfAdapter(msp, doc, self.config)
        
        # 创建策略组件
        self.basic_shapes = ComponentFactory.create_strategy('basic_shapes', self.canvas, self.config)
        self.dimensions = ComponentFactory.create_strategy('dimensions', self.canvas, self.config)
        self.symbols = ComponentFactory.create_strategy('symbols', self.canvas, self.config)
        self.views = ComponentFactory.create_strategy('views', self.canvas, self.config)
    
    def generate_drawing(self, **kwargs) -> Any:
        """生成图纸 - 模板方法
        
        定义标准绘图流程，子类通过重写抽象方法实现具体功能
        """
        # 1. 设置文档
        self._setup_document(**kwargs)
        
        # 2. 创建标题栏
        self._create_title_block(**kwargs)
        
        # 3. 设置视图
        self._setup_viewports(**kwargs)
        
        # 4. 绘制主视图
        self._draw_main_view(**kwargs)
        
        # 5. 绘制辅助视图
        self._draw_auxiliary_views(**kwargs)
        
        # 6. 添加尺寸标注
        self._add_dimensions(**kwargs)
        
        # 7. 添加注释
        self._add_annotations(**kwargs)
        
        # 8. 完成绘图
        self._finalize_drawing(**kwargs)
        
        return self.doc
    
    def _setup_document(self, **kwargs):
        """设置文档 - 默认实现"""
        # 文档设置已在EzdxfAdapter中完成
        pass
    
    def _create_title_block(self, **kwargs):
        """创建标题栏 - 默认实现"""
        # 可以在具体模板中重写以创建特定的标题栏
        pass
    
    def _setup_viewports(self, **kwargs):
        """设置视图 - 默认实现"""
        # 可以在具体模板中重写以设置特定的视图布局
        pass
    
    @abstractmethod
    def _draw_main_view(self, **kwargs):
        """绘制主视图 - 抽象方法，必须由子类实现"""
        pass
    
    @abstractmethod
    def _draw_auxiliary_views(self, **kwargs):
        """绘制辅助视图 - 抽象方法，必须由子类实现"""
        pass
    
    def _add_dimensions(self, **kwargs):
        """添加尺寸标注 - 默认实现"""
        # 可以在具体模板中重写以添加特定的尺寸标注
        pass
    
    def _add_annotations(self, **kwargs):
        """添加注释 - 默认实现"""
        # 可以在具体模板中重写以添加特定的注释
        pass
    
    def _finalize_drawing(self, **kwargs):
        """完成绘图 - 默认实现"""
        # 可以在具体模板中重写以进行最终的处理
        pass


class ShaftTemplate(DrawingTemplate):
    """轴类零件绘图模板
    
    适用于轴、销等旋转体零件的技术图纸生成
    """
    
    def _draw_main_view(self, origin: Tuple[float, float] = (0, 0), 
                       diameter: float = 20, length: float = 100, **kwargs):
        """绘制轴的主视图（正视图）"""
        x, y = origin
        
        # 绘制轴的外轮廓
        self.basic_shapes.draw('rectangle', lower_left=(x - length/2, y - diameter/2), 
                              width=length, height=diameter, layer='PARTS')
        
        # 绘制中心线
        self.basic_shapes.draw('centerline', start=(x - length/2 - 10, y), 
                              end=(x + length/2 + 10, y))
    
    def _draw_auxiliary_views(self, origin: Tuple[float, float] = (0, 0), 
                            diameter: float = 20, **kwargs):
        """绘制轴的辅助视图（左视图 - 圆形）"""
        x, y = origin
        
        # 在左侧绘制圆形视图
        view_x = x - 80
        self.basic_shapes.draw('circle', center=(view_x, y), radius=diameter/2, layer='PARTS')
        
        # 绘制中心线
        self.basic_shapes.draw('centerline', start=(view_x - diameter/2 - 5, y), 
                              end=(view_x + diameter/2 + 5, y))
        self.basic_shapes.draw('centerline', start=(view_x, y - diameter/2 - 5), 
                              end=(view_x, y + diameter/2 + 5))
    
    def _add_dimensions(self, origin: Tuple[float, float] = (0, 0), 
                       diameter: float = 20, length: float = 100, **kwargs):
        """添加轴的尺寸标注"""
        x, y = origin
        
        # 长度标注
        self.dimensions.draw('linear', p1=(x - length/2, y - diameter/2), 
                           p2=(x + length/2, y - diameter/2), distance=15)
        
        # 直径标注
        self.dimensions.draw('diameter', center=(x - 80, y), radius=diameter/2, angle=45)


class GearTemplate(DrawingTemplate):
    """齿轮零件绘图模板
    
    适用于齿轮等复杂零件的技术图纸生成
    """
    
    def _draw_main_view(self, origin: Tuple[float, float] = (0, 0), 
                       outer_diameter: float = 60, inner_diameter: float = 20, **kwargs):
        """绘制齿轮的主视图"""
        x, y = origin
        
        # 绘制外圆
        self.basic_shapes.draw('circle', center=(x, y), radius=outer_diameter/2, layer='PARTS')
        
        # 绘制内圆（孔）
        self.basic_shapes.draw('circle', center=(x, y), radius=inner_diameter/2, layer='PARTS')
        
        # 绘制中心线
        self.basic_shapes.draw('centerline', start=(x - outer_diameter/2 - 10, y), 
                              end=(x + outer_diameter/2 + 10, y))
        self.basic_shapes.draw('centerline', start=(x, y - outer_diameter/2 - 10), 
                              end=(x, y + outer_diameter/2 + 10))
    
    def _draw_auxiliary_views(self, origin: Tuple[float, float] = (0, 0), 
                            thickness: float = 15, outer_diameter: float = 60, **kwargs):
        """绘制齿轮的辅助视图（侧视图）"""
        x, y = origin
        
        # 在右侧绘制侧视图
        view_x = x + 80
        self.basic_shapes.draw('rectangle', lower_left=(view_x - thickness/2, y - outer_diameter/2), 
                              width=thickness, height=outer_diameter, layer='PARTS')
        
        # 绘制中心线
        self.basic_shapes.draw('centerline', start=(view_x, y - outer_diameter/2 - 10), 
                              end=(view_x, y + outer_diameter/2 + 10))
    
    def _add_dimensions(self, origin: Tuple[float, float] = (0, 0), 
                       outer_diameter: float = 60, inner_diameter: float = 20, **kwargs):
        """添加齿轮的尺寸标注"""
        x, y = origin
        
        # 外径标注
        self.dimensions.draw('diameter', center=(x, y), radius=outer_diameter/2, angle=45)
        
        # 内径标注
        self.dimensions.draw('diameter', center=(x, y), radius=inner_diameter/2, angle=135) 