import math
from typing import Any, Tuple, List, Optional
from .base import DrawingStrategy


class ViewDrawer(DrawingStrategy):
    """视图处理绘制策略
    
    负责绘制剖面指示线、剖视图标签、局部放大图等视图相关功能
    """
    
    def draw(self, operation: str, **kwargs) -> Any:
        """执行视图处理绘制操作
        
        Args:
            operation: 操作类型 ('section_line', 'section_view_label', 'detail_view', 'text')
            **kwargs: 操作参数
            
        Returns:
            绘图结果对象
        """
        if not self.validate_params(operation, **kwargs):
            raise ValueError(f"Invalid parameters for operation: {operation}")
        
        if operation == 'section_line':
            return self._add_section_line(**kwargs)
        elif operation == 'section_view_label':
            return self._add_section_view_label(**kwargs)
        elif operation == 'detail_view':
            return self._add_detail_view(**kwargs)
        elif operation == 'text':
            return self._add_text(**kwargs)
        else:
            raise ValueError(f"Unsupported operation: {operation}")
    
    def _add_section_line(self, start_point: Tuple[float, float], end_point: Tuple[float, float], 
                         section_label: str = "A", arrow_size: float = 3) -> Any:
        """添加剖面指示线"""
        mapped_layer = self._get_layer('CUTTING_PLANE')
        
        # 计算方向向量
        dx = end_point[0] - start_point[0]
        dy = end_point[1] - start_point[1]
        length = math.sqrt(dx*dx + dy*dy)
        
        elements = []
        
        if length > 0:
            # 单位向量
            dx /= length
            dy /= length
            
            # 法向量（垂直于方向向量）
            nx = -dy
            ny = dx
            
            # 箭头在单位向量方向上偏移
            arrow_offset = 5  # 箭头偏移量
            
            # 计算箭头位置
            arrow1_center = (
                start_point[0] + arrow_offset * dx,
                start_point[1] + arrow_offset * dy
            )
            
            arrow2_center = (
                end_point[0] - arrow_offset * dx,
                end_point[1] - arrow_offset * dy
            )
            
            # 绘制主线
            elements.append(self.canvas.add_line(start_point, end_point, layer=mapped_layer, linetype='CENTER'))
            
            # 绘制第一个箭头
            elements.append(self.canvas.add_line(
                (arrow1_center[0] - arrow_size * dx + arrow_size * nx, 
                 arrow1_center[1] - arrow_size * dy + arrow_size * ny),
                arrow1_center,
                layer=mapped_layer
            ))
            elements.append(self.canvas.add_line(
                (arrow1_center[0] - arrow_size * dx - arrow_size * nx, 
                 arrow1_center[1] - arrow_size * dy - arrow_size * ny),
                arrow1_center,
                layer=mapped_layer
            ))
            
            # 绘制第二个箭头（方向相反）
            elements.append(self.canvas.add_line(
                (arrow2_center[0] + arrow_size * dx + arrow_size * nx, 
                 arrow2_center[1] + arrow_size * dy + arrow_size * ny),
                arrow2_center,
                layer=mapped_layer
            ))
            elements.append(self.canvas.add_line(
                (arrow2_center[0] + arrow_size * dx - arrow_size * nx, 
                 arrow2_center[1] + arrow_size * dy - arrow_size * ny),
                arrow2_center,
                layer=mapped_layer
            ))
            
            # 添加剖面标识 - 在两端
            text_offset = 8
            elements.append(self.canvas.add_text(
                f"{section_label}-{section_label}", 
                (start_point[0] - text_offset * dx, start_point[1] - text_offset * dy),
                height=5,
                layer=mapped_layer
            ))
            
            elements.append(self.canvas.add_text(
                f"{section_label}-{section_label}", 
                (end_point[0] + text_offset * dx, end_point[1] + text_offset * dy),
                height=5,
                layer=mapped_layer
            ))
            
        return elements
    
    def _add_section_view_label(self, position: Tuple[float, float], section_label: str = "A-A", height: float = 5) -> Any:
        """添加剖视图标签"""
        mapped_layer = self._get_layer('TEXT')
        
        # 创建标签文本
        text = f"剖视图 {section_label}"
        
        elements = []
        text_obj = self.canvas.add_text(text, position, height=height, layer=mapped_layer)
        elements.append(text_obj)
        
        # 添加下划线
        x, y = position
        text_length = len(text) * height * 0.6  # 估算文本长度
        underline = self.canvas.add_line(
            (x - text_length/2, y - height*0.8),
            (x + text_length/2, y - height*0.8),
            layer=mapped_layer
        )
        elements.append(underline)
        
        return elements
    
    def _add_detail_view(self, center: Tuple[float, float], radius: float, 
                        detail_label: str = "B", scale: str = "2:1") -> Any:
        """添加局部放大图指示"""
        mapped_layer = self._get_layer('DETAIL')
        
        elements = []
        
        # 绘制圆
        circle = self.canvas.add_circle(center, radius, layer=mapped_layer)
        elements.append(circle)
        
        # 添加放大图标识
        label_text = self.canvas.add_text(detail_label, (center[0], center[1] + radius*1.2), height=5, layer=mapped_layer)
        elements.append(label_text)
        
        # 添加比例文本
        scale_text = self.canvas.add_text(scale, (center[0], center[1] - radius*1.2), height=3.5, layer=mapped_layer)
        elements.append(scale_text)
        
        return elements
    
    def _add_text(self, text: str, position: Tuple[float, float], height: float = 2.5, 
                 layer: str = 'TEXT', style: str = 'chinese', valign: int = 1, halign: int = 1) -> Any:
        """添加文本"""
        x, y = position
        mapped_layer = self._get_layer(layer)
        
        text_obj = self.canvas.add_text(text, position=(x, y), height=height, layer=mapped_layer, 
                                       style=style, valign=valign, halign=halign)
        return text_obj
    
    def validate_params(self, operation: str, **kwargs) -> bool:
        """验证视图处理参数"""
        if not super().validate_params(operation, **kwargs):
            return False
        
        # 针对不同操作类型进行特定验证
        if operation == 'section_line':
            return 'start_point' in kwargs and 'end_point' in kwargs
        elif operation == 'section_view_label':
            return 'position' in kwargs
        elif operation == 'detail_view':
            return 'center' in kwargs and 'radius' in kwargs and kwargs['radius'] > 0
        elif operation == 'text':
            return 'text' in kwargs and 'position' in kwargs
        
        return True 