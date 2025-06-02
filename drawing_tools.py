# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# Drawing Tools - 向后兼容接口
# 这个文件提供了与之前版本的兼容性，所有功能现在都从mechdrawkit包中导入。

# 为了保持向后兼容性，您可以继续使用：
#     from drawing_tools import RiceMillDrawingTools, generate_part_drawing

# 推荐的新用法：
#     from mechdrawkit import RiceMillDrawingTools, generate_part_drawing
# """

# # 从mechdrawkit包中导入所有功能，保持向后兼容
# from mechdrawkit.drawing_tools import (
#     RiceMillDrawingTools,
#     generate_part_drawing,
#     find_project_root,
#     PROJECT_ROOT
# )

# # 保持向后兼容的导出
# __all__ = [
#     'RiceMillDrawingTools',
#     'generate_part_drawing', 
#     'find_project_root',
#     'PROJECT_ROOT'
# ]

# # 向后兼容性警告（可选）
# import warnings
# warnings.warn(
#     "直接导入 drawing_tools 已弃用。请使用 'from mechdrawkit import RiceMillDrawingTools' 代替。",
#     DeprecationWarning,
#     stacklevel=2
# ) 