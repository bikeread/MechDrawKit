import math
from typing import Any, Tuple, List, Optional
from .base import DrawingStrategy


class SymbolDrawer(DrawingStrategy):
    """工程符号绘制策略
    
    负责绘制表面粗糙度、几何公差、焊接符号等工程技术符号
    """
    
    def draw(self, operation: str, **kwargs) -> Any:
        """执行工程符号绘制操作
        
        Args:
            operation: 操作类型 ('roughness', 'advanced_surface_finish', 'geometric_tolerance', 'welding_symbol', 'leader_arrow')
            **kwargs: 操作参数
            
        Returns:
            绘图结果对象
        """
        if not self.validate_params(operation, **kwargs):
            raise ValueError(f"Invalid parameters for operation: {operation}")
        
        if operation == 'roughness':
            return self._add_roughness(**kwargs)
        elif operation == 'advanced_surface_finish':
            return self._add_advanced_surface_finish(**kwargs)
        elif operation == 'geometric_tolerance':
            return self._add_geometric_tolerance(**kwargs)
        elif operation == 'welding_symbol':
            return self._add_welding_symbol(**kwargs)
        elif operation == 'leader_arrow':
            return self._add_leader_arrow(**kwargs)
        else:
            raise ValueError(f"Unsupported operation: {operation}")
    
    def _add_roughness(self, position: Tuple[float, float], roughness_value: str, height: float = 3) -> Any:
        """添加表面粗糙度标注"""
        x, y = position
        mapped_layer = self._get_layer('DIMENSIONS')
        
        # 绘制粗糙度符号
        # 竖线
        line1 = self.canvas.add_line((x, y), (x, y + 6), layer=mapped_layer)
        # 斜线
        line2 = self.canvas.add_line((x, y + 6), (x + 4, y + 10), layer=mapped_layer)
        # 水平线
        line3 = self.canvas.add_line((x + 4, y + 10), (x + 10, y + 10), layer=mapped_layer)
        
        # 添加粗糙度值
        text_layer = self._get_layer('TEXT')
        text = self.canvas.add_text(f"Ra{roughness_value}", (x + 15, y + 10), height=height, layer=text_layer)
        
        return [line1, line2, line3, text]
    
    def _add_advanced_surface_finish(self, position: Tuple[float, float], ra_value: str, 
                                   machining_method: str = None, waviness: str = None, 
                                   lay: str = None, cutoff: str = None, height: float = 2.5) -> Any:
        """添加高级表面粗糙度标注 (符合GB/T 131 标准)"""
        x, y = position
        mapped_layer = self._get_layer('SURFACE_FINISH')
        
        # 符号大小
        sym_height = 10
        sym_width = 10
        
        # 基本符号 - 符合GB/T 131标准的粗糙度符号
        lines = []
        # 竖线
        lines.append(self.canvas.add_line((x, y), (x, y + sym_height * 0.6), layer=mapped_layer))
        # 斜线
        lines.append(self.canvas.add_line((x, y + sym_height * 0.6), (x + sym_width * 0.4, y + sym_height), layer=mapped_layer))
        # 水平线
        lines.append(self.canvas.add_line((x + sym_width * 0.4, y + sym_height), (x + sym_width, y + sym_height), layer=mapped_layer))
        
        # 绘制加工方法指示（顶部水平线）
        if machining_method:
            # 上方水平线
            lines.append(self.canvas.add_line((x, y + sym_height * 0.6), (x + sym_width, y + sym_height * 0.6), layer=mapped_layer))
            # 加工方法文字
            lines.append(self.canvas.add_text(machining_method, (x + sym_width * 0.5, y + sym_height * 0.8), height=height, layer=mapped_layer))
        
        # 添加主要的Ra值
        ra_text = f"Ra{ra_value}"
        text_x = x + sym_width * 1.2
        text_y = y + sym_height * 0.5
        lines.append(self.canvas.add_text(ra_text, (text_x, text_y), height=height, layer=mapped_layer))
        
        # 添加额外参数
        extra_info = []
        if waviness:
            extra_info.append(f"W{waviness}")
        if lay:
            extra_info.append(f"Lay {lay}")
        if cutoff:
            extra_info.append(f"λc {cutoff}")
        
        if extra_info:
            extra_text = ", ".join(extra_info)
            lines.append(self.canvas.add_text(extra_text, (text_x, y + sym_height * 0.2), height=height*0.8, layer=mapped_layer))
        
        return lines
    
    def _add_geometric_tolerance(self, position: Tuple[float, float], symbol: str, tolerance: str, 
                               datum: str = None, height: float = 2.5) -> Any:
        """添加几何公差框"""
        x, y = position
        mapped_layer = self._get_layer('TOLERANCE')
        
        # 绘制公差框
        box_width = 14
        box_height = 7
        
        lines = []
        # 框框矩形
        lines.append(self.canvas.add_line((x, y), (x + box_width, y), layer=mapped_layer))
        lines.append(self.canvas.add_line((x + box_width, y), (x + box_width, y + box_height), layer=mapped_layer))
        lines.append(self.canvas.add_line((x + box_width, y + box_height), (x, y + box_height), layer=mapped_layer))
        lines.append(self.canvas.add_line((x, y + box_height), (x, y), layer=mapped_layer))
        
        # 如果有基准，添加基准框
        if datum:
            lines.append(self.canvas.add_line((x + box_width, y), (x + box_width + 7, y), layer=mapped_layer))
            lines.append(self.canvas.add_line((x + box_width + 7, y), (x + box_width + 7, y + box_height), layer=mapped_layer))
            lines.append(self.canvas.add_line((x + box_width + 7, y + box_height), (x + box_width, y + box_height), layer=mapped_layer))
            
            # 添加基准文字
            lines.append(self.canvas.add_text(datum, (x + box_width + 3.5, y + box_height/2), height=height, layer=mapped_layer))
        
        # 特征符号和公差值
        lines.append(self.canvas.add_text(symbol, (x + 3, y + box_height/2), height=height, layer=mapped_layer))
        lines.append(self.canvas.add_text(str(tolerance), (x + 10, y + box_height/2), height=height, layer=mapped_layer))
        
        return lines
    
    def _add_welding_symbol(self, position: Tuple[float, float], weld_type: str, size: str = None, 
                           length: str = None, process: str = None, finish: str = None, 
                           field: bool = False, height: float = 2.5) -> Any:
        """添加焊接符号"""
        x, y = position
        mapped_layer = self._get_layer('WELD_SYMBOL')
        
        # 符号基本尺寸
        sym_length = 30
        
        elements = []
        # 主引出线
        elements.append(self.canvas.add_line((x, y), (x + sym_length, y), layer=mapped_layer))
        
        # 箭头
        arrow_size = 3
        elements.append(self.canvas.add_line((x, y), (x + arrow_size, y + arrow_size), layer=mapped_layer))
        elements.append(self.canvas.add_line((x, y), (x + arrow_size, y - arrow_size), layer=mapped_layer))
        
        # 如果是现场焊接，添加标记
        flag_height = 5
        if field:
            elements.append(self.canvas.add_line((x + sym_length * 0.8, y), (x + sym_length * 0.8, y + flag_height), layer=mapped_layer))
            elements.append(self.canvas.add_circle((x + sym_length * 0.8, y + flag_height + 1), 1, layer=mapped_layer))
        
        # 焊接符号位置
        sym_x = x + sym_length * 0.5
        sym_y = y + 3  # 放在基线上方
        
        # 添加焊接类型符号
        elements.append(self.canvas.add_text(weld_type, (sym_x, sym_y), height=height, layer=mapped_layer))
        
        # 添加尺寸信息（如有）
        info_text = ""
        if size:
            info_text += f"{size}"
        if length:
            if info_text:
                info_text += "-"
            info_text += f"{length}"
        
        if info_text:
            elements.append(self.canvas.add_text(info_text, (sym_x, y - 3), height=height, layer=mapped_layer))
        
        # 添加工艺信息（如有）
        if process or finish:
            proc_text = ""
            if process:
                proc_text += f"{process}"
            if finish:
                if proc_text:
                    proc_text += ", "
                proc_text += f"{finish}"
            
            elements.append(self.canvas.add_text(proc_text, (x + sym_length * 0.5, y - 6), height=height * 0.8, layer=mapped_layer))
        
        return elements
    
    def _add_leader_arrow(self, start_point: Tuple[float, float], end_point: Tuple[float, float], text: str) -> Any:
        """添加引出线和文本标注"""
        mapped_dimensions_layer = self._get_layer('DIMENSIONS')
        mapped_text_layer = self._get_layer('TEXT')
        
        # 计算箭头方向向量，用于延长引出线
        dx = end_point[0] - start_point[0]
        dy = end_point[1] - start_point[1]
        
        height = 3.5
        
        # 计算距离
        dist = math.sqrt(dx*dx + dy*dy)
        
        # 规范化向量
        if dist > 0:
            dx = dx / dist
            dy = dy / dist
        
        # 延长引出线 - 在start_point方向延长20%
        extension_factor = 0.2
        extended_start_x = start_point[0] - dx * dist * extension_factor
        extended_start_y = start_point[1] - dy * dist * extension_factor
        extended_start = (extended_start_x, extended_start_y)
        
        elements = []
        # 创建延长的引出线
        elements.append(self.canvas.add_line(end_point, extended_start, layer=mapped_dimensions_layer))
        
        # 检查原始引出线是否已经是水平的
        is_horizontal = abs(dy) < 0.05  # 如果y方向差异很小，认为是水平线
        
        if not is_horizontal:
            # 修改后的引线实现 - 添加更长的水平线段以延伸到视图外部
            horizontal_length = 10  # 足够长的水平线段
            
            # 计算end_point到start_point的方向
            view_direction_x = start_point[0] - end_point[0]
            
            # 确定水平线段的方向（向左或向右）
            if abs(view_direction_x) > 10:  # 有明显的水平偏移
                horiz_direction = 1 if view_direction_x > 0 else -1
            else:
                # 如果引出线几乎垂直，则根据大概的视图位置判断
                horiz_direction = -1 if dx > 0 else 1
            
            # 水平线段的终点
            horiz_end_x = extended_start_x + horizontal_length * horiz_direction
            horiz_end_y = extended_start_y
            horiz_end = (horiz_end_x, horiz_end_y)
            
            # 添加水平线段
            elements.append(self.canvas.add_line(extended_start, horiz_end, layer=mapped_dimensions_layer))
            
            # 文本位置在水平线段的终点附近
            text_offset = 5  # 文本偏移量
            text_point = (horiz_end_x + text_offset * horiz_direction, horiz_end_y)
        else:
            # 对于已经是水平线的情况，只需要在现有线段的基础上延长
            horiz_direction = 1 if start_point[0] < end_point[0] else -1
            
            # 额外的延长长度
            extra_length = 1  # 固定延长长度
            
            # 计算延长后的终点
            horiz_end_x = extended_start_x + extra_length * horiz_direction
            horiz_end_y = extended_start_y
            horiz_end = (horiz_end_x, horiz_end_y)
            
            # 添加延长的水平线段
            elements.append(self.canvas.add_line(extended_start, horiz_end, layer=mapped_dimensions_layer))
            
            # 文本位置在延长线的终点附近
            text_offset = 5  # 文本偏移量
            text_point = (horiz_end_x + text_offset * horiz_direction, horiz_end_y)
        
        # 添加文本
        elements.append(self.canvas.add_text(text, text_point, height=height, layer=mapped_text_layer, 
                                           halign=1, valign=2))
        
        return elements
    
    def validate_params(self, operation: str, **kwargs) -> bool:
        """验证工程符号参数"""
        if not super().validate_params(operation, **kwargs):
            return False
        
        # 针对不同操作类型进行特定验证
        if operation == 'roughness':
            return 'position' in kwargs and 'roughness_value' in kwargs
        elif operation == 'advanced_surface_finish':
            return 'position' in kwargs and 'ra_value' in kwargs
        elif operation == 'geometric_tolerance':
            return 'position' in kwargs and 'symbol' in kwargs and 'tolerance' in kwargs
        elif operation == 'welding_symbol':
            return 'position' in kwargs and 'weld_type' in kwargs
        elif operation == 'leader_arrow':
            return 'start_point' in kwargs and 'end_point' in kwargs and 'text' in kwargs
        
        return True 