import os
import sys
import ezdxf
import math
from mechdrawkit.tools.table_methods import update_title_block
from mechdrawkit.core.factory import ComponentFactory
from mechdrawkit.core.adapters import EzdxfAdapter
from mechdrawkit.config.gb_standards import GBStandardConfig

# 确保当前目录在系统路径中
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

def find_project_root(start_path=None):
    """
    查找项目根目录，通过检查标识文件来确定
    
    Args:
        start_path: 开始查找的路径，默认为当前文件所在目录
    
    Returns:
        str: 项目根目录的绝对路径
    """
    if start_path is None:
        start_path = os.path.dirname(os.path.abspath(__file__))
    
    # 项目根目录的标识文件
    root_indicators = [
        'setup.py',
        'pyproject.toml', 
        'requirements.txt',
        'Makefile',
        'mechdrawkit'  # 包目录
    ]
    
    current_path = start_path
    while True:
        # 检查当前目录是否包含任何标识文件
        for indicator in root_indicators:
            indicator_path = os.path.join(current_path, indicator)
            if os.path.exists(indicator_path):
                return current_path
        
        # 移动到父目录
        parent_path = os.path.dirname(current_path)
        
        # 如果已经到达根目录（Unix: '/', Windows: 'C:\'等）
        if parent_path == current_path:
            # 没找到项目根目录，返回原始目录
            return start_path
        
        current_path = parent_path

# 获取项目根目录
PROJECT_ROOT = find_project_root()

# GB/T 4457.4-2002 技术制图 线型
# GB/T 14689-2008 机械制图 图样画法视图表示法
# GB/T 4458.4-2003 技术制图 比例
# GB/T 4456-2020 技术制图 字体

