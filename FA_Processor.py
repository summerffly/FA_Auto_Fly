import re
import datetime

class FAProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.lines = []
        self.initial_wealth = 0
        self.categories = {}
        self.months = {}
        self.current_wealth = 0
        self.disposable_wealth = 0
        self.assets = {}
        self.update_time = ''
        self.other_items = []
    
    def read_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()

    def parse_file(self):        
        i = 0
        while i < len(self.lines):
            line = self.lines[i].strip()
            
            # 初始财富
            if line.startswith('初始财富'):
                wealth_match = re.match(r'初始财富\s*:\s*([+-]?\d+)', line)
                if wealth_match:
                    self.initial_wealth = int(wealth_match.group(1))
                i += 1
                continue
            
            # 分类金额
            category_match = re.match(r'##\s+(\w+)', line)
            if category_match:
                category_name = category_match.group(1)
                i += 1
                # 读取下一个以 '>' 开头的金额
                if i < len(self.lines):
                    amount_line = self.lines[i].strip()
                    amount_match = re.match(r'>\s*([+-]?\d+)', amount_line)
                    if amount_match:
                        amount = int(amount_match.group(1))
                        self.categories[category_name] = amount
                        i += 1
                        continue
            # 月份数据
            month_match = re.match(r'##\s+(life\.M\d+)', line)
            if month_match:
                month_name = month_match.group(1)
                month_data = {}
                for _ in range(3):
                    i += 1
                    if i >= len(self.lines):
                        break
                    total_line = self.lines[i].strip()
                    salary_match = re.match(r'>\s*(\d+月薪资)\s*:\s*([+-]?\d+)', total_line)
                    expense_match = re.match(r'>\s*(\d+月支出)\s*:\s*([+-]?\d+)', total_line)
                    balance_match = re.match(r'>\s*(\d+月结余)\s*:\s*([+-]?\d+)', total_line)
                    if salary_match:
                        month_data['salary'] = int(salary_match.group(2))
                    elif expense_match:
                        month_data['expense'] = int(expense_match.group(2))
                    elif balance_match:
                        month_data['balance'] = int(balance_match.group(2))
                self.months[month_name] = month_data
                i += 1
                continue
            # 当前财富
            if line.startswith('当前财富'):
                wealth_match = re.match(r'当前财富\s*:\s*([+-]?\d+)', line)
                if wealth_match:
                    self.current_wealth = int(wealth_match.group(1))
                i += 1
                continue
            # 可支配财富
            if line.startswith('可支配财富'):
                disposable_match = re.match(r'可支配财富\s*:\s*([+-]?\d+)', line)
                if disposable_match:
                    self.disposable_wealth = int(disposable_match.group(1))
                i += 1
                # 读取资产列表
                while i < len(self.lines):
                    asset_line = self.lines[i].strip()
                    if asset_line.startswith('*Update Time'):
                        break
                    asset_match = re.match(r'(.+?)\s*:\s*([+-]?\d+)', asset_line)
                    if asset_match:
                        asset_name = asset_match.group(1)
                        asset_amount = int(asset_match.group(2))
                        self.assets[asset_name] = asset_amount
                    i += 1
                continue
            # 更新时间
            if line.startswith('*Update Time'):
                time_match = re.match(r'\*Update Time\s*:\s*(.+)', line)
                if time_match:
                    self.update_time = time_match.group(1)
                i += 1
                continue
            # 其他项目
            item_match = re.match(r'`([+-]\s*\d+)`\s+(.+)', line)
            if item_match:
                amount = int(item_match.group(1).replace(' ', ''))
                description = item_match.group(2)
                self.other_items.append({'amount': amount, 'description': description})
                i += 1
                continue
            else:
                i += 1

    def calculate_totals(self):
        # 计算总分类金额
        total_categories = sum(self.categories.values())
        # 计算总月度结余
        total_monthly_balance = sum(month['balance'] for month in self.months.values())
        # 计算其他项目总额
        total_other_items = sum(item['amount'] for item in self.other_items)
        # 计算当前财富
        calculated_current_wealth = self.initial_wealth + total_categories + total_monthly_balance + total_other_items
        # 计算资产总额
        total_assets = sum(self.assets.values())
        # 计算可支配财富
        calculated_disposable_wealth = total_assets
        # 存储计算结果
        self.calculated_results = {
            'total_categories': total_categories,
            'total_monthly_balance': total_monthly_balance,
            'total_other_items': total_other_items,
            'calculated_current_wealth': calculated_current_wealth,
            'total_assets': total_assets,
            'calculated_disposable_wealth': calculated_disposable_wealth
        }

    def generate_report(self):
        print("初始财富:", self.initial_wealth)
        print("分类金额:")
        for category, amount in self.categories.items():
            print(f"  {category}: {amount}")
        print("月份结余:")
        for month, data in self.months.items():
            print(f"  {month}: 薪资={data.get('salary', 0)}, 支出={data.get('expense', 0)}, 结余={data.get('balance', 0)}")
        print("其他项目:")
        for item in self.other_items:
            print(f"  {item['description']}: {item['amount']}")
        print("当前财富:", self.current_wealth)
        print("计算得到的当前财富:", self.calculated_results['calculated_current_wealth'])
        print("资产列表:")
        for asset, amount in self.assets.items():
            print(f"  {asset}: {amount}")
        print("可支配财富:", self.disposable_wealth)
        print("计算得到的可支配财富:", self.calculated_results['calculated_disposable_wealth'])
        print("更新时间:", self.update_time)
    
    def run(self):
        self.read_file()
        self.parse_file()
        self.calculate_totals()
        self.generate_report()
