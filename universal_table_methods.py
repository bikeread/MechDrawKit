# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# Universal Table Methods - 向后兼容接口
# 这个文件提供了与之前版本的兼容性，所有功能现在都从mechdrawkit.tools包中导入。

# 为了保持向后兼容性，您可以继续使用：
#     from universal_table_methods import update_title_block, add_parts_table

# 推荐的新用法：
#     from mechdrawkit.tools import update_title_block, add_parts_table
# """

# # 从mechdrawkit.tools包中导入所有功能，保持向后兼容
# from mechdrawkit.tools.table_methods import (
#     update_title_block,
#     add_parts_table,
#     add_part_to_table
# )

# # 保持向后兼容的导出
# __all__ = [
#     'update_title_block',
#     'add_parts_table',
#     'add_part_to_table'
# ]

# # 向后兼容性警告（可选）
# import warnings
# warnings.warn(
#     "直接导入 universal_table_methods 已弃用。请使用 'from mechdrawkit.tools import update_title_block' 代替。",
#     DeprecationWarning,
#     stacklevel=2
# ) 