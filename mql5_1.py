from Chan import CChan
from ChanConfig import CChanConfig
from Common.CEnum import AUTYPE, DATA_SRC, KL_TYPE
from Plot.AnimatePlotDriver import CAnimateDriver
from Plot.PlotDriver import CPlotDriver
from Plot.PlotDriver_ICT import CPlotDriver_ICT


def do_one(code, begin_time, end_time, lv_list, data_src):
    config = CChanConfig({
        "bi_strict": True,
        "trigger_step": False,
        "skip_step": 0,
        "divergence_rate": float("inf"),
        "bsp2_follow_1": False,
        "bsp3_follow_1": False,
        "min_zs_cnt": 0,
        "bs1_peak": False,
        "macd_algo": "peak",
        "bs_type": '1,2,3a',
        # "bs_type": '1,2,3a,1p,2s,3b',
        "print_warning": True,
        "zs_algo": "normal",
        "max_kl_inconsistent_cnt": 12
    })
    plot_config = {
        "plot_kline": True,
        "plot_kline_combine": False,
        "plot_bi": True,
        "plot_seg": True,
        "plot_eigen": False,
        "plot_zs": True,
        "plot_macd": True,
        "plot_mean": False,
        "plot_channel": False,
        "plot_bsp": True,
        "plot_extrainfo": False,
        "plot_demark": False,
        "plot_marker": False,
        "plot_rsi": False,
        "plot_kdj": False,
    }
    plot_para = {
        "seg": {
            # "plot_trendline": True,
        },
        "bi": {
            # "show_num": True,
            # "disp_end": True,
        },
        "figure": {
            "x_range": 1000,
        },
        "marker": {
            # "markers": {  # text, position, color
            #     '2023/06/01': ('marker here', 'up', 'red'),
            #     '2023/06/08': ('marker here', 'down')
            # },
        }
    }
    chan = CChan(
        code=code,
        begin_time=begin_time,
        end_time=end_time,
        data_src=data_src,
        lv_list=lv_list,
        config=config,
        autype=AUTYPE.QFQ,
    )
    if not config.trigger_step:
        plot_driver = CPlotDriver_ICT(
            chan,
            plot_config=plot_config,
            plot_para=plot_para,
        )
        # plot_driver.figure.show()
        # plot_driver.save2img('test_btcsd_H4.png')
        plot_driver.save2img('./peter/test_' + code + '_+M5+.png')
        # plot_driver.save2img('test_btcsd_W1.png')
    else:
        CAnimateDriver(
            chan,
            plot_config=plot_config,
            plot_para=plot_para,
        )


if __name__ == "__main__":
    # code = "EURUSD"
    my_begin_time = "2024-09-10 00:00:00"
    my_end_time = "2024-10-03 00:00:00"
    # my_lv_list = [KL_TYPE.K_DAY]
    # my_lv_list = [KL_TYPE.K_H4]
    my_lv_list = [KL_TYPE.K_15M]
    my_lv_list = [KL_TYPE.K_5M]
    # my_lv_list = [KL_TYPE.K_DAY,KL_TYPE.K_H4]

    currency_pairs = ["GBPUSD", "GBPAUD", "GBPJPY", "GBPCAD", "GBPNZD", "GBPCHF", "EURUSD", "EURGBP", "EURCAD", "EURJPY",
                      "EURAUD", "EURNZD", "EURCHF", "AUDUSD", "AUDNZD", "AUDCAD", "AUDJPY", "AUDCHF", "NZDUSD", "NZDCAD",
                      "NZDCHF", "NZDJPY", "CADCHF", "CADJPY", "CHFJPY", "USDCAD", "USDCHF", "USDJPY", "XAUUSD", "XAGUSD",
                      "ETHUSD", "BTCUSD"]

    # todo debug peter
    # currency_pairs = ["GBPCHF"]
    # currency_pairs = ["AUDCAD"]
    # currency_pairs = ["EURGBP"]
    # currency_pairs = ["XAUUSD"]
    # currency_pairs = ["GBPAUD"]

    for pair in currency_pairs:
        print(f"----{pair}--{my_begin_time}---{my_end_time}-----")
        do_one(pair, my_begin_time, my_end_time, my_lv_list, DATA_SRC.MQL5)
        print(f"--------------------------\n")
