def update_title_block(msp, doc, title_info):
    """
    Update template title block with custom information
    
    Parameters:
    -----------
    msp : ezdxf.layouts.ModelSpace
        Model space object of the drawing
    doc : ezdxf.document.Drawing
        DXF document object
    title_info : dict
        Dictionary containing title block information with the following keys:
        - 图样名称: Drawing title
        - 图样代号: Drawing number
        - 单位名称: Organization name
        - 设计: Designer name
        - 审核: Reviewer name
        - 标准号: Standard number
        - 重量: Weight
        - 比例: Scale
        - 材料: Material
        - 日期: Date
    
    Returns:
    --------
    None
    """
    # Default title info if not provided
    default_info = {
        "图样名称": "Assembly Drawing",
        "图样代号": "001",
        "单位名称": "Organization",
        "设计": "Designer",
        "审核": "Reviewer",
        "标准号": "Standard",
        "重量": "Weight",
        "比例": "1:1",
        "材料": "Assembly",
        "日期": "Date",
        "weight": "45kg",    # 符合设计方案中的要求 (≤50kg)
        "scale": "1:2"     # 适合A0纸上绘制的比例
    }
    
    # Merge provided info with defaults
    for key, value in default_info.items():
        if key not in title_info:
            title_info[key] = value
    
    # Use template's text style
    text_style = '5号字体' if '5号字体' in doc.styles else 'Standard'
    
    # Iterate through all text entities in model space
    for entity in msp:
        if entity.dxftype() in ('TEXT', 'MTEXT'):
            if hasattr(entity.dxf, 'insert') :
                if hasattr(entity.dxf, 'text'):
                    text = entity.dxf.text
                    pos = entity.dxf.insert
                    
                    # Update drawing name
                    if '图样名称' in text or '(图样名称)' in text or '（图样名称）' in text:
                        entity.dxf.text = title_info["图样名称"]
                        entity.dxf.style = text_style
                    
                    # Update drawing code
                    elif '图样代号' in text or '(图样代号)' in text or '（图样代号）' in text:
                        entity.dxf.text = title_info["图样代号"]
                        entity.dxf.style = text_style
                    
                    # Update organization name
                    elif '单位名称' in text or '(单位名称)' in text or '（单位名称）' in text:
                        entity.dxf.text = title_info["单位名称"]
                        entity.dxf.style = text_style
                    
                    # Update signature area
                    elif '（签名）' in text or '(签名)' in text:
                        if pos[0] < 1030:  # Designer signature position
                            entity.dxf.text = title_info["设计"]
                            entity.dxf.style = text_style
                        elif pos[0] < 1060:  # Checker signature position
                            entity.dxf.text = title_info["审核"]
                            entity.dxf.style = text_style
                    
                    # Update date area
                    elif '（年月日）' in text or '(年月日)' in text or '年、月、日' in text:
                        entity.dxf.text = title_info["日期"]
                        entity.dxf.style = text_style
                    
                    # Update material mark
                    elif '材料标记' in text or '(材料标记)' in text or '（材料标记）' in text:
                        entity.dxf.text = title_info["材料"]
                        entity.dxf.style = text_style
                    
                    # Update standard number
                    elif '标准号' in text:
                        entity.dxf.text = title_info["标准号"]
                        entity.dxf.style = text_style
                    
                    # Update weight
                    elif 'weight' in text:
                        entity.dxf.text = title_info["weight"]
                        entity.dxf.style = text_style
                    
                    # Update scale
                    elif 'scale' in text:
                        entity.dxf.text = title_info["scale"]
                        entity.dxf.style = text_style

