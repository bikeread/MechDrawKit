#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MechDrawKit 使用示例
展示重构后的新架构特性和完整的向后兼容性

包括：
1. 向后兼容性演示 - 原有代码无需任何修改
2. 新架构特性演示 - 策略模式和模板系统的使用
3. 混合使用模式 - 同时使用原有接口和新特性
"""

import os
import ezdxf
# 新的推荐导入方式
from mechdrawkit import (
    RiceMillDrawingTools, generate_part_drawing,
    GBStandardConfig, ComponentFactory, EzdxfAdapter,
    BasicShapeDrawer, DimensionDrawer, SymbolDrawer, ViewDrawer,
    ShaftTemplate, GearTemplate
)

def demo_backward_compatibility():
    """演示1：完全向后兼容性 - 原有代码无需任何修改"""
    print("=" * 60)
    print("演示1：完全向后兼容性")
    print("=" * 60)
    
    # 创建新的DXF文档
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # 使用原有的工具类接口，完全不变
    drawing_tools = RiceMillDrawingTools(msp, doc)
    
    # 原有的绘图方法调用完全不变
    origin = (100, 100)
    
    # 绘制基础图形
    print("  ✓ 绘制基础图形（原有接口）")
    drawing_tools.draw_circle((origin[0], origin[1]), 20)
    drawing_tools.draw_rectangle((origin[0] - 40, origin[1] - 15), 80, 30)
    drawing_tools.draw_centerline((origin[0] - 50, origin[1]), (origin[0] + 50, origin[1]))
    
    # 添加尺寸标注
    print("  ✓ 添加尺寸标注（原有接口）")
    drawing_tools.add_dimension((origin[0] - 40, origin[1] - 15), (origin[0] + 40, origin[1] - 15), 25)
    drawing_tools.add_diameter_dimension((origin[0], origin[1]), 20, angle=45)
    
    # 添加工程符号
    print("  ✓ 添加工程符号（原有接口）")
    drawing_tools.add_roughness((origin[0] + 50, origin[1] + 20), "3.2")
    drawing_tools.add_leader_arrow((origin[0] + 20, origin[1] + 10), (origin[0] + 60, origin[1] + 30), "重要特征")
    
    # 保存文件
    output_path = "output/demo1_backward_compatibility.dxf"
    os.makedirs("output", exist_ok=True)
    doc.saveas(output_path)
    print(f"  ✓ 保存文件: {output_path}")


def demo_new_architecture():
    """演示2：新架构特性 - 直接使用策略组件"""
    print("\n" + "=" * 60)
    print("演示2：新架构特性 - 策略组件")
    print("=" * 60)
    
    # 创建新的DXF文档
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # 初始化新架构组件
    config = GBStandardConfig()
    canvas = EzdxfAdapter(msp, doc, config)
    
    # 直接创建策略组件
    basic_shapes = ComponentFactory.create_strategy('basic_shapes', canvas, config)
    dimensions = ComponentFactory.create_strategy('dimensions', canvas, config)
    symbols = ComponentFactory.create_strategy('symbols', canvas, config)
    views = ComponentFactory.create_strategy('views', canvas, config)
    
    print("  ✓ 策略组件创建完成")
    
    # 使用策略组件绘图
    origin = (200, 100)
    
    # 基础图形策略
    print("  ✓ 使用基础图形策略")
    basic_shapes.draw('circle', center=(origin[0], origin[1]), radius=25)
    basic_shapes.draw('rectangle', lower_left=(origin[0] - 50, origin[1] - 20), width=100, height=40)
    basic_shapes.draw('centerline', start=(origin[0] - 60, origin[1]), end=(origin[0] + 60, origin[1]))
    
    # 尺寸标注策略
    print("  ✓ 使用尺寸标注策略")
    dimensions.draw('linear', p1=(origin[0] - 50, origin[1] - 20), p2=(origin[0] + 50, origin[1] - 20), distance=30)
    dimensions.draw('diameter', center=(origin[0], origin[1]), radius=25, angle=135)
    
    # 符号绘制策略
    print("  ✓ 使用符号绘制策略")
    symbols.draw('advanced_surface_finish', position=(origin[0] + 60, origin[1] + 25), 
                ra_value="1.6", machining_method="精车", cutoff="0.8")
    symbols.draw('geometric_tolerance', position=(origin[0] + 60, origin[1] - 10), 
                symbol="⊥", tolerance="0.05", datum="A")
    
    # 视图处理策略
    print("  ✓ 使用视图处理策略")
    views.draw('text', text="新架构示例", position=(origin[0], origin[1] + 60), height=5)
    views.draw('section_line', start_point=(origin[0] - 30, origin[1] + 40), 
              end_point=(origin[0] + 30, origin[1] + 40), section_label="B")
    
    # 保存文件
    output_path = "output/demo2_new_architecture.dxf"
    doc.saveas(output_path)
    print(f"  ✓ 保存文件: {output_path}")


def demo_template_system():
    """演示3：模板系统 - 使用预定义模板"""
    print("\n" + "=" * 60)
    print("演示3：模板系统")
    print("=" * 60)
    
    # 轴类零件模板
    print("  ✓ 使用轴类零件模板")
    doc1 = ezdxf.new('R2010')
    msp1 = doc1.modelspace()
    
    shaft_template = ShaftTemplate(msp1, doc1)
    shaft_doc = shaft_template.generate_drawing(
        origin=(150, 150),
        diameter=30,
        length=120
    )
    
    output_path1 = "output/demo3_shaft_template.dxf"
    shaft_doc.saveas(output_path1)
    print(f"    保存轴类零件图: {output_path1}")
    
    # 齿轮零件模板
    print("  ✓ 使用齿轮零件模板")
    doc2 = ezdxf.new('R2010')
    msp2 = doc2.modelspace()
    
    gear_template = GearTemplate(msp2, doc2)
    gear_doc = gear_template.generate_drawing(
        origin=(150, 150),
        outer_diameter=80,
        inner_diameter=25,
        thickness=12
    )
    
    output_path2 = "output/demo3_gear_template.dxf"
    gear_doc.saveas(output_path2)
    print(f"    保存齿轮零件图: {output_path2}")


def demo_mixed_usage():
    """演示4：混合使用模式 - 原有接口与新特性并存"""
    print("\n" + "=" * 60)
    print("演示4：混合使用模式")
    print("=" * 60)
    
    # 使用原有的generate_part_drawing函数
    def draw_complex_part(drawing_tools, origin, scale=1.0):
        """绘制复杂零件，混合使用原有接口和新特性"""
        x, y = origin
        
        # 使用原有接口绘制基础形状
        print("    使用原有接口绘制基础形状")
        drawing_tools.draw_rectangle((x - 40, y - 20), 80, 40)
        drawing_tools.draw_circle((x - 20, y), 8)
        drawing_tools.draw_circle((x + 20, y), 8)
        drawing_tools.draw_centerline((x - 50, y), (x + 50, y))
        
        # 使用原有接口添加尺寸
        print("    使用原有接口添加尺寸")
        drawing_tools.add_dimension((x - 40, y - 20), (x + 40, y - 20), 25)
        drawing_tools.add_diameter_dimension((x - 20, y), 8, angle=45)
        drawing_tools.add_diameter_dimension((x + 20, y), 8, angle=135)
        
        # 使用新架构的策略组件添加高级符号
        print("    使用新架构添加高级符号")
        drawing_tools.symbols.draw('advanced_surface_finish', 
                                  position=(x + 50, y + 25), 
                                  ra_value="0.8", 
                                  machining_method="精铣",
                                  lay="=", 
                                  cutoff="0.25")
        
        drawing_tools.symbols.draw('welding_symbol',
                                  position=(x - 60, y),
                                  weld_type="V",
                                  size="6",
                                  length="50",
                                  field=True)
        
        # 使用视图策略添加剖面指示
        drawing_tools.views.draw('section_line',
                                start_point=(x - 30, y + 35),
                                end_point=(x + 30, y + 35),
                                section_label="C")
    
    # 标题栏信息
    title_info = {
        "title": "混合使用模式示例",
        "part_name": "复杂零件",
        "material": "45钢",
        "designer": "重构团队",
        "checker": "质检员",
        "scale": "1:1"
    }
    
    print("  ✓ 使用混合模式生成零件图")
    output_path = generate_part_drawing(
        part_name="demo4_mixed_usage",
        draw_func=draw_complex_part,
        title_info=title_info,
        origin=(200, 150),
        scale_factor=1.0,
        paper_size='A3',
        add_views=[
            {
                'type': 'section',
                'label': 'C-C',
                'position': (200, 50),
                'section_line': {
                    'start': (170, 185),
                    'end': (230, 185)
                }
            },
            {
                'type': 'detail',
                'center': (280, 200),
                'radius': 12,
                'label': 'D',
                'scale': '5:1'
            }
        ]
    )
    
    print(f"  ✓ 保存混合使用示例: {output_path}")


def demo_configuration_system():
    """演示5：配置系统 - GB标准配置管理"""
    print("\n" + "=" * 60)
    print("演示5：配置系统")
    print("=" * 60)
    
    # 获取配置实例
    config = GBStandardConfig()
    
    # 展示配置信息
    print("  ✓ GB标准线型配置:")
    line_types = config.get_all_line_types()
    for name, info in list(line_types.items())[:3]:  # 只显示前3个
        print(f"    {name}: {info['description']}")
    
    print("  ✓ 图层映射配置:")
    layer_mappings = config.get_all_layer_mappings()
    for logical, physical in list(layer_mappings.items())[:5]:  # 只显示前5个
        print(f"    {logical} -> {physical}")
    
    print("  ✓ 文字高度配置:")
    for height_type in ['TITLE', 'NORMAL', 'SMALL']:
        height = config.get_text_height(height_type)
        print(f"    {height_type}: {height}mm")
    
    print("  ✓ 其他配置:")
    print(f"    箭头尺寸: {config.get_arrow_size()}mm")
    print(f"    字体样式: {config.get_font_style()}")
    print(f"    支持比例: {config.get_scales()[:5]}...")  # 只显示前5个


def main():
    """运行所有演示"""
    print("MechDrawKit 2.0 重构演示")
    print("展示向后兼容性和新架构特性")
    print()
    
    # 确保输出目录存在
    os.makedirs("output", exist_ok=True)
    
    try:
        # 运行所有演示
        demo_backward_compatibility()
        demo_new_architecture()
        demo_template_system()
        demo_mixed_usage()
        demo_configuration_system()
        
        print("\n" + "=" * 60)
        print("所有演示完成！")
        print("=" * 60)
        print("重构成果:")
        print("✓ 完全向后兼容 - 原有代码无需修改")
        print("✓ 策略模式架构 - 功能模块化")
        print("✓ 配置外化 - GB标准集中管理")  
        print("✓ 模板系统 - 标准化绘图流程")
        print("✓ 工厂模式 - 组件统一创建管理")
        print("✓ 适配器模式 - ezdxf接口封装")
        print()
        print("生成的文件位于 output/ 目录:")
        for file in os.listdir("output"):
            if file.endswith('.dxf'):
                print(f"  - {file}")
        
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保所有重构组件已正确创建")
    except Exception as e:
        print(f"运行错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 