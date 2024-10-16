from colorama import init, Fore, Style
from TT_Processor import TTProcessor
from SM_Processor import SMProcessor
from Life_Processor import LifeProcessor
from FA_Processor import FAProcessor

def print_logo():
    init(autoreset=True)
    print(Fore.CYAN + '****************************************')
    print(Fore.CYAN + '***                                  ***')
    pre_text = Fore.CYAN + '***            '
    fa_text = Fore.GREEN + Style.BRIGHT + 'FA_Auto_PE'
    post_text = Fore.CYAN + Style.NORMAL + '            ***'
    print(pre_text + fa_text + post_text)
    pre_text = Fore.CYAN + '***          '
    fa_text = Fore.GREEN + Style.BRIGHT + 'Version: Alpha'
    post_text = Fore.CYAN + Style.NORMAL + '          ***'
    print(pre_text + fa_text + post_text)
    print(Fore.CYAN + '***                                  ***')
    print(Fore.CYAN + '****************************************')

if __name__ == '__main__':
    print_logo()

    tt_dk_path = './DK.md'
    tt_ns_path = './NS.md'
    tt_travel_path = './travel.md'
    tt_box_path = './BOX.md'
    tt_dk_processor = TTProcessor(tt_dk_path, 'DK')
    tt_ns_processor = TTProcessor(tt_ns_path, 'NS')
    tt_travel_processor = TTProcessor(tt_travel_path, 'travel')
    tt_box_processor = TTProcessor(tt_box_path, 'BOX')
    tt_dk_processor.run()
    tt_ns_processor.run()
    tt_travel_processor.run()
    tt_box_processor.run()

    sm_keep_path = './KEEP.M.md'
    sm_dgtler_path = './DGtler.M.md'
    sm_tb_path = './TB.M.md'
    sm_keep_processor = SMProcessor(sm_keep_path, 'KEEP.M')
    sm_dgtler_processor = SMProcessor(sm_dgtler_path, 'DGtler.M')
    sm_tb_processor = SMProcessor(sm_tb_path, 'TB.M')
    sm_keep_processor.run()
    sm_dgtler_processor.run()
    sm_tb_processor.run()

    life_path = './life.M.md'
    life_processor = LifeProcessor(life_path)
    life_processor.run()
    #life_processor.modify_item(10, 'KEEP', -1000)

    #fa_sum_path = './FA_SUM.md'
    #fa_processor = FAProcessor(fa_sum_path)
    #fa_processor.run()
