# 🎉 lottery_party

一个适用于年会的抽奖程序，由 **PyQt5** 支持。

---

## 🚀 功能简介
- **背景图片**：默认使用同目录下的 `lottery_bg.png`。
- **头像滚动**：将头像图片放入同目录的 `avatar` 文件夹中，头像文件名需与人名一致。
- **抽奖提示**：抽奖人数超过剩余人数时会弹出提示。
- **结果保存**：抽奖结果会保存在文件 `名单.txt` 中。
- **重置功能**：点击“重置”按钮可清空抽奖名单。

---

## 🛠 安装与运行

1. 安装依赖：
   ```bash
   pip install PyQt5
   ```

2. 确保以下文件和目录存在：
   - `lottery_bg.png`（背景图片）
   - `avatar/` 文件夹（存放头像图片）

3. 运行程序：
   ```bash
   python lottery_image.py
   ```

---

## 📂 文件结构

```
lottery_party/
├── lottery_image.py       # 主程序
├── config.json            # 配置文件
├── lottery_bg.png         # 背景图片
├── avatar/                # 存放头像图片
│   ├── 张三.png
│   ├── 李四.png
│   └── ...
└── 名单.txt              # 抽奖结果保存文件
```

---

## 💡 使用说明

1. **头像命名规则**：  
   将头像图片放在 `avatar` 文件夹下，文件名需与对应人名一致，例如：
   ```
   avatar/
   ├── 张三.png
   ├── 李四.png
   ```

2. **运行抽奖程序**：  
   - 点击开始按钮滚动头像。
   - 停止滚动后，选中的人会被记录到 `名单.txt` 中。
   - 如果抽奖人数超过剩余人数，程序会提示错误信息。

3. **重置名单**：  
   点击“重置”按钮即可清空 `名单.txt`。

---

## 🎉 欢迎贡献

欢迎通过 Pull Request（PR）为本项目贡献代码或优化功能！😊

---

## 🖼 示例截图

![截图](https://github.com/user-attachments/assets/368399ba-b567-44e4-a3d5-1466ee3ddd03)


---

## 📄 许可证

本项目使用 [MIT License](LICENSE)。
```

### **特点**
- 使用了表情符号（如 🎉、🚀）让标题更醒目。
- 文件结构说明清晰，便于用户了解项目文件的组织方式。
- 将使用说明拆分为多步，条理分明。
- 提供了欢迎贡献和许可证信息，增加了专业性。

如果需要进一步美化或调整内容，随时告诉我！
