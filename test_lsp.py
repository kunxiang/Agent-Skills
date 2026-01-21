"""
测试 Claude Code LSP 功能的 Python 文件
"""

class TestClass:
    """测试类，用于验证跳转到定义功能"""

    def __init__(self, name):
        self.name = name
        self.count = 0

    def increment(self):
        """增加计数器"""
        self.count += 1
        return self.count

    def get_info(self):
        """获取信息"""
        return f"Name: {self.name}, Count: {self.count}"


def test_function(param1, param2):
    """测试函数，用于验证代码补全"""
    result = param1 + param2
    return result


# 创建实例并测试
if __name__ == "__main__":
    # 测试类的实例化
    obj = TestClass("Test")

    # 测试方法调用 - LSP 应该提供补全建议
    obj.increment()
    info = obj.get_info()
    print(info)

    # 测试函数调用
    result = test_function(5, 3)
    print(f"Result: {result}")

    # 测试标准库补全
    import os
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")