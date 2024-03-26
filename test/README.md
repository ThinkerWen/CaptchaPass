# Test func

这个文件夹用来执行图形识别测试

### 目录介绍
_test_click.py_ 、_test_slide.py_ 两文件是主方法文件

_images_ 文件夹中存储的是待测试的图像

若需要增加图像，则添加到images文件夹中后，再修改main方法中的序号即可
```python
if __name__ == '__main__':
    for i in range(0, 5):   # 修改此处
        process(
            os.path.join(os.getcwd(), f"images/bg{i}.jpg"),
            os.path.join(os.getcwd(), f"images/front{i}.png")
        )
```

### 注
修改 _process_ 方法后，别忘记同步到 _main.py_ 文件中
### 缺陷
混淆度不高，或者颜色分明的图像识别都较为容易例如序号 **0、1、2**，但颜色与待匹配的front图像相似的，难以精确匹配，如序号 **3**