# 绘图工具类 - 重构版本，保持原有接口完全兼容
class RiceMillDrawingTools:
    """绘图工具类，提供所有基础绘图操作，符合GB标准
    
    重构版本：内部使用策略模式和工厂模式，保持原有接口完全不变
    """
    
    # 保持原有常量定义以确保向后兼容性
    # GB标准线型定义
    LINE_TYPES = {
        'CONTINUOUS': ('连续线', []),
        'CENTER': ('中心线', [7.5, 5.0, -1.25, 0.0]),
        'HIDDEN': ('虚线', [1.25, -1.25]),
        'PHANTOM': ('双点长划线', [12.0, -3.0, 0.5, -3.0, 0.5, -3.0]),
        'DASHDOT': ('点划线', [5.0, -2.0, 0.0, -2.0]),
        'BORDER': ('边界线', [6.0, -2.0, 1.5, -2.0]),
        'DIVIDE': ('分界线', [1.0, -1.0]),
    }
    
    # GB标准线宽定义 (mm)
    LINE_WEIGHTS = {
        'THIN': 0.25,     # 细线
        'MEDIUM': 0.5,    # 中等线
        'THICK': 0.7,     # 粗线
        'EXTRA_THICK': 1.0  # 特粗线
    }
    
    # 图层映射字典 - 静态类属性，所有实例共享
    LAYER_MAPPING = {
        # 基本图层
        'CENTERLINE': '4中心线',        # 中心线使用标准中心线样式
        'HIDDEN': '5虚线',              # 隐藏线使用标准虚线样式
        'DIMENSIONS': '1细实线',        # 尺寸线使用细实线
        'TEXT': '3文字',                # 文字图层专用
        'PARTS': '6外框',               # 零件轮廓使用外框图层
        'HATCH': '3剖面线',             # 剖面图案使用专用图层
        'VISIBLE': '1细实线',           # 可见线使用细实线
        'DETAIL': '2粗实线',            # 局部放大图使用粗实线
        'ANNOTATION': '3文字',          # 注释使用文字图层
        'TABLE': '2粗实线',             # 表格线使用粗实线
        
        # GB标准扩展图层
        'AXIS': '4中心线',              # 轴线
        'SECTION': '2粗实线',           # 剖面线
        'PHANTOM': '7双点长划线',        # 虚想线/双点长划线
        'BORDER': '8边界线',            # 边界线
        'CUTTING_PLANE': '4中心线',     # 剖切平面线
        'TOLERANCE': '3文字',           # 公差标注
        'SURFACE_FINISH': '3文字',      # 表面处理
        'WELD_SYMBOL': '3文字',         # 焊接符号
        'AUXILIARY': '9辅助线',         # 辅助线
        'COORDINATE': '10坐标线',       # 坐标线
        'TITLE_BLOCK': '2粗实线',       # 标题栏
    }
    
    # GB标准文字高度 (mm)
    TEXT_HEIGHTS = {
        'TITLE': 5.0,     # 标题
        'SUBTITLE': 3.5,  # 副标题
        'NORMAL': 2.5,    # 常规文字
        'SMALL': 1.8,     # 小文字
        'TINY': 1.4       # 微小文字
    }
    
    # 图纸比例
    SCALES = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
    
    # GB标准箭头尺寸 (mm)
    ARROW_SIZE = 3.0
    
    # GB标准字体
    FONT_STYLE = 'chinese'
    
    def __init__(self, msp, doc=None):
        """初始化绘图工具
        
        Args:
            msp: 模型空间对象
            doc: DXF文档对象，用于创建图层等
        """
        self.msp = msp
        self.doc = doc
        
        # 初始化新架构组件
        self.config = GBStandardConfig()
        self.canvas = EzdxfAdapter(msp, doc, self.config)
        
        # 创建策略组件
        self.basic_shapes = ComponentFactory.create_strategy('basic_shapes', self.canvas, self.config)
        self.dimensions = ComponentFactory.create_strategy('dimensions', self.canvas, self.config)
        self.symbols = ComponentFactory.create_strategy('symbols', self.canvas, self.config)
        self.views = ComponentFactory.create_strategy('views', self.canvas, self.config)
        
        # 如果提供了文档对象，确保所需的图层和线型存在（保持原有逻辑）
        if doc:
            self._setup_document(doc)
    
    def _setup_document(self, doc):
        """设置文档的图层和线型，符合GB标准"""
        # 委托给适配器处理，它已经包含了原有的所有逻辑
        pass  # EzdxfAdapter已经在初始化时处理了文档设置
    
    # 工具函数 - 角度转换
    def deg2rad(self, degrees):
        """度转弧度"""
        return degrees * math.pi / 180.0
    
    # 绘制中心线
    def draw_centerline(self, start, end):
        """绘制中心线"""
        return self.basic_shapes.draw('centerline', start=start, end=end)
    
    # 绘制隐藏线
    def draw_hiddenline(self, start, end):
        """绘制隐藏线"""
        return self.basic_shapes.draw('hiddenline', start=start, end=end)
    
    # 绘制可见线
    def draw_visibleline(self, start, end, layer='VISIBLE'):
        """绘制可见线"""
        return self.basic_shapes.draw('line', start=start, end=end, layer=layer)
    
    # 绘制幻影线/双点长划线
    def draw_phantomline(self, start, end):
        """绘制幻影线/双点长划线"""
        return self.basic_shapes.draw('phantomline', start=start, end=end)
    
    # 绘制边界线
    def draw_borderline(self, start, end):
        """绘制边界线"""
        return self.basic_shapes.draw('borderline', start=start, end=end)
    
    # 绘制圆
    def draw_circle(self, center, radius, layer='PARTS'):
        """绘制圆"""
        return self.basic_shapes.draw('circle', center=center, radius=radius, layer=layer)
    
    # 绘制圆弧
    def draw_arc(self, center, radius, start_angle, end_angle, layer='PARTS'):
        """绘制圆弧
        
        Args:
            center: 圆心坐标 (x, y)
            radius: 半径
            start_angle: 起始角度 (度)
            end_angle: 结束角度 (度)
            layer: 图层名称
        """
        return self.basic_shapes.draw('arc', center=center, radius=radius, 
                                     start_angle=start_angle, end_angle=end_angle, layer=layer)
    
    # 绘制椭圆
    def draw_ellipse(self, center, major_axis, ratio, start_param=0, end_param=6.283185307, layer='PARTS'):
        """绘制椭圆
        
        Args:
            center: 中心点 (x, y)
            major_axis: 长轴向量 (x, y)
            ratio: 短轴与长轴的比例
            start_param: 起始参数角
            end_param: 结束参数角
            layer: 图层名称
        """
        return self.basic_shapes.draw('ellipse', center=center, major_axis=major_axis, ratio=ratio,
                                     start_param=start_param, end_param=end_param, layer=layer)
    
    # 绘制多段线
    def draw_polyline(self, points, closed=False, layer='PARTS'):
        """绘制多段线
        
        Args:
            points: 点列表 [(x1, y1), (x2, y2), ...]
            closed: 是否闭合
            layer: 图层名称
        """
        return self.basic_shapes.draw('polyline', points=points, closed=closed, layer=layer)
    
    # 绘制样条曲线
    def draw_spline(self, points, degree=3, layer='PARTS'):
        """绘制样条曲线
        
        Args:
            points: 控制点列表 [(x1, y1), (x2, y2), ...]
            degree: 样条曲线阶数
            layer: 图层名称
        """
        return self.basic_shapes.draw('spline', points=points, degree=degree, layer=layer)
    
    # 绘制文本
    def add_text(self, text, position, height=2.5, layer='TEXT', style='chinese', valign=1, halign=1):
        """添加文本"""
        return self.views.draw('text', text=text, position=position, height=height, 
                              layer=layer, style=style, valign=valign, halign=halign)
    
    # 添加尺寸标注
    def add_dimension(self, p1, p2, distance, text=None):
        """添加直线尺寸标注"""
        return self.dimensions.draw('linear', p1=p1, p2=p2, distance=distance, text=text)
    
    # 添加半径标注
    def add_radius_dimension(self, center, radius, angle=45, text=None):
        """添加半径尺寸标注"""
        return self.dimensions.draw('radius', center=center, radius=radius, angle=angle, text=text)
    
    # 添加直径标注
    def add_diameter_dimension(self, center, radius, angle=45, text=None):
        """添加直径尺寸标注"""
        return self.dimensions.draw('diameter', center=center, radius=radius, angle=angle, text=text)
    
    # 添加角度标注
    def add_angular_dimension(self, center, p1, p2, text=None):
        """添加角度尺寸标注
        
        Args:
            center: 角的顶点
            p1: 第一条边上的点
            p2: 第二条边上的点
            text: 自定义标注文本
        """
        return self.dimensions.draw('angular', center=center, p1=p1, p2=p2, text=text)
    
    # 添加对齐标注
    def add_aligned_dimension(self, p1, p2, distance, text=None):
        """添加对齐尺寸标注
        
        Args:
            p1: 第一个点
            p2: 第二个点
            distance: 标注线与被标注线的距离
            text: 自定义标注文本
        """
        return self.dimensions.draw('aligned', p1=p1, p2=p2, distance=distance, text=text)
    
    # 添加基准尺寸
    def add_baseline_dimensions(self, base_point, points, spacing=10, direction=(1, 0), text=None):
        """添加基准尺寸标注
        
        Args:
            base_point: 基准点
            points: 要标注的点列表
            spacing: 尺寸线间距
            direction: 标注方向向量
            text: 自定义标注文本
        """
        return self.dimensions.draw('baseline', base_point=base_point, points=points, 
                                   spacing=spacing, direction=direction, text=text)
    
    # 添加尺寸公差
    def add_dimension_with_tolerance(self, p1, p2, distance, nominal, upper_tol, lower_tol):
        """添加带公差的尺寸标注
        
        Args:
            p1: 第一个点
            p2: 第二个点
            distance: 标注线与被标注线的距离
            nominal: 名义尺寸
            upper_tol: 上公差
            lower_tol: 下公差
        """
        return self.dimensions.draw('tolerance', p1=p1, p2=p2, distance=distance,
                                   nominal=nominal, upper_tol=upper_tol, lower_tol=lower_tol)
    
    # 添加几何公差框
    def add_geometric_tolerance(self, position, symbol, tolerance, datum=None, height=2.5):
        """添加几何公差框
        
        Args:
            position: 放置位置
            symbol: 几何特征符号（如 'Ø' 表示圆度，'⊥' 表示垂直度等）
            tolerance: 公差值
            datum: 基准（如 'A'、'B'）
            height: 文字高度
        """
        return self.symbols.draw('geometric_tolerance', position=position, symbol=symbol, 
                                tolerance=tolerance, datum=datum, height=height)
    
    # 绘制矩形
    def draw_rectangle(self, lower_left, width, height, layer='PARTS'):
        """绘制矩形"""
        return self.basic_shapes.draw('rectangle', lower_left=lower_left, width=width, height=height, layer=layer)
    
    # 绘制填充区域
    def draw_hatch(self, points, pattern='ANSI31', layer='HATCH', scale=1.0):
        """添加填充区域"""
        return self.basic_shapes.draw('hatch', points=points, pattern=pattern, layer=layer, scale=scale)
    
    def _add_standard_leader(self, drawing_tools, target_point, text_point, text, scale):
        """添加标准引线标注
        
        Args:
            drawing_tools: 绘图工具对象
            target_point: 指向的目标点
            text_point: 文本位置点
            text: 标注文本
            scale: 比例因子
        """
        # 委托给符号绘制策略
        return self.symbols.draw('leader_arrow', start_point=target_point, end_point=text_point, text=text)
    
    # 添加箭头线指向零件
    def add_leader_arrow(self, start_point, end_point, text):
        """添加引出线和文本标注"""
        return self.symbols.draw('leader_arrow', start_point=start_point, end_point=end_point, text=text)
    
    # 添加表面粗糙度标注
    def add_roughness(self, position, roughness_value, height=3):
        """添加表面粗糙度标注"""
        return self.symbols.draw('roughness', position=position, roughness_value=roughness_value, height=height)
    
    # 添加高级表面粗糙度标注 (符合GB/T 131 标准)
    def add_advanced_surface_finish(self, position, ra_value, machining_method=None, 
                                  waviness=None, lay=None, cutoff=None, height=2.5):
        """添加高级表面粗糙度标注
        
        Args:
            position: 放置位置 (x, y)
            ra_value: Ra值，如 '3.2'
            machining_method: 加工方法，如 '车削'
            waviness: 波度值
            lay: 加工方向符号, =表示平行，X表示交叉，M表示多方向
            cutoff: 采样长度，如 '0.8'
            height: 文字高度
        """
        return self.symbols.draw('advanced_surface_finish', position=position, ra_value=ra_value,
                                machining_method=machining_method, waviness=waviness, 
                                lay=lay, cutoff=cutoff, height=height)
    
    # 添加焊接符号
    def add_welding_symbol(self, position, weld_type, size=None, length=None, 
                          process=None, finish=None, field=False, height=2.5):
        """添加焊接符号
        
        Args:
            position: 放置位置 (x, y)
            weld_type: 焊接类型，如 'V', '工', 'X', '人'
            size: 焊接尺寸
            length: 焊接长度
            process: 焊接工艺
            finish: 表面处理
            field: 是否现场焊接
            height: 文字高度
        """
        return self.symbols.draw('welding_symbol', position=position, weld_type=weld_type,
                                size=size, length=length, process=process, finish=finish,
                                field=field, height=height)
    
    # 添加剖面指示线
    def add_section_line(self, start_point, end_point, section_label="A", arrow_size=3):
        """添加剖面指示线
        
        Args:
            start_point: 起始点 (x, y)
            end_point: 终点 (x, y)
            section_label: 剖面标识，如 'A', 'B' 等
            arrow_size: 箭头大小
        """
        return self.views.draw('section_line', start_point=start_point, end_point=end_point,
                              section_label=section_label, arrow_size=arrow_size)
    
    # 添加剖视图标签
    def add_section_view_label(self, position, section_label="A-A", height=5):
        """添加剖视图标签
        
        Args:
            position: 放置位置 (x, y)
            section_label: 剖面标识，如 'A-A', 'B-B' 等
            height: 文字高度
        """
        return self.views.draw('section_view_label', position=position, 
                              section_label=section_label, height=height)
    
    # 添加局部放大图
    def add_detail_view(self, center, radius, detail_label="B", scale="2:1"):
        """添加局部放大图指示
        
        Args:
            center: 圆心位置 (x, y)
            radius: 圆半径
            detail_label: 放大图标识，如 'A', 'B' 等
            scale: 放大比例，如 '2:1'
        """
        return self.views.draw('detail_view', center=center, radius=radius,
                              detail_label=detail_label, scale=scale)

def generate_part_drawing(part_name, draw_func, title_info, origin=None, scale_factor=0.5, template_path=None, output_dir=None, paper_size='A3', add_views=None):
    """
    通用零件图生成函数，可以从任何零件特定脚本调用，符合GB标准
    
    参数:
        part_name (str): 零件名称，用于命名输出文件
        draw_func (callable): 绘制零件的函数，接受drawing_tools、origin和scale参数
        title_info (dict): 标题栏信息字典
        origin (tuple, optional): 绘图原点坐标，默认为None (将使用图纸中心点)
        scale_factor (float, optional): 缩放因子，默认为0.5
        template_path (str, optional): 模板文件路径，默认为None (将使用标准模板路径)
        output_dir (str, optional): 输出目录路径，默认为None (将使用标准输出目录)
        paper_size (str, optional): 图纸大小，如 'A4', 'A3', 'A2', 'A1', 'A0'
        add_views (list, optional): 要添加的附加视图列表，格式为 [{'type': 'section', 'label': 'A-A', 'position': (x,y), ...}, ...]
    
    返回:
        str: 生成的DXF文件路径
    """
    # 定义纸张尺寸（mm）
    paper_sizes = {
        'A0': (1189, 841),
        'A1': (841, 594),
        'A2': (594, 420),
        'A3': (420, 297),
        'A4': (297, 210),
        'A4_LANDSCAPE': (210, 297)
    }
    
    # 如果未提供模板路径，使用项目根目录下的templates目录
    if template_path is None:
        template_name = f"{paper_size}_Template.dxf"
        templates_dir = os.path.join(PROJECT_ROOT, "templates")
        template_path = os.path.join(templates_dir, template_name)
        
        # 确保templates目录存在
        os.makedirs(templates_dir, exist_ok=True)
        print(f"模板目录: {templates_dir}")
    
    # 如果未提供输出目录，使用项目根目录下的output目录
    if output_dir is None:
        output_dir = os.path.join(PROJECT_ROOT, "output")
        
        # 确保output目录存在
        os.makedirs(output_dir, exist_ok=True)
        print(f"输出目录: {output_dir}")
    
    # 尝试加载模板文件
    try:
        print(f"尝试加载模板: {template_path}")
        part_doc = ezdxf.readfile(template_path)
        print("模板加载成功")
    except Exception as e:
        print(f"加载模板失败: {e}")
        print("尝试创建新的DXF文件...")
        part_doc = ezdxf.new('R2010')
        
        # 对于新创建的文件，设置合适的界限
        current_size = paper_sizes.get(paper_size, paper_sizes['A3'])
        part_doc.header['$EXTMIN'] = (0, 0, 0)
        part_doc.header['$EXTMAX'] = (current_size[0], current_size[1], 0)
    
    # 获取模型空间
    msp = part_doc.modelspace()
    
    # 创建绘图工具实例（使用重构后的版本）
    drawing_tools = RiceMillDrawingTools(msp, part_doc)
    
    # 如果未提供原点坐标，使用图纸中心点
    if origin is None:
        # 根据纸张大小设置默认原点
        current_size = paper_sizes.get(paper_size, paper_sizes['A3'])
        origin = (current_size[0]/2, current_size[1]/2)  # 图纸中心点
    
    # 计算比例文本
    scale_ratio = 1 / scale_factor
    scale_ratio_rounded = int(scale_ratio) if scale_ratio == int(scale_ratio) else scale_ratio
    scale_text = f"1:{scale_ratio_rounded}"
    
    # 确保标题信息中包含比例文本
    if "scale" not in title_info:
        title_info["scale"] = scale_text
    
    # 确保标题信息中包含日期
    if "date" not in title_info:
        from datetime import datetime
        title_info["date"] = datetime.now().strftime("%Y-%m-%d")
    
    print(f"  绘制 {part_name}，原点坐标 {origin}，比例因子 {scale_factor}，比例文本 {scale_text}")
    
    # 绘制零件
    draw_func(drawing_tools, origin, scale=scale_factor)
    
    # 添加额外视图（如剖视图、局部放大图等）
    if add_views:
        for view in add_views:
            view_type = view.get('type', '')
            
            if view_type == 'section':
                # 添加剖视图标签
                label = view.get('label', 'A-A')
                position = view.get('position', (origin[0], origin[1] - 100))
                drawing_tools.add_section_view_label(position, section_label=label)
                
                # 如果提供了剖切线位置，添加剖切线
                if 'section_line' in view:
                    start = view['section_line'].get('start', (origin[0] - 50, origin[1] + 50))
                    end = view['section_line'].get('end', (origin[0] + 50, origin[1] + 50))
                    section_label = label.split('-')[0]  # 从 'A-A' 提取 'A'
                    drawing_tools.add_section_line(start, end, section_label=section_label)
            
            elif view_type == 'detail':
                # 添加局部放大图
                center = view.get('center', (origin[0] + 80, origin[1] + 80))
                radius = view.get('radius', 15)
                label = view.get('label', 'B')
                detail_scale = view.get('scale', '2:1')
                drawing_tools.add_detail_view(center, radius, detail_label=label, scale=detail_scale)
    
    # 更新标题栏
    update_title_block(msp, part_doc, title_info)
    
    # 保存零件图
    output_filename = os.path.join(output_dir, f"{part_name}.dxf")
    part_doc.saveas(output_filename)
    print(f"已保存零件图: {output_filename}")
    
    return output_filename 