# 模拟流水线运行日志

## 场景一：正常运行（成功）

### 运行时间
2026-06-02 10:00:00

### 执行结果：✅ 成功

```
[CI Pipeline] Starting build...

# 阶段1: 拉取代码
Checkout code: ✓ Done
  - Repository: demo-project
  - Branch: main
  - Commit: a1b2c3d

# 阶段2: 安装依赖
Set up Python: ✓ Done
  - Python version: 3.12.8
Install dependencies: ✓ Done
  - pip install pytest==8.0.0
  - 1 package installed

# 阶段3: 运行测试
Run tests: ✓ PASSED
  test_calculator.py::TestCalculator::test_add PASSED       [ 20%]
  test_calculator.py::TestCalculator::test_subtract PASSED      [ 40%]
  test_calculator.py::TestCalculator::test_multiply PASSED     [ 60%]
  test_calculator.py::TestCalculator::test_divide PASSED   [ 80%]
  test_calculator.py::TestCalculator::test_divide_by_zero PASSED [100%]

============================== 5 passed in 0.03s ===============================

# 质量门禁: ✓ 通过（测试失败即中止）
```

---

## 场景二：制造失败 - 依赖缺失

### 运行时间
2026-06-02 10:30:00

### 执行结果：❌ 失败

```
[CI Pipeline] Starting build...

# 阶段1: 拉取代码
Checkout code: ✓ Done

# 阶段2: 安装依赖
Set up Python: ✓ Done
Install dependencies: ❌ FAILED
  ERROR: Could not find a version that satisfies the requirement pytest==8.0.0
  ERROR: No matching distribution found for pytest==8.0.0

# 阶段3: 运行测试
Run tests: ⏸️ SKIPPED (due to previous failure)

# 失败原因分析
- 依赖版本号错误：pytest==8.0.0 不存在
- 正确版本：pytest==8.0.0 在当时实际已发布，但演示需要制造失败

# 修复方案
将 requirements.txt 中的 pytest 版本改为实际可用版本
```

### 修复操作
```diff
- pytest==8.0.0
+ pytest==8.0.0
```
（注：实际上 8.0.0 是正确的，这里模拟依赖缺失场景）

---

## 场景三：制造失败 - 测试断言错误

### 运行时间
2026-06-02 11:00:00

### 执行结果：❌ 失败

```
[CI Pipeline] Starting build...

# 阶段1: 拉取代码
Checkout code: ✓ Done

# 阶段2: 安装依赖
Install dependencies: ✓ Done

# 阶段3: 运行测试
Run tests: ❌ FAILED

============================= test session starts ==============================
platform win32 -- Python 3.12.8, pytest-8.0.0
collected 5 items

test_calculator.py::TestCalculator::test_add FAILED               [ 20%]
test_calculator.py::TestCalculator::test_subtract PASSED              [ 40%]
test_calculator.py::TestCalculator::test_multiply PASSED            [ 60%]
test_calculator.py::TestCalculator::test_divide PASSED              [ 80%]
test_calculator.py::TestCalculator::test_divide_by_zero PASSED        [100%]

========================== FAILURES =======================================
__________________________ TestCalculator.test_add __________________________

    def test_add(self):
        assert add(1, 2) == 4  # 故意修改为错误断言

E       AssertionError: assert 3 == 4
E        +  where 3 = add(1, 2)
============================== 1 failed in 0.02s ==============================

# 质量门禁: ✓ 生效（测试失败阻止后续阶段）

# 失败原因分析
- 测试断言错误：期望 1+2=4，但实际结果是 3
- 这是一个人为制造的失败，用于演示质量门禁

# 修复方案
修正测试断言为正确值：assert add(1, 2) == 3
```

### 修复操作
```diff
- assert add(1, 2) == 4
+ assert add(1, 2) == 3
```

---

## 场景四：修复后重新运行（成功）

### 运行时间
2026-06-02 11:30:00

### 执行结果：✅ 成功

```
[CI Pipeline] Starting build...

# 阶段1: 拉取代码
Checkout code: ✓ Done

# 阶段2: 安装依赖
Install dependencies: ✓ Done

# 阶段3: 运行测试
Run tests: ✓ PASSED
  test_calculator.py::TestCalculator::test_add PASSED       [ 20%]
  test_calculator.py::TestCalculator::test_subtract PASSED      [ 40%]
  test_calculator.py::TestCalculator::test_multiply PASSED     [ 60%]
  test_calculator.py::TestCalculator::test_divide PASSED         [ 80%]
  test_calculator.py::TestCalculator::test_divide_by_zero PASSED [100%]

============================== 5 passed in 0.03s ===============================

# 质量门禁: ✓ 通过
```

---

## 质量门禁说明

1. **测试失败中止**: 当 pytest 返回非零退出码时，流水线立即停止，不继续后续阶段
2. **依赖安装失败中止**: 如果 pip install 失败，后续测试阶段不会执行
3. **质量门禁价值**: 防止不合格代码进入构建或部署阶段

## AI 工具使用记录

| 场景 | AI 工具 | Prompt 摘要 | AI 输出摘要 | 人工验证 |
|------|--------|-------------|-------------|----------|
| 配置 GitHub Actions | 通义千问 | "帮我写一个 Python 项目的 GitHub Actions CI 配置" | 提供了 ci.yml 配置模板 | ✅ 已验证可用 |
| 失败日志分析 | 通义千问 | "解释这个 pytest 失败日志" | 说明了 AssertionError 原因 | ✅ 已验证正确 |
| 质量门禁设置 | 通义千问 | "GitHub Actions 如何设置质量门禁" | 说明使用 if: failure() 条件 | ✅ 已验证正确 |