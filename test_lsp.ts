/**
 * 测试 Claude Code LSP 功能的 TypeScript 文件
 */

interface User {
    id: number;
    name: string;
    email: string;
    age?: number;
}

class UserService {
    private users: User[] = [];

    constructor() {
        this.users = [];
    }

    addUser(user: User): void {
        this.users.push(user);
    }

    getUserById(id: number): User | undefined {
        return this.users.find(u => u.id === id);
    }

    getAllUsers(): User[] {
        return this.users;
    }
}

// 测试函数
function processUser(user: User): string {
    // LSP 应该能够提供 user 对象的属性补全
    const info = `User ${user.name} with email ${user.email}`;
    return info;
}

// 使用示例
const service = new UserService();

// LSP 应该能够提供类型提示
const newUser: User = {
    id: 1,
    name: "张三",
    email: "zhangsan@example.com",
    age: 25
};

// LSP 应该能够提供方法补全
service.addUser(newUser);

// LSP 应该能够跳转到 getUserById 的定义
const foundUser = service.getUserById(1);

if (foundUser) {
    // LSP 应该能够识别 foundUser 的类型为 User
    console.log(processUser(foundUser));
}

// 测试数组方法的补全
const allUsers = service.getAllUsers();
allUsers.forEach(user => {
    // LSP 应该识别 user 的类型
    console.log(`${user.id}: ${user.name}`);
});

export { User, UserService, processUser };