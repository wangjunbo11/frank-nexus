# Frank Nexus资料库

静态、无第三方前端依赖的开放科研目录。GitHub 为内容与版本的主仓库；dist 可以部署到 GitHub Pages 或其他静态托管服务。

## 当前内容

两份原始 Excel 清单共32条，按官方链接去重后31篇独立文献，其中16篇前沿文献、16篇方法文献（黄河水文经济模型交叉收录）。另有6个数据入口、4个论文案例、3个政策报告入口。三份 Word 的纯文字记录存于 notes.json，公式、图片、部分表格结构请查阅原文件。未上传原始论文全文或期刊图片。

导读依据用户整理材料与题名编写，非出版商摘要；正式目录的来源未全部联网核验，均保留核验状态。《The paradox of irrigation efficiency》原清单年份2026有疑点，尚未擅自替换。案例为文献案例，不属于课题组实地项目。

## 本地预览

在此目录运行 `python3 -m http.server 8080 --directory dist`，访问 http://localhost:8080 。不要直接双击 index.html，浏览器会限制 JSON 读取。

## GitHub 发布

使用 GitHub Actions 构建并发布 GitHub Pages。公开地址以 Pages 部署结果为准。

1. 用 `gh auth login --hostname github.com --web` 恢复账号登录。
2. 在本目录执行 `git init -b main`、`git add .`、`git commit -m 'Build Frank Nexus research library'`。
3. 执行 `gh repo create frank-nexus --public --source=. --remote=origin --push`。若同名仓库已存在，先确认，勿覆盖。
4. GitHub 仓库 Settings → Pages → Source 选择 GitHub Actions；运行 Publish research library 工作流。
5. 以 Actions 返回的实际 URL 为准。未发布前不存在已验证的公开网址。

GitHub Pages 官方说明：https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages 。它支持从公开仓库发布静态网站；这并不构成全球所有地区可达性的保证。

## 覆盖不同地区

前端全部资源随站点托管，无远程字体、CDN或在线API运行依赖；网站打开与外部论文、数据入口访问分别处理。全球所有地区免VPN不能由GitHub Pages单独保证。若中国大陆稳定直连是硬性要求，建议使用自有域名，并另行选择大陆合规托管/镜像方案，完成服务商要求及实际跨地区网络测试。仓库可保持GitHub作为主源，镜像仅发布dist目录。当前未购买域名、未配置镜像，也未进行跨地区测试。

## 手动更新

网页“维护资料库”可添加、编辑、导入记录。保存的是当前浏览器的本地草稿，任何访客都不能直接改云端目录。点击“导出完整目录”，由有仓库权限的维护者将JSON覆盖至 dist/catalog.json，提交后自动发布。不要在前端写入GitHub token。编辑器导入会合并同编号记录，未出现的已有记录不删除；需要删除时通过GitHub编辑JSON。访客收藏仅保存在当前浏览器。

## 定期更新

仓库启用后 `.github/workflows/discover.yml` 每周一北京时间08:15检索最近45天的Crossref论文，按DOI与正式目录去重，写入候选池并发布。候选不自动冒充已审核资料；维护入口可将候选带入表单，补齐中文导读、核对相关性和官网后导出提交。该流程不需要API密钥或AI付费调用，不自动生成论文摘要。仓库Actions需开启且允许工作流写入；平台可能延迟计划任务，公共仓库长期无活动时也可能停用计划任务。接口失败时工作流报告失败，保留正式资料不变。

已有ChatGPT Nexus任务可以继续用于研究与导读；目前尚无自动读取该ChatGPT任务并同步GitHub的连接，不声称两者已经互通。

## 核验

`python3 scripts/validate.py` 检查目录结构、编号、链接协议和必要文件。脚本不证明官方链接在线、元数据准确、所有地区可访问。自动检索首次运行需联网，当前尚未运行线上流程。


## 2026-11-17 第二版

综述按原文生成3个Part、6章、31节，共41个HTML页面；不再显示文本文件归档卡片。31篇文献补充背景、方法、结论、启示，并各有独立页面。政策新增全球4项、国内4项，连同原有机构报告共11条，支持范围筛选。展示界面移除核验状态字样，后台记录继续保留来源管理信息。

内容修改后执行 `python3 scripts/build_pages.py` 再执行 `python3 scripts/validate.py`；GitHub发布和镜像工作流也执行此生成步骤。分节与表格保存在dist/reviews.json；原始notes.json仅作为历史归档数据，页面不再读取。

大陆镜像流程见 MAINLAND-MIRROR.md。镜像目前未上线，需实际云账户、域名、DNS与HTTPS配置。
