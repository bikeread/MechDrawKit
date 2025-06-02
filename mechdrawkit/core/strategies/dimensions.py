import math
from typing import Any, Tuple, List, Optional
from .base import DrawingStrategy


class DimensionDrawer(DrawingStrategy):
    """尺寸标注绘制策略
    
    负责绘制各种类型的尺寸标注，包括线性标注、半径标注、直径标注、角度标注等
    """
    
    def draw(self, operation: str, **kwargs) -> Any:
        """执行尺寸标注绘制操作
        
        Args:
            operation: 操作类型 ('linear', 'radius', 'diameter', 'angular', 'aligned', 'baseline', 'tolerance')
            **kwargs: 操作参数
            
        Returns:
            绘图结果对象
        """
        if not self.validate_params(operation, **kwargs):
            raise ValueError(f"Invalid parameters for operation: {operation}")
        
        if operation == 'linear':
            return self._add_dimension(**kwargs)
        elif operation == 'radius':
            return self._add_radius_dimension(**kwargs)
        elif operation == 'diameter':
            return self._add_diameter_dimension(**kwargs)
        elif operation == 'angular':
            return self._add_angular_dimension(**kwargs)
        elif operation == 'aligned':
            return self._add_aligned_dimension(**kwargs)
        elif operation == 'baseline':
            return self._add_baseline_dimensions(**kwargs)
        elif operation == 'tolerance':
            return self._add_dimension_with_tolerance(**kwargs)
        else:
            raise ValueError(f"Unsupported operation: {operation}")
    
    def _add_dimension(self, p1: Tuple[float, float], p2: Tuple[float, float], distance: float, text: str = None) -> Any:
        """添加直线尺寸标注"""
        mapped_layer = self._get_layer('DIMENSIONS')
        override_dict = {'dimdle': 0.5, 'dimexe': 0.5}
        
        return self.canvas.add_linear_dim(
            base=(min(p1[0], p2[0]), min(p1[1], p2[1]) - distance),
            p1=p1, p2=p2,
            text=text,
            dimstyle='Standard',
            override=override_dict,
            layer=mapped_layer
        )
    
    def _add_radius_dimension(self, center: Tuple[float, float], radius: float, angle: float = 45, text: str = None) -> Any:
        """添加半径尺寸标注"""
        mapped_layer = self._get_layer('DIMENSIONS')
        override_dict = {'dimdle': 0.5, 'dimexe': 0.5}
        angle_rad = self._deg2rad(angle)
        
        return self.canvas.add_radius_dim(
            center=center,
            radius=radius,
            angle=angle_rad,
            text=text,
            dimstyle='Standard',
            override=override_dict,
            layer=mapped_layer
        )
    
    def _add_diameter_dimension(self, center: Tuple[float, float], radius: float, angle: float = 45, text: str = None) -> Any:
        """添加直径尺寸标注"""
        mapped_layer = self._get_layer('DIMENSIONS')
        override_dict = {'dimdle': 0.5, 'dimexe': 0.5}
        angle_rad = self._deg2rad(angle)
        
        return self.canvas.add_diameter_dim(
            center=center,
            radius=radius,
            angle=angle_rad,
            text=text,
            dimstyle='Standard',
            override=override_dict,
            layer=mapped_layer
        )
    
    def _add_angular_dimension(self, center: Tuple[float, float], p1: Tuple[float, float], p2: Tuple[float, float], text: str = None) -> Any:
        """添加角度尺寸标注"""
        mapped_layer = self._get_layer('DIMENSIONS')
        override_dict = {'dimdle': 0.5, 'dimexe': 0.5}
        
        return self.canvas.add_angular_dim(
            center=center,
            p1=p1,
            p2=p2,
            text=text,
            dimstyle='Standard',
            override=override_dict,
            layer=mapped_layer
        )
    
    def _add_aligned_dimension(self, p1: Tuple[float, float], p2: Tuple[float, float], distance: float, text: str = None) -> Any:
        """添加对齐尺寸标注"""
        mapped_layer = self._get_layer('DIMENSIONS')
        override_dict = {'dimdle': 0.5, 'dimexe': 0.5}
        
        return self.canvas.add_aligned_dim(
            p1=p1,
            p2=p2,
            distance=distance,
            text=text,
            dimstyle='Standard',
            override=override_dict,
            layer=mapped_layer
        )
    
    def _add_baseline_dimensions(self, base_point: Tuple[float, float], points: List[Tuple[float, float]], 
                                spacing: float = 10, direction: Tuple[float, float] = (1, 0), text: str = None) -> List[Any]:
        """添加基准尺寸标注"""
        mapped_layer = self._get_layer('DIMENSIONS')
        dims = []
        
        for i, point in enumerate(points):
            dim = self.canvas.add_linear_dim(
                base=base_point,
                p1=base_point,
                p2=point,
                angle=math.atan2(direction[1], direction[0]),
                dimstyle='Standard',
                override={
                    'dimdle': 0.5,
                    'dimexe': 0.5,
                    'dimexo': spacing * i  # 每个尺寸线的偏移量递增
                },
                layer=mapped_layer
            )
            dims.append(dim)
        return dims
    
    def _add_dimension_with_tolerance(self, p1: Tuple[float, float], p2: Tuple[float, float], distance: float,
                                     nominal: float, upper_tol: float, lower_tol: float) -> Any:
        """添加带公差的尺寸标注"""
        mapped_layer = self._get_layer('DIMENSIONS')
        
        # 构建公差文本
        if upper_tol >= 0:
            upper_text = f"+{upper_tol}"
        else:
            upper_text = f"{upper_tol}"
            
        if lower_tol >= 0:
            lower_text = f"+{lower_tol}"
        else:
            lower_text = f"{lower_tol}"
            
        tol_text = f"{nominal}{upper_text}/{lower_text}"
        
        return self.canvas.add_linear_dim(
            base=(min(p1[0], p2[0]), min(p1[1], p2[1]) - distance),
            p1=p1, p2=p2,
            text=tol_text,
            dimstyle='Standard',
            override={'dimdle': 0.5, 'dimexe': 0.5},
            layer=mapped_layer
        )
    
    def _deg2rad(self, degrees: float) -> float:
        """度转弧度"""
        return degrees * math.pi / 180.0
    
    def validate_params(self, operation: str, **kwargs) -> bool:
        """验证尺寸标注参数"""
        if not super().validate_params(operation, **kwargs):
            return False
        
        # 针对不同操作类型进行特定验证
        if operation == 'linear':
            return 'p1' in kwargs and 'p2' in kwargs and 'distance' in kwargs
        elif operation in ['radius', 'diameter']:
            return 'center' in kwargs and 'radius' in kwargs and kwargs['radius'] > 0
        elif operation == 'angular':
            return 'center' in kwargs and 'p1' in kwargs and 'p2' in kwargs
        elif operation == 'aligned':
            return 'p1' in kwargs and 'p2' in kwargs and 'distance' in kwargs
        elif operation == 'baseline':
            return 'base_point' in kwargs and 'points' in kwargs and len(kwargs['points']) > 0
        elif operation == 'tolerance':
            return ('p1' in kwargs and 'p2' in kwargs and 'distance' in kwargs 
                    and 'nominal' in kwargs and 'upper_tol' in kwargs and 'lower_tol' in kwargs)
        
        return True 