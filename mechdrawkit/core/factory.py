from typing import Dict, Type, Any, List
from .strategies.base import DrawingStrategy
from .strategies.basic_shapes import BasicShapeDrawer
from .strategies.dimensions import DimensionDrawer
from .strategies.symbols import SymbolDrawer
from .strategies.views import ViewDrawer


class ComponentFactory:
    """组件工厂类
    
    负责策略组件的注册、创建和管理，支持懒加载和实例缓存
    """
    
    # 策略组件注册表
    _strategies: Dict[str, Type[DrawingStrategy]] = {}
    # 实例缓存
    _instances: Dict[str, DrawingStrategy] = {}
    
    @classmethod
    def register_strategy(cls, name: str, strategy_class: Type[DrawingStrategy]):
        """注册策略组件
        
        Args:
            name: 策略名称
            strategy_class: 策略类
        """
        if not issubclass(strategy_class, DrawingStrategy):
            raise ValueError(f"Strategy class must inherit from DrawingStrategy: {strategy_class}")
        
        cls._strategies[name] = strategy_class
    
    @classmethod
    def create_strategy(cls, name: str, canvas, config) -> DrawingStrategy:
        """创建策略组件实例
        
        Args:
            name: 策略名称
            canvas: 画布适配器对象
            config: 配置管理器对象
            
        Returns:
            策略组件实例
            
        Raises:
            ValueError: 当策略名称不存在时
        """
        if name not in cls._strategies:
            raise ValueError(f"Unknown strategy: {name}. Available strategies: {list(cls._strategies.keys())}")
        
        # 创建缓存key
        cache_key = f"{name}_{id(canvas)}_{id(config)}"
        
        # 检查缓存
        if cache_key in cls._instances:
            return cls._instances[cache_key]
        
        # 创建新实例
        strategy_class = cls._strategies[name]
        instance = strategy_class(canvas, config)
        
        # 缓存实例
        cls._instances[cache_key] = instance
        
        return instance
    
    @classmethod
    def list_strategies(cls) -> List[str]:
        """获取所有注册的策略名称列表
        
        Returns:
            策略名称列表
        """
        return list(cls._strategies.keys())
    
    @classmethod
    def clear_cache(cls):
        """清理实例缓存"""
        cls._instances.clear()
    
    @classmethod
    def _auto_register_strategies(cls):
        """自动注册所有策略组件"""
        # 注册默认策略组件
        cls.register_strategy('basic_shapes', BasicShapeDrawer)
        cls.register_strategy('dimensions', DimensionDrawer)
        cls.register_strategy('symbols', SymbolDrawer)
        cls.register_strategy('views', ViewDrawer)


# 自动注册默认策略组件
ComponentFactory._auto_register_strategies() 