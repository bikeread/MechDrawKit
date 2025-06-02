import ezdxf
from typing import Any, Tuple, List, Optional, Dict
from ..config.gb_standards import GBStandardConfig


class EzdxfAdapter:
    """ezdxf适配器类
    
    封装ezdxf的ModelSpace操作，自动应用GB标准配置
    """
    
    def __init__(self, msp, doc, config_manager: GBStandardConfig = None):
        """初始化适配器
        
        Args:
            msp: ezdxf模型空间对象
            doc: ezdxf文档对象
            config_manager: 配置管理器对象
        """
        self.msp = msp
        self.doc = doc
        self.config = config_manager or GBStandardConfig()
        
        # 如果提供了文档对象，确保所需的图层和线型存在
        if doc:
            self._setup_document()
    
    def _setup_document(self):
        """设置文档的图层和线型，符合GB标准"""
        # 创建支持中文的字体样式
        if 'chinese' not in self.doc.styles:
            self.doc.styles.new('chinese', dxfattribs={
                'font': 'simsun.ttf',  # 宋体，大多数Windows系统都有
                'bigfont': 'simsun.ttf'  # 必须指定bigfont以支持中文
            })
        
        # 添加GB标准线型
        line_types = self.config.get_all_line_types()
        for linetype_name, line_config in line_types.items():
            if linetype_name not in self.doc.linetypes:
                description = line_config.get('description', '')
                pattern = line_config.get('pattern', [])
                
                if pattern:  # 如果有模式定义
                    self.doc.linetypes.new(linetype_name, dxfattribs={
                        'description': description, 
                        'pattern': pattern
                    })
                else:  # CONTINUOUS线型没有模式
                    self.doc.linetypes.new(linetype_name, dxfattribs={
                        'description': description
                    })
        
        # 添加所有图层并设置正确的线型
        layer_mappings = self.config.get_all_layer_mappings()
        for logical_layer, mapped_name in layer_mappings.items():
            if mapped_name not in self.doc.layers:
                # 默认为白色
                layer_color = 7
                
                # 根据图层名称推断线型
                linetype = 'CONTINUOUS'
                if '中心线' in mapped_name or logical_layer in ['CENTERLINE', 'AXIS']:
                    linetype = 'CENTER'
                elif '虚线' in mapped_name or logical_layer == 'HIDDEN':
                    linetype = 'HIDDEN'
                elif '双点长划线' in mapped_name or logical_layer == 'PHANTOM':
                    linetype = 'PHANTOM'
                elif '边界线' in mapped_name or logical_layer == 'BORDER':
                    linetype = 'BORDER'
                
                # 创建图层
                self.doc.layers.new(name=mapped_name, dxfattribs={
                    'color': layer_color,
                    'linetype': linetype
                })
    
    def add_line(self, start: Tuple[float, float], end: Tuple[float, float], 
                layer: str = None, linetype: str = None, **attrs) -> Any:
        """添加直线"""
        dxfattribs = {'layer': layer} if layer else {}
        if linetype:
            dxfattribs['linetype'] = linetype
        dxfattribs.update(attrs)
        
        return self.msp.add_line(start, end, dxfattribs=dxfattribs)
    
    def add_circle(self, center: Tuple[float, float], radius: float, 
                  layer: str = None, **attrs) -> Any:
        """添加圆形"""
        dxfattribs = {'layer': layer} if layer else {}
        dxfattribs.update(attrs)
        
        return self.msp.add_circle(center, radius, dxfattribs=dxfattribs)
    
    def add_arc(self, center: Tuple[float, float], radius: float, 
               start_angle: float, end_angle: float, layer: str = None, **attrs) -> Any:
        """添加圆弧"""
        dxfattribs = {'layer': layer} if layer else {}
        dxfattribs.update(attrs)
        
        return self.msp.add_arc(
            center=center,
            radius=radius,
            start_angle=start_angle,
            end_angle=end_angle,
            dxfattribs=dxfattribs
        )
    
    def add_ellipse(self, center: Tuple[float, float], major_axis: Tuple[float, float], 
                   ratio: float, start_param: float = 0, end_param: float = 6.283185307, 
                   layer: str = None, **attrs) -> Any:
        """添加椭圆"""
        dxfattribs = {'layer': layer} if layer else {}
        dxfattribs.update(attrs)
        
        return self.msp.add_ellipse(
            center=center,
            major_axis=major_axis,
            ratio=ratio,
            start_param=start_param,
            end_param=end_param,
            dxfattribs=dxfattribs
        )
    
    def add_polyline(self, points: List[Tuple[float, float]], closed: bool = False, 
                    layer: str = None, **attrs) -> Any:
        """添加多段线"""
        dxfattribs = {'layer': layer} if layer else {}
        dxfattribs.update(attrs)
        
        polyline = self.msp.add_polyline2d(points=points, dxfattribs=dxfattribs)
        if closed and len(points) > 2:
            polyline.close()
        return polyline
    
    def add_spline(self, points: List[Tuple[float, float]], degree: int = 3, 
                  layer: str = None, **attrs) -> Any:
        """添加样条曲线"""
        dxfattribs = {'layer': layer} if layer else {}
        dxfattribs.update(attrs)
        
        return self.msp.add_spline(
            control_points=points,
            degree=degree,
            dxfattribs=dxfattribs
        )
    
    def add_hatch(self, points: List[Tuple[float, float]], pattern: str = 'ANSI31', 
                 layer: str = None, scale: float = 1.0, **attrs) -> Any:
        """添加填充区域"""
        dxfattribs = {'layer': layer} if layer else {}
        dxfattribs.update(attrs)
        
        hatch = self.msp.add_hatch(dxfattribs=dxfattribs)
        hatch.set_pattern_fill(pattern, scale=scale)
        hatch.paths.add_polyline_path(points + [points[0]], is_closed=True)
        return hatch
    
    def add_text(self, text: str, position: Tuple[float, float], height: float = 2.5, 
                layer: str = None, style: str = 'chinese', valign: int = 1, 
                halign: int = 1, **attrs) -> Any:
        """添加文本"""
        x, y = position
        dxfattribs = {
            'height': height,
            'layer': layer,
            'style': style,
            'insert': (x, y),
            'halign': halign,
            'valign': valign,
            'align_point': (x, y),
            'rotation': 0
        }
        # 过滤掉None值
        dxfattribs = {k: v for k, v in dxfattribs.items() if v is not None}
        dxfattribs.update(attrs)
        
        return self.msp.add_text(text, dxfattribs=dxfattribs)
    
    def add_linear_dim(self, base: Tuple[float, float], p1: Tuple[float, float], 
                      p2: Tuple[float, float], text: str = None, 
                      dimstyle: str = 'Standard', override: Dict = None, 
                      layer: str = None, **attrs) -> Any:
        """添加线性尺寸标注"""
        dxfattribs = {'layer': layer} if layer else {}
        dxfattribs.update(attrs)
        
        return self.msp.add_linear_dim(
            base=base,
            p1=p1, 
            p2=p2,
            text=text,
            dimstyle=dimstyle,
            override=override or {},
            dxfattribs=dxfattribs
        )
    
    def add_radius_dim(self, center: Tuple[float, float], radius: float, 
                      angle: float, text: str = None, dimstyle: str = 'Standard', 
                      override: Dict = None, layer: str = None, **attrs) -> Any:
        """添加半径尺寸标注"""
        dxfattribs = {'layer': layer} if layer else {}
        dxfattribs.update(attrs)
        
        return self.msp.add_radius_dim(
            center=center,
            radius=radius,
            angle=angle,
            text=text,
            dimstyle=dimstyle,
            override=override or {},
            dxfattribs=dxfattribs
        )
    
    def add_diameter_dim(self, center: Tuple[float, float], radius: float, 
                        angle: float, text: str = None, dimstyle: str = 'Standard', 
                        override: Dict = None, layer: str = None, **attrs) -> Any:
        """添加直径尺寸标注"""
        dxfattribs = {'layer': layer} if layer else {}
        dxfattribs.update(attrs)
        
        return self.msp.add_diameter_dim(
            center=center,
            radius=radius,
            angle=angle,
            text=text,
            dimstyle=dimstyle,
            override=override or {},
            dxfattribs=dxfattribs
        )
    
    def add_angular_dim(self, center: Tuple[float, float], p1: Tuple[float, float], 
                       p2: Tuple[float, float], text: str = None, 
                       dimstyle: str = 'Standard', override: Dict = None, 
                       layer: str = None, **attrs) -> Any:
        """添加角度尺寸标注"""
        dxfattribs = {'layer': layer} if layer else {}
        dxfattribs.update(attrs)
        
        return self.msp.add_angular_dim(
            center=center,
            p1=p1,
            p2=p2,
            text=text,
            dimstyle=dimstyle,
            override=override or {},
            dxfattribs=dxfattribs
        )
    
    def add_aligned_dim(self, p1: Tuple[float, float], p2: Tuple[float, float], 
                       distance: float, text: str = None, dimstyle: str = 'Standard', 
                       override: Dict = None, layer: str = None, **attrs) -> Any:
        """添加对齐尺寸标注"""
        dxfattribs = {'layer': layer} if layer else {}
        dxfattribs.update(attrs)
        
        return self.msp.add_aligned_dim(
            p1=p1,
            p2=p2,
            distance=distance,
            text=text,
            dimstyle=dimstyle,
            override=override or {},
            dxfattribs=dxfattribs
        ) 