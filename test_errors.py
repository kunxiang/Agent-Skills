"""
测试 LSP 错误检测功能
"""

# 故意的语法错误 - 缺少冒号
def broken_function(x)
    return x * 2

# 未定义变量的使用
result = undefined_variable + 5

# 类型错误示例
number = 42
text = "hello"
# 这应该会被 LSP 标记为潜在问题
mixed = number + text

# 缩进错误
def another_function():
print("缩进错误")  # 故意的缩进错误

# 未闭合的括号
data = [1, 2, 3
print(data)

# 导入不存在的模块
from nonexistent_module import something

# 正确的代码，用于对比
def correct_function(x):
    """这是正确的函数"""
    return x * 2

# 使用未导入的模块
result = math.sqrt(16)  # math 未导入