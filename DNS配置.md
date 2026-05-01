# DNS 配置指南 - anhemeg.top

## Vercel DNS 配置

登录 Vercel 后，在项目 Settings → Domains 中添加域名，会显示具体需要配置的 DNS 记录。

### 通常需要添加的记录：

| 记录类型 | 名称 | 值 | 说明 |
|---------|------|-----|------|
| A | @ | 76.76.21.21 | 指向 Vercel |
| CNAME | www | cname.vercel-dns.com | Vercel 域名 |

### 具体步骤：

#### 1. 在域名注册商（NameSilo）添加记录
1. 登录 NameSilo 账户
2. 进入 Domain Manager
3. 选择 anhemeg.top 域名
4. 点击 "DNS Records"
5. 添加以下记录：

```
Type    Host    Value                   TTL
A       @       76.76.21.21             3600
CNAME   www     cname.vercel-dns.com    3600
```

#### 2. 等待生效
- DNS 更改通常在 10 分钟 - 24 小时内生效
- 可以使用以下命令验证：
```bash
# Windows
nslookup anhemeg.top

# Mac/Linux
dig anhemeg.top
```

#### 3. Vercel 验证
1. 在 Vercel Dashboard 的 Domains 页面
2. 等待 "Valid Configuration" 状态
3. 点击 "Check DNS Configuration" 手动检查

---

## 常见问题

### Q: 为什么添加了 A 记录还要 CNAME？
- A 记录用于根域名（@）
- CNAME 用于 www 子域名
- 两者都配置才能完整访问

### Q: DNS 已添加但还是显示未验证？
- 等待 24-48 小时
- 确认记录值完全一致
- 检查是否有冲突的记录

### Q: HTTPS 证书多久生效？
- Vercel 会自动申请 Let's Encrypt 证书
- 通常在域名验证通过后 24 小时内完成
- 无需手动操作

---

## 备用：Cloudflare DNS（推荐）

如果 NameSilo DNS 不稳定，可以使用 Cloudflare 免费 DNS：

1. 注册 [Cloudflare](https://cloudflare.com)
2. 添加域名 anhemeg.top
3. 将 NameSilo 的 DNS 服务器改为 Cloudflare 提供的服务器
4. 在 Cloudflare 添加 DNS 记录：
   - A 记录：@ → 76.76.21.21
   - CNAME：www → cname.vercel-dns.com
   - 代理状态：DNS only（灰色云朵）

---

## DNS 配置检查清单

- [ ] 添加 A 记录（@）
- [ ] 添加 CNAME 记录（www）
- [ ] 确认记录值正确
- [ ] 等待 10-30 分钟
- [ ] 在 Vercel 点击 "Check DNS"
- [ ] 确认状态变为 Valid
- [ ] 测试 https://anhemeg.top
- [ ] 测试 https://www.anhemeg.top