def add_parts_table(msp, doc, parts):
    """
    Add parts to the template's parts table
    
    Parameters:
    -----------
    msp : ezdxf.layouts.ModelSpace
        Model space object of the drawing
    doc : ezdxf.document.Drawing
        DXF document object
    parts : dict
        Dictionary mapping sequence numbers to part information lists.
        Each list should contain: [代号, 名称, 数量, 材料, 单件质量, 总计质量, 备注]
        Parts with sequence numbers 1-3 will be placed in template areas
        Parts with sequence numbers >3 will be placed in additional rows
    
    Returns:
    --------
    dict
        Dictionary containing parts table information including:
        - base_x: x-coordinate of the left edge of the table
        - base_y: y-coordinate of the first row
        - row_height: height of each row
        - rows: total number of rows
    """
    # Split parts into template parts (1-3) and additional parts (>3)
    template_parts = {k: v for k, v in parts.items() if 1 <= k <= 3}
    additional_parts = {k: v for k, v in parts.items() if k > 3}
    
    # Existing sequence number positions from template analysis
    existing_seq_y = {
        1: 53.5,
        2: 60.5,
        3: 67.5
    }
    
    # Table coordinates from analysis
    base_x = 999.0  # Parts table left boundary
    row_height = 7.0  # Height per row
    
    # Table's column x-coordinates (from analysis)
    col_x = {
        "序号": 1003.0,    # Sequence number column center
        "代号": 1029.0,    # Code column center
        "名称": 1071.0,    # Name column center
        "数量": 1095.0,    # Quantity column center
        "材料": 1118.0,    # Material column center
        "单件质量": 1142.0, # Unit weight column center
        "总计质量": 1153.0, # Total weight column center
        "备注": 1200.0     # Remarks column center
    }
    
    # Table title row position
    title_y = existing_seq_y[3] + row_height  # Title row above first data row
    
    # Text height and style settings
    text_height = 3.5  # Based on analysis 
    text_style = '5号字体' if '5号字体' in doc.styles else 'Standard'  # Use template's text style
    
    # Column width definitions for drawing table lines
    col_widths = {
        "序号": 8,       # Sequence number column width
        "代号": 44,      # Code column width
        "名称": 40,      # Name column width
        "数量": 8,       # Quantity column width
        "材料": 38,      # Material column width
        "单件质量": 10,   # Unit weight column width
        "总计质量": 12,   # Total weight column width
        "备注": 19.5     # Remarks column width
    }
    
    # Table boundary definitions
    table_left = base_x
    table_right = base_x + sum(col_widths.values())
    
    # Process parts for sequence numbers 1-3 (connect with template)
    print("Adding parts to parts table:")
    for i in range(1, 4):
        if i in template_parts:
            part_info = template_parts[i]
            y_pos = existing_seq_y[i]  # Use existing y-coordinate in template
            
            print(f"  Sequence {i} position: y={y_pos}, Part: {part_info[0]}")
            
            # Add part information to all columns
            add_part_to_table(msp, doc, i, part_info, col_x, y_pos, text_height, text_style)
    
    # Calculate starting position for sequence number 4 and beyond
    start_y = existing_seq_y[3] + row_height
    
    # Process additional parts starting at position 4
    for i in range(4, 4 + len(additional_parts)):
        if i in additional_parts:
            part_info = additional_parts[i]
            y_pos = start_y + (i-4) * row_height  # Offset each row
            
            print(f"  Sequence {i} position: y={y_pos}, Part: {part_info[0]}")
            
            # Add this part to the table
            add_part_to_table(msp, doc, i, part_info, col_x, y_pos, text_height, text_style)
    
    # Get position for lines between rows 3 and 4
    begin_line_y = existing_seq_y[3] + row_height + 26.5
    
    # Draw table frame - horizontal lines for sequences 4 to max
    current_y = start_y + 27.5 + 2.5
    max_row = 3 + len(additional_parts) if additional_parts else 16
    for i in range(4, max_row):
        # Horizontal divider for each row
        y_line = current_y + row_height / 2
        msp.add_line((table_left, y_line), (table_right, y_line), 
                     dxfattribs={'layer': '2粗实线'})
        current_y += row_height
    
    # Add bottom border for the last row
    y_line = current_y + row_height / 2
    msp.add_line((table_left, y_line), (table_right, y_line), 
                 dxfattribs={'layer': '2粗实线'})
    
    # Add left frame line - from after sequence 3 to bottom
    msp.add_line(
        (table_left, begin_line_y), 
        (table_left, y_line),  # To bottom of last row
        dxfattribs={'layer': '2粗实线'}
    )

    # Draw vertical divider lines - starting after sequence 3
    x_current = table_left
    for col_name, width in col_widths.items():
        # Vertical line position
        x_line = x_current + width
        
        # Skip right border of the last column (already covered by outer frame)
        if col_name != "备注":
            # Draw vertical line from below sequence 3 to last row
            msp.add_line(
                (x_line, begin_line_y),
                (x_line, y_line),
                dxfattribs={'layer': '2粗实线'}
            )
        
        x_current += width
    
    # Return table information for further reference
    return {
        "base_x": base_x,
        "base_y": existing_seq_y[1],  # Use sequence 1's y-coordinate as base
        "row_height": row_height,
        "rows": min(17, 3 + len(additional_parts)) if additional_parts else 16  # Match max_row calculation
    }

