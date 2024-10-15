# PE白皮书

- parse_accounting_file(self)
读取文件内容并解析
使用正则表达式匹配分类标题、分类总额、项目金额和描述
将解析的数据存储在 self.data 中，结构如下：
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
