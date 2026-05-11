## 介绍

此仓库管理了某 mc 航空学服务器的整合包变更（当然，仅限于配置文件）

使用的是 [HMCL](https://github.com/HMCL-dev/HMCL) 的服务端自动更新整合包，具体信息可参考 HMCL 文档的 [服务端自动更新整合包制作教程](https://docs.hmcl.net/modpack/serverpack.html)

## 使用

整合包使用方式：

HMCL 依次点开 实例列表 > 安装整合包 > 从互联网下载整合包

填入整合包链接：

- 完整整合包（因为包含了大量 voxy 缓存数据，完整整合包大小约为 4GB）

http://<此处插入地址>/modpack/server-manifest.json

- 轻量级整合包（去除了 voxy 和光影包等数据，大小只有几百 MB）

http://<此处插入地址>/modpack-lite/server-manifest.json

确定后即可自动下载导入，实例每次启动之后都会自动更新

## 变更

初始配置

- 小地图移动到右上角
- ysm 模型位置向下移动，避免遮挡 minihud
- 隐藏式字幕打开
- minihud 打开
  - fps 帧率显示
  - mc 格式化时间
  - 移动速度
- tweakeroo
  - 灵魂出窍 F8
  - 伽马值修改 F9
- 按键绑定
  - 取消 Iris 重新加载光影包的快捷键
  - Create 打开方块旋转菜单绑定到 `
- 资源包
  - 航空学汉化

包含主世界和下界预生成之后的 voxy 数据和地图数据