def add_part_to_table(msp, doc, seq_num, part_info, col_x, y_pos, text_height, text_style):
    """
    Helper function to add a single part to the parts table
    
    Parameters:
    -----------
    msp : ezdxf.layouts.ModelSpace
        Model space object of the drawing
    doc : ezdxf.document.Drawing
        DXF document object
    seq_num : int
        Sequence number for the part
    part_info : list
        List containing [代号, 名称, 数量, 材料, 单件质量, 总计质量, 备注]
    col_x : dict
        Dictionary mapping column names to x-coordinates
    y_pos : float
        Y-coordinate for the row
    text_height : float
        Text height for the table entries
    text_style : str
        Text style to use
    
    Returns:
    --------
    None
    """
    # Sequence number
    msp.add_text(str(seq_num), dxfattribs={
        'height': text_height,
        'layer': '3文字',
        'style': text_style,
        'insert': (col_x["序号"], y_pos),
        'halign': 1,  # Center aligned
        'valign': 1,  # Vertically centered
        'align_point': (col_x["序号"], y_pos)
    })
    
    # Code - use part_info[0] or generated code if part_info[0] is empty
    code = part_info[0] if part_info[0] else f"P{seq_num:02d}"
    msp.add_text(code, dxfattribs={
        'height': text_height,
        'layer': '3文字',
        'style': text_style,
        'insert': (col_x["代号"], y_pos),
        'halign': 1,
        'valign': 1,
        'align_point': (col_x["代号"], y_pos)
    })
    
    # Name (truncate if too long)
    name = part_info[1]
    if len(name) > 10:  # Prevent name from being too long
        name = name[:10]
    msp.add_text(name, dxfattribs={
        'height': text_height,
        'layer': '3文字',
        'style': text_style,
        'insert': (col_x["名称"], y_pos),
        'halign': 1,
        'valign': 1,
        'align_point': (col_x["名称"], y_pos)
    })
    
    # Quantity
    msp.add_text(part_info[2], dxfattribs={
        'height': text_height,
        'layer': '3文字',
        'style': text_style,
        'insert': (col_x["数量"], y_pos),
        'halign': 1,
        'valign': 1,
        'align_point': (col_x["数量"], y_pos)
    })
    
    # Material (truncate if too long)
    material = part_info[3]
    if len(material) > 10:  # Prevent material description from being too long
        material = material[:10]
    msp.add_text(material, dxfattribs={
        'height': text_height,
        'layer': '3文字',
        'style': text_style,
        'insert': (col_x["材料"], y_pos),
        'halign': 1,
        'valign': 1,
        'align_point': (col_x["材料"], y_pos)
    })
    
    # Unit weight
    msp.add_text(part_info[4], dxfattribs={
        'height': text_height,
        'layer': '3文字',
        'style': text_style,
        'insert': (col_x["单件质量"], y_pos),
        'halign': 1,
        'valign': 1,
        'align_point': (col_x["单件质量"], y_pos)
    })
    
    # Total weight
    msp.add_text(part_info[5], dxfattribs={
        'height': text_height,
        'layer': '3文字',
        'style': text_style,
        'insert': (col_x["总计质量"], y_pos),
        'halign': 1,
        'valign': 1,
        'align_point': (col_x["总计质量"], y_pos)
    })
    
    # Remarks
    msp.add_text(part_info[6], dxfattribs={
        'height': text_height,
        'layer': '3文字',
        'style': text_style,
        'insert': (col_x["备注"], y_pos),
        'halign': 1,
        'valign': 1,
        'align_point': (col_x["备注"], y_pos)
    })