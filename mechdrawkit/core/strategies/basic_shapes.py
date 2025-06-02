from typing import Any, Tuple, List, Optional
from .base import DrawingStrategy


class BasicShapeDrawer(DrawingStrategy):
    """基础图形绘制策略
    
    负责绘制圆形、矩形、直线、多段线、圆弧、椭圆、样条曲线等基础几何图形
    """
    
    def draw(self, operation: str, **kwargs) -> Any:
        """执行基础图形绘制操作
        
        Args:
            operation: 操作类型 ('circle', 'rectangle', 'line', 'polyline', 'arc', 'ellipse', 'spline')
            **kwargs: 操作参数
            
        Returns:
            绘图结果对象
        """
        if not self.validate_params(operation, **kwargs):
            raise ValueError(f"Invalid parameters for operation: {operation}")
        
        if operation == 'circle':
            return self._draw_circle(**kwargs)
        elif operation == 'rectangle':
            return self._draw_rectangle(**kwargs)
        elif operation == 'line':
            return self._draw_line(**kwargs)
        elif operation == 'centerline':
            return self._draw_centerline(**kwargs)
        elif operation == 'hiddenline':
            return self._draw_hiddenline(**kwargs)
        elif operation == 'phantomline':
            return self._draw_phantomline(**kwargs)
        elif operation == 'borderline':
            return self._draw_borderline(**kwargs)
        elif operation == 'polyline':
            return self._draw_polyline(**kwargs)
        elif operation == 'arc':
            return self._draw_arc(**kwargs)
        elif operation == 'ellipse':
            return self._draw_ellipse(**kwargs)
        elif operation == 'spline':
            return self._draw_spline(**kwargs)
        elif operation == 'hatch':
            return self._draw_hatch(**kwargs)
        else:
            raise ValueError(f"Unsupported operation: {operation}")
    
    def _draw_circle(self, center: Tuple[float, float], radius: float, layer: str = 'PARTS') -> Any:
        """绘制圆形"""
        mapped_layer = self._get_layer(layer)
        return self.canvas.add_circle(center, radius, layer=mapped_layer)
    
    def _draw_rectangle(self, lower_left: Tuple[float, float], width: float, height: float, layer: str = 'PARTS') -> Any:
        """绘制矩形"""
        x, y = lower_left
        mapped_layer = self._get_layer(layer)
        
        # 绘制四条边线
        lines = []
        lines.append(self.canvas.add_line((x, y), (x + width, y), layer=mapped_layer))
        lines.append(self.canvas.add_line((x + width, y), (x + width, y + height), layer=mapped_layer))
        lines.append(self.canvas.add_line((x + width, y + height), (x, y + height), layer=mapped_layer))
        lines.append(self.canvas.add_line((x, y + height), (x, y), layer=mapped_layer))
        
        return lines
    
    def _draw_line(self, start: Tuple[float, float], end: Tuple[float, float], layer: str = 'VISIBLE') -> Any:
        """绘制直线"""
        mapped_layer = self._get_layer(layer)
        return self.canvas.add_line(start, end, layer=mapped_layer)
    
    def _draw_centerline(self, start: Tuple[float, float], end: Tuple[float, float]) -> Any:
        """绘制中心线"""
        mapped_layer = self._get_layer('CENTERLINE')
        return self.canvas.add_line(start, end, layer=mapped_layer, linetype='CENTER')
    
    def _draw_hiddenline(self, start: Tuple[float, float], end: Tuple[float, float]) -> Any:
        """绘制隐藏线"""
        mapped_layer = self._get_layer('HIDDEN')
        return self.canvas.add_line(start, end, layer=mapped_layer, linetype='HIDDEN')
    
    def _draw_phantomline(self, start: Tuple[float, float], end: Tuple[float, float]) -> Any:
        """绘制幻影线/双点长划线"""
        mapped_layer = self._get_layer('PHANTOM')
        return self.canvas.add_line(start, end, layer=mapped_layer, linetype='PHANTOM')
    
    def _draw_borderline(self, start: Tuple[float, float], end: Tuple[float, float]) -> Any:
        """绘制边界线"""
        mapped_layer = self._get_layer('BORDER')
        return self.canvas.add_line(start, end, layer=mapped_layer, linetype='BORDER')
    
    def _draw_polyline(self, points: List[Tuple[float, float]], closed: bool = False, layer: str = 'PARTS') -> Any:
        """绘制多段线"""
        mapped_layer = self._get_layer(layer)
        return self.canvas.add_polyline(points, closed=closed, layer=mapped_layer)
    
    def _draw_arc(self, center: Tuple[float, float], radius: float, start_angle: float, end_angle: float, layer: str = 'PARTS') -> Any:
        """绘制圆弧"""
        mapped_layer = self._get_layer(layer)
        return self.canvas.add_arc(center, radius, start_angle, end_angle, layer=mapped_layer)
    
    def _draw_ellipse(self, center: Tuple[float, float], major_axis: Tuple[float, float], ratio: float,
                      start_param: float = 0, end_param: float = 6.283185307, layer: str = 'PARTS') -> Any:
        """绘制椭圆"""
        mapped_layer = self._get_layer(layer)
        return self.canvas.add_ellipse(center, major_axis, ratio, start_param, end_param, layer=mapped_layer)
    
    def _draw_spline(self, points: List[Tuple[float, float]], degree: int = 3, layer: str = 'PARTS') -> Any:
        """绘制样条曲线"""
        mapped_layer = self._get_layer(layer)
        return self.canvas.add_spline(points, degree=degree, layer=mapped_layer)
    
    def _draw_hatch(self, points: List[Tuple[float, float]], pattern: str = 'ANSI31', layer: str = 'HATCH', scale: float = 1.0) -> Any:
        """绘制填充区域"""
        mapped_layer = self._get_layer(layer)
        return self.canvas.add_hatch(points, pattern=pattern, layer=mapped_layer, scale=scale)
    
    def validate_params(self, operation: str, **kwargs) -> bool:
        """验证基础图形参数"""
        if not super().validate_params(operation, **kwargs):
            return False
        
        # 针对不同操作类型进行特定验证
        if operation == 'circle':
            return 'center' in kwargs and 'radius' in kwargs and kwargs['radius'] > 0
        elif operation == 'rectangle':
            return ('lower_left' in kwargs and 'width' in kwargs and 'height' in kwargs 
                    and kwargs['width'] > 0 and kwargs['height'] > 0)
        elif operation in ['line', 'centerline', 'hiddenline', 'phantomline', 'borderline']:
            return 'start' in kwargs and 'end' in kwargs
        elif operation == 'polyline':
            return 'points' in kwargs and len(kwargs['points']) >= 2
        elif operation == 'arc':
            return ('center' in kwargs and 'radius' in kwargs and 'start_angle' in kwargs 
                    and 'end_angle' in kwargs and kwargs['radius'] > 0)
        elif operation == 'ellipse':
            return 'center' in kwargs and 'major_axis' in kwargs and 'ratio' in kwargs
        elif operation == 'spline':
            return 'points' in kwargs and len(kwargs['points']) >= 2
        elif operation == 'hatch':
            return 'points' in kwargs and len(kwargs['points']) >= 3
        
        return True 