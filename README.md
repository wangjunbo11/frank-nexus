# Frank Nexus资料库

静态、无第三方前端依赖的开放科研目录。GitHub 为内容与版本的主仓库；dist 可以部署到 GitHub Pages 或其他静态托管服务。

## 当前内容

两份原始 Excel 清单共32条，按官方链接去重后31篇独立文献，其中16篇前沿文献、16篇方法文献（黄河水文经济模型交叉收录）。另有6个数据入口、4个论文案例、3个政策报告入口。网站仅发布经整理的资料，原始研究笔记、同步状态和内部检查报告保留在本地。公式、图片等请查阅原文件。未上传原始论文全文或期刊图片。

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

## 手动更新与权限

公开站点仅支持浏览、搜索、收藏和导出。已移除公开页面的编辑、新增、导入及本地草稿覆盖功能。旧版浏览器存储中的草稿不再影响展示内容。

“所有者维护”链接打开GitHub的dist/catalog.json编辑页，由GitHub验证登录和仓库写入权限。当前仓库具有写入权限的账户仅wangjunbo11；其他访客即使打开链接，也不能修改本仓库。公开仓库允许他人阅读、下载及fork副本，副本不会改动正式网站。

所有者登录GitHub后可编辑catalog.json（文献、数据、政策等）或reviews.json（综述结构与正文），提交main分支后自动生成页面并发布。已授权的自动维护仍通过所有者授权操作。

## 定期更新

仓库启用后 `.github/workflows/discover.yml` 每日北京时间22:30检索最近45天的Crossref论文，按DOI与正式目录去重，写入候选池并发布。候选写入dist/candidates.json；所有者通过GitHub检查候选、补齐导读后更新正式目录。该流程不需要API密钥或AI付费调用，不自动生成论文摘要。仓库Actions需开启且允许工作流写入；平台可能延迟计划任务，公共仓库长期无活动时也可能停用计划任务。接口失败时工作流报告失败，保留正式资料不变。

已有ChatGPT Nexus任务可以继续用于研究与导读；目前尚无自动读取该ChatGPT任务并同步GitHub的连接，不声称两者已经互通。

## 核验

`python3 scripts/validate.py` 检查目录结构、编号、链接协议和必要文件。脚本不证明官方链接在线、元数据准确、所有地区可访问。自动检索首次运行需联网，当前尚未运行线上流程。


## 2026-11-17 第二版

综述按原文生成3个Part、6章、31节，共41个HTML页面；不再显示文本文件归档卡片。31篇文献补充背景、方法、结论、启示，并各有独立页面。政策新增全球4项、国内4项，连同原有机构报告共11条，支持范围筛选。展示界面移除核验状态字样，后台记录继续保留来源管理信息。

内容修改后执行 `python3 scripts/build_pages.py` 再执行 `python3 scripts/validate.py`；GitHub发布和镜像工作流也执行此生成步骤。分节与表格保存在dist/reviews.json；旧版笔记全文归档已从公开文件中移除。

大陆镜像流程见 MAINLAND-MIRROR.md。镜像目前未上线，需实际云账户、域名、DNS与HTTPS配置。


## 每日更新与摘要

本项目的Codex维护任务每天北京时间23:00执行，寻找并核验优质Nexus文献、案例、数据和政策，通过后自动提交和发布。GitHub候选检索工作流每天22:30预先抓取文献元数据，两者调度时间可能延迟；正式收录由维护任务核实来源和相关性。

每篇文献卡片默认展开摘要，可点击摘要标题收起。现有摘要为基于课题组材料的中文概述，明确标注，与出版商原文摘要区分；新增记录需提供abstract{text,kind,source}。期刊优先列表在config/journals.json；此列表用于来源优先级，不声称固定分区或影响因子。


## 本地文档同步与引用

每日23:00任务同时执行 `python3 scripts/sync_local_documents.py`，扫描项目上一级研究目录中的Word、Excel、PDF等源文件，以SHA-256检测内容更新，忽略网站目录及Word锁文件。本地.local/source-state.json记录同步基线；非综述文件变化进入pendingFiles，由维护任务整理后清除。删除不直接导致线上资料删除。原始文档只读。

综述导入根据Word编号层级识别章和节，将有标题或无标题的文末连续APA书目提取至dist/references.json。正文作者—年份引用链接至本节参考文献，references.html提供全局书目及引用位置回链。同作者同年条目仅在研究对象明确时区分，否则记录本地.local/citation-audit.json；正文引文在书目缺失时不臆造对应。

更新综述后运行 `python3 scripts/sync_local_documents.py --force`、`python3 -m unittest discover -s tests`、`python3 scripts/build_pages.py`、`python3 scripts/validate.py`。云端构建使用已同步JSON，不直接读取本地Word。


## 公开发布保护

公开文件不包含旧笔记全文归档、本地文件清单和内部引用检查报告；这些资料只保存在被Git忽略的.local目录或仓库之外的本地备份。提交使用GitHub隐藏邮箱。发布前执行python3 scripts/check_publication.py，阻止私密文件路径与常见凭证被加入公开目录；CI构建也执行同一检查。GitHub密钥扫描与推送保护已开启。工作流依赖固定完整SHA，并将写入权限限定到实际需要的作业。
