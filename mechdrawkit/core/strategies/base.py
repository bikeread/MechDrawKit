from abc import ABC, abstractmethod
from typing import Any, Dict


class DrawingStrategy(ABC):
    """绘图策略抽象基类
    
    定义所有绘图策略必须实现的接口规范
    """
    
    def __init__(self, canvas_adapter, config_manager):
        """初始化绘图策略
        
        Args:
            canvas_adapter: 画布适配器对象
            config_manager: 配置管理器对象
        """
        self.canvas = canvas_adapter
        self.config = config_manager
    
    @abstractmethod
    def draw(self, operation: str, **kwargs) -> Any:
        """执行绘图操作
        
        Args:
            operation: 操作类型字符串
            **kwargs: 操作参数
            
        Returns:
            绘图结果对象
            
        Raises:
            ValueError: 当操作类型不支持时
            TypeError: 当参数类型错误时
        """
        pass
    
    def validate_params(self, operation: str, **kwargs) -> bool:
        """参数验证
        
        Args:
            operation: 操作类型
            **kwargs: 操作参数
            
        Returns:
            bool: 参数是否有效
        """
        # 默认实现：基本验证
        if not operation:
            return False
        return True
    
    def _get_layer(self, layer: str) -> str:
        """获取映射后的图层名称
        
        Args:
            layer: 逻辑图层名称
            
        Returns:
            str: 映射后的物理图层名称
        """
        return self.config.get_layer_mapping(layer) 