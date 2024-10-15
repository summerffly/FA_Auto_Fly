import re
import datetime

class SMProcessor:
    def __init__(self, file_path, sm_name):
        self.file_path = file_path
        self.sm_name = sm_name
        self.data = {}
        self.lines = []
        self.overall_total = 0

    def parse_accounting_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()

        i = 0
        while i < len(self.lines):
            line = self.lines[i]
            # 检查是否为分月标题
            category_match = re.match(r'## (.+)', line)
            if category_match:
                category_name = category_match.group(1).strip()
                # 找到分月总额行
                i += 1
                total_line_index = i
                total_line = self.lines[i]
                total_match = re.match(r'> ([+-]?\d+)', total_line)
                category_total = int(total_match.group(1)) if total_match else 0
                items = []
                i += 1
                # 记录分月的起始行号
                category_start_index = i
                # 读取分月下的项目
                while i < len(self.lines) and not self.lines[i].startswith('##') and not self.lines[i].startswith('*Update Time :'):
                    item_line = self.lines[i]
                    item_match = re.match(r'`([+-]\s*\d+)` (.+)', item_line)
                    if item_match:
                        amount = int(item_match.group(1).replace(' ', ''))
                        description = item_match.group(2).strip()
                        items.append({'amount': amount, 'description': description})
                    i += 1
                # 记录分月的结束行号
                category_end_index = i - 1
                self.data[category_name] = {
                    'total': category_total,
                    'items': items,
                    'total_line_index': total_line_index,
                    'start_index': category_start_index,
                    'end_index': category_end_index
                }
            else:
                i += 1

    def calculate_totals(self):
        self.overall_total = 0
        for category, details in self.data.items():
            category_actual_total = sum(item['amount'] for item in details['items'])
            self.data[category]['calculated_total'] = category_actual_total
            self.overall_total += category_actual_total

    def update_total_in_file(self):
        # 更新每个分月的总额
        for category, details in self.data.items():
            total_line_index = details['total_line_index']
            calculated_total = details['calculated_total']
            # 更新分月总额行
            self.lines[total_line_index] = f'> {calculated_total}\n'

        # 更新时间
        total_updated = False
        update_time_updated = False
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for i, line in enumerate(self.lines):
            if line.strip().startswith('*Update Time :'):
                self.lines[i] = f'*Update Time : {current_time}*\n'
                update_time_updated = True

        # 如果没有更新时间，则添加
        if not update_time_updated:
            self.lines.append(f'\n*Update Time : {current_time}*\n')

        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.writelines(self.lines)

    def run(self):
        self.parse_accounting_file()
        self.calculate_totals()
        self.update_total_in_file()
        print(f'{self.sm_name} 总金额为：{self.overall_total}')
