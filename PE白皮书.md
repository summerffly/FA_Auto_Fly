# PE白皮书

## 安装python依赖包
- colorama
- pyinstaller

## 打包命令
pyinstaller --onefile FA_Auto_PE.py

## 工程白皮书

### 解析TT文件
{
    '分类名称': {
        'total': 分类总额（文件中的值）,
        'items': [
            {'amount': 项目金额, 'description': 描述},
            ...
        ],
        'total_line_index': 分类总额所在行的索引,
        'start_index': 分类项目开始行的索引,
        'end_index': 分类项目结束行的索引
    },
    ...
}

### 解析life文件
{
    '分类名称': {
        'total': 分类总额（文件中的值）,
        'items': [
            {'amount': 项目金额, 'description': 描述},
            ...
        ],
    },
    ...
}