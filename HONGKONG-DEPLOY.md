# 香港试点部署

当前阶段：应用和部署文件已准备；尚无香港实例、公网地址或上线结果。此前准备的大陆COS方案保留，但本次优先香港，无需先办理大陆备案。

## 选定方案

香港轻量云服务器，先用公网IP提供HTTP试点，暂不购买域名。网站是静态站点，试点使用小规格Linux实例即可；套餐必须在账户控制台核实中国香港地域、CPU/内存、流量额度、线路类型、续费及超额流量价格，再决定是否购买。不要默认勾选长期自动续费。

腾讯云官方指出中国香港入门型套餐不能保障中国内地跨境公网质量。该方案只用于验证；上线后需用实际大陆网络测试，不能宣称已经保证稳定。

需要用户完成：注册云账户、按平台要求实名认证；在确认实际套餐与价格后购买实例；提供公网IP并配置适当的部署权限。无需在聊天里发送账户密码、SecretKey或SSH私钥。公网入站80用于试点，SSH仅限维护者来源IP；后续配置HTTPS时再开放443。

注册/登录：https://cloud.tencent.com/login
实例控制台：https://console.cloud.tencent.com/lighthouse/instance
地域与网络：https://cloud.tencent.com/document/product/1207/50103
套餐说明：https://cloud.tencent.com/document/product/1207/73452/
备案地域说明：https://cloud.tencent.com/document/product/243/19630

## 实例就绪后的部署

以下命令在已安装Docker及Compose的专用香港Linux实例上执行。勿在本机或有其他网站的服务器上直接运行。80端口已被占用时先检查，不替换现有服务。

1. 将完整项目上传至服务器自己的目录并进入该目录；公网静态文件包仅供已有Nginx/Caddy站点直接上传。
2. 运行 `docker compose -f deploy/hongkong/compose.yaml config` 检查配置。
3. 运行 `docker compose -f deploy/hongkong/compose.yaml up -d --build`。
4. 用实例真实公网IP打开 `http://公网IP/`，检查首页、综述、章节、文献精读、政策筛选。

Docker镜像内置完整静态内容；访问者不需要连接GitHub、外部字体或CDN加载页面。官方文献链接仍由相应出版商提供。HTTP只用于公开内容试点；正式使用宜接入自有域名和HTTPS。

更新时先在源码端运行 `python3 scripts/build_pages.py` 与 `python3 scripts/validate.py`，然后重新上传并构建容器。容器不含数据库，资料由JSON版本文件管理；浏览器收藏和本地草稿不会同步到其他域名。

GitHub Pages与香港托管分别部署；香港自动同步尚未接入实例。本部署包不包含任何凭证。
