# encoding=utf-8
import jieba
import jieba.posseg as pseg

def test_chinese_seg():
    strs = ["我建议患者每日服用布洛芬8袋,并且需要9粒地黄丸.",
            "需要坚持9袋布洛芬,和5粒山楂丸,以及甘草片3粒,并且需要4袋蒙脱石散."]
    for str in strs:
        words = pseg.cut(str, use_paddle=True)
        for word, flag in words:
            print('%s %s' % (word, flag))



def test_english_seg():
    str = "On Dec. 7, 2021, more than a dozen surgeons convened a meeting at their hospital, HCA Florida Bayonet Point in Hudson, Florida. Their concerns about patient safety at the 290-bed acute care facility owned by HCA Healthcare Inc. had been intensifying for months and the doctors had requested the meeting to push management to address their complaints. "
    # seg_list = jieba.cut(str, cut_all=True)
    # print("Full Mode: " + "/ ".join(seg_list))  # 全模式
    # seg_list = jieba.cut(str, cut_all=False)
    # print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
    seg_list = jieba.cut(str)  # 默认是精确模式
    print(", ".join(seg_list))
    # seg_list = jieba.cut_for_search(str)  # 搜索引擎模式
    # print(", ".join(seg_list))

def test_custom_lib():
    str = "接下来对我们的专有名词进行测试"
    jieba.load_userdict("custom.lib")
    words = jieba.cut(str)
    print("Paddle Mode: " + '/'.join(list(words)))

if __name__ == "__main__":
    jieba.enable_paddle()  # 启动paddle模式。 0.40版之后开始支持，早期版本不支持
    test_chinese_seg()
    test_english_seg()
    test_custom_lib()
