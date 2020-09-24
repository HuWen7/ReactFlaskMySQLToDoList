# ReactFlaskMySQLToDoList

使用

- material UI

- react 
- redux / react-redux / redux-thunk
- react-router
- axios
- flask 

构建一个 ToDoList。

知乎链接：https://zhuanlan.zhihu.com/p/256420485

## 完成情况

- [x] Flask 建立和链接数据库
- [x] Server 端 Token 登录
- [ ] 样式构建
- [ ] 数据管理
- [ ] 路由

## 使用方法

### 服务端

- python2.7

``` shell
cd Server
# 安装必要的库
pip install -r requirement.txt
# 配置 constant.py，包括数据库的链接，端口号，Token 的密钥等
cp constant.py.example constant.py
# 创建数据库
python schema.py
# 运行服务端
python app.py
```

