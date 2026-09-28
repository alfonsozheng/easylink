# 魂斗罗 - RETURNS / CONTRA - RETURNS

一款经典魂斗罗（Contra）风格的横版卷轴射击游戏，使用 **Python + Pygame** 开发。

全部美术与音效均为**程序化生成**，不依赖任何外部素材文件。

---

## 系统要求

- **操作系统**: macOS (Apple Silicon / Intel), Linux, Windows
- **Python**: 3.9+
- **依赖**: Pygame 2.5+

## 安装与启动

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 2. 启动游戏

```bash
python main.py
```

---

## 操作说明

| 按键 | 功能 |
|------|------|
| ← → / A D | 左右移动 |
| ↑ / W | 仰角射击（站立时） |
| ↓ / S | 趴下 |
| Space | 跳跃 |
| J / Z | 射击（按住连发） |
| P / Esc | 暂停 / 继续 |
| Enter | 开始游戏 / 确认 |
| Esc (标题/结束画面) | 退出游戏 |

---

## 游戏内容

### 关卡

- **第 1 关 - 丛林前线**: 穿越绿色丛林，击败丛林 Boss
- **第 2 关 - 军事基地**: 攻入敌方基地，击败最终 Boss

### 武器

| 图标 | 名称 | 效果 |
|------|------|------|
| 默认 | 普通枪 | 单发直线，均衡射速 |
| S | 散弹枪 | 扇形 3 发散弹 |
| M | 机枪 | 极高射速连射 |
| R | 加速弹 | 大威力子弹 |

### 道具

- **S / M / R**: 拾取切换对应武器
- **1UP**: 增加一条生命
- **500**: 加分道具

---

## 项目结构

```
├── main.py              # 游戏入口
├── requirements.txt     # Python 依赖
├── README.md            # 本文件
├── src/
│   ├── game.py          # 游戏主循环与状态管理
│   ├── player.py        # 玩家角色
│   ├── enemy.py         # 敌人（巡逻兵/哨兵）
│   ├── boss.py          # Boss（丛林/基地）
│   ├── bullet.py        # 子弹
│   ├── weapon.py        # 武器配置
│   ├── item.py          # 道具
│   ├── level.py         # 关卡加载与管理
│   ├── camera.py        # 卷轴摄像机
│   ├── hud.py           # HUD 渲染
│   └── ui.py            # 标题/暂停/Game Over/通关界面
├── levels/
│   ├── level1.json      # 第 1 关数据
│   └── level2.json      # 第 2 关数据
└── assets/
    ├── sprites.py        # 程序化生成精灵
    └── sounds.py         # 程序化生成音效
```

---

## 技术细节

- 引擎: Pygame 2.x
- 分辨率: 800×600 窗口模式
- 帧率: 目标 60 FPS
- 碰撞检测: AABB（轴对齐矩形碰撞）
- 所有资源均为程序化运行时生成

## 许可

本项目仅供学习与演示用途。
