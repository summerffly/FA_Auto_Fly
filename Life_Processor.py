import re
import datetime

class LifeProcessor:
    # 构造函数
    def __init__(self, file_path):
        self.file_path = file_path
        self.lines = []
        self.data = {}

    # 读取文件
    def read_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()

    # 解析文件
    def parse_file(self):
        i = 0
        while i < len(self.lines):
            line = self.lines[i].strip()
            # 检查是否为月份分类
            month_match = re.match(r'## (life\.M\d+)', line)
            if month_match:
                month_name = month_match.group(1).strip()
                # 初始化月份数据
                month_data = {
                    'salary': 0,
                    'expense': 0,
                    'balance': 0,
                    'salary_line_index': None,
                    'expense_line_index': None,
                    'balance_line_index': None,
                    'items': []
                }
                i += 1
                # 读取薪资/支出/结余行
                for _ in range(3):
                    if i >= len(self.lines):
                        break
                    total_line = self.lines[i].strip()
                    salary_match = re.match(r'>\s*(\d+月薪资)\s*:\s*([+-]?\d+)', total_line)
                    expense_match = re.match(r'>\s*(\d+月支出)\s*:\s*([+-]?\d+)', total_line)
                    balance_match = re.match(r'>\s*(\d+月结余)\s*:\s*([+-]?\d+)', total_line)
                    if salary_match:
                        month_data['salary_line_index'] = i
                        month_data['salary'] = int(salary_match.group(2))
                    elif expense_match:
                        month_data['expense_line_index'] = i
                        month_data['expense'] = int(expense_match.group(2))
                    elif balance_match:
                        month_data['balance_line_index'] = i
                        month_data['balance'] = int(balance_match.group(2))
                    i += 1

                # 读取项目明细
                while i < len(self.lines) and not self.lines[i].startswith('## '):
                    item_line = self.lines[i].strip()
                    item_match = re.match(r'`([+-]\s*\d+)`\s+(.+)', item_line)
                    if item_match:
                        amount = int(item_match.group(1).replace(' ', ''))
                        description = item_match.group(2).strip()
                        item = {
                            'amount': amount,
                            'description': description,
                            'line_index': i
                        }
                        month_data['items'].append(item)
                    i += 1
                self.data[month_name] = month_data
            else:
                i += 1

    def calculate_month(self):
        for month, details in self.data.items():
            # 计算薪资和支出
            income = details['salary']
            expense = sum(item['amount'] for item in details['items'])
            balance = income + expense
            # 更新计算结果
            details['calculated_salary'] = income
            details['calculated_expense'] = expense
            details['calculated_balance'] = balance

    def update_month(self):
        # 更新每个月份的薪资、支出和结余
        for month, details in self.data.items():
            # 更新薪资
            if details['salary_line_index'] is not None:
                self.lines[details['salary_line_index']] = f"> {month[-2:]}月薪资 : {details['calculated_salary']}\n"
            # 更新支出
            if details['expense_line_index'] is not None:
                self.lines[details['expense_line_index']] = f"> {month[-2:]}月支出 : {details['calculated_expense']}\n"
            # 更新结余
            if details['balance_line_index'] is not None:
                self.lines[details['balance_line_index']] = f"> {month[-2:]}月结余 : {details['calculated_balance']}\n"

        # 更新更新时间
        update_time_updated = False
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for i, line in enumerate(self.lines):
            if line.strip().startswith('*Update Time :'):
                self.lines[i] = f'*Update Time : {current_time}*\n'
                update_time_updated = True
                break
        
        # 如果没有更新时间，则添加到文件末尾
        if not update_time_updated:
            self.lines.append(f'\n*Update Time : {current_time}*\n')

    def modify_item(self, month, description, new_amount):
        month_key = f'life.M{month:0>2}'
        if month_key not in self.data:
            print(f"未找到月份：{month_key}")
            return

        month_data = self.data[month_key]
        # 查找匹配描述的项目
        item_found = False
        for item in month_data['items']:
            if description in item['description']:
                item['amount'] = new_amount  # 更新金额
                # 更新文件中的对应行
                sign = '+' if new_amount >= 0 else '-'
                self.lines[item['line_index']] = f'`{sign} {abs(new_amount)}` {item['description']}\n'
                item_found = True
                break

        if not item_found:
            print(f"未找到描述为“{description}”的项目")
            return

        # 修改后重新计算并写入
        self.calculate_month()
        self.update_month()
        self.write_file()
        print(f"已更新 {month_key} 中“{description}”的金额为 {new_amount}")
    
    # 写入文件
    def write_file(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.writelines(self.lines)

    def update(self):
        self.read_file()
        self.parse_file()
        self.calculate_month()
        self.update_month()
        self.write_file()
        print('life文件已更新')
