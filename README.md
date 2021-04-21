# AwesomeBot

## dev start

1. 安装依赖 `poetry install`
2. 启动 go-cqhttp chrome 依赖`docker-compose up -d`
3. 启动开发 `uvicorn bot:app --workers 4 --reload --reload-dir='./src' --host=0.0.0.0 --port 8080`

## build docker

`docker build -f ./Dockerfile -t awesomebot . --no-cache --rm`

## prod start

`docker-compose -f ./.docker/docker-compose.yml up -d`

## 注意事项

1. config.hjson 内账号密码配置
2. env 内 chrome 插件路径配置

## 参考资料

1. [nonebot2](https://github.com/nonebot/nonebot2)
2. [nonebot2 doc](https://v2.nonebot.dev/)
3. [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
4. [selenium](https://www.selenium.dev/documentation/en/)
