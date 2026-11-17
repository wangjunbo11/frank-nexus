# 大陆镜像接入

状态：代码与自动同步流程已准备，尚未连接实际云账户或域名，当前没有已上线镜像网址。

GitHub保留主仓库；dist目录同步至中国大陆区域的腾讯云COS，使用自有域名作为大陆访问入口。已有GitHub发布工作流成功后，mirror.yml同步同一main分支内容；定期发现候选的工作流同样会触发镜像。镜像中的页面、样式、脚本和JSON都在本地托管，不回源GitHub，也不自动跳转外部代理。

## 接入资源

需要现有或新建的腾讯云COS桶、一个自有域名、备案、DNS管理权限和HTTPS配置。请勿将SecretKey发在聊天或写入仓库。通过GitHub环境mainland-mirror的Secrets填入凭证。

1. 创建专用中国大陆区域桶，按官方流程开启静态网站，索引文档index.html；配置适合公开站点的只读访问。上传凭证仅授予专用桶必要的写入权限。
2. 添加自定义域名，选择静态网站源站，配置CNAME和HTTPS。腾讯云说明2024年1月1日后创建的桶默认域名不支持网页预览，因此不能以默认桶域名代替正式入口。
3. 在仓库Actions Variables设置 COS_REGION（例如ap-shanghai）与 COS_BUCKET（完整bucket-appid）；在mainland-mirror环境Secrets设置 COS_SECRET_ID、COS_SECRET_KEY，可选COS_SESSION_TOKEN。
4. 完成域名和访问配置后，将仓库Variable COS_MIRROR_ENABLED设为true，手动运行Publish mainland mirror。
5. 上线后分别检查首页、reviews/index.html、章节页、literature/L001.html、catalog.json、CSS和JS的响应与HTTPS；使用电信、联通、移动和境外网络实测。仅本机访问成功不代表大陆全国稳定。

工作流不创建云资源、不购买域名、不修改DNS、不删除远端对象。云服务和域名会产生费用，应在明确账户与方案后接入。

官方托管指南：https://cloud.tencent.com/document/api/436/9512
Python SDK：https://cloud.tencent.com/document/product/436/12269

如果已有阿里云OSS或国内服务器，也可原样部署dist目录；需要替换上传步骤，内容和页面路径无需改写。
