# 上海安禾美阁医疗美容官网

基于 anhemeg.top 域名的静态SEO网站

## 网站结构

```
anhemeg-site/
├── index.html          # 首页
├── about.html          # 机构介绍
├── doctors.html        # 医生团队
├── services.html       # 服务项目
├── news.html           # 资讯中心
├── contact.html        # 联系我们
├── doctors/            # 医生详情页 (29个)
├── guide/              # 就诊指南
│   ├── booking.html    # 预约挂号
│   ├── transport.html  # 交通指南
│   ├── flow.html       # 就诊流程
│   └── notice.html     # 注意事项
├── news/               # 资讯文章 (89篇)
├── styles.css          # 样式文件
├── sitemap.xml         # 网站地图
├── robots.txt          # 爬虫规则
└── vercel.json         # Vercel配置
```

## SEO配置

- sitemap.xml: 包含129个页面URL
- robots.txt: 允许所有爬虫
- 每个页面独立title/description/keywords
- Schema.org结构化数据

## 部署到Vercel

### 方法1: GitHub导入（推荐）

1. 将此仓库上传到GitHub
2. 访问 [vercel.com](https://vercel.com)
3. 使用GitHub账号登录
4. 点击 "Import Project"
5. 选择此仓库
6. 点击 "Deploy"

### 方法2: Vercel CLI

```bash
npm i -g vercel
cd anhemeg-site
vercel
```

## 绑定域名 anhemeg.top

1. Vercel部署完成后，进入项目设置
2. 点击 "Domains"
3. 输入 `anhemeg.top`
4. Vercel会给出验证记录

## NameSilo DNS配置

在NameSilo中添加以下记录：

| Type | Name | Value |
|------|------|-------|
| CNAME | www | cname.vercel-dns.com |
| A | @ | 76.76.21.21 |

等待DNS生效（通常10分钟-48小时）

## 搜索引擎提交

网站上线后，在以下平台提交sitemap:
- 百度搜索资源平台: https://ziyuan.baidu.com
- Google Search Console: https://search.google.com/search-console
- 搜狗站长平台: https://zhanzhang.sogou.com

---
© 2024 上海安禾美阁医疗美容机构
