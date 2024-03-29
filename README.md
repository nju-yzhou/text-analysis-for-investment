# text-analysis-for-investment
这是我的毕业论文《基于文本分析的公司投资战略研究》的相关代码，持续更新中....

## 依赖安装

为了复现论文中的内容，请先用下述代码安装依赖:

```bash
pip install -r requirements.txt
```

## 技术路径

我计划使用两条技术路径，如下图所示：

![](/Users/zmxing/Downloads/zythesis/pictures/method.png)

## 代码解释

`get_pdf_data.py`会从上交所爬取自1999年以来所有A股上市公司的年报，并存储在`./text-analysis-for-investment/pdfs`中。其实现流程如下：

![](/Users/zmxing/Downloads/zythesis/pictures/spider.png)

这里借鉴了开源代码库[shreport](https://github.com/hiDaDeng/shreport?tab=readme-ov-file)。



`pdf_2_text.py`可以将上述代码得到的pdf转化为txt文件，并存储在`./text-analysis-for-investment/rawtxts`中，转化效果如下图所示：

![](/Users/zmxing/Downloads/zythesis/pictures/pdf2txt.png)

这里借鉴了ChatGLM金融挑战赛中的[PDFprocessor](https://github.com/MetaGLM/FinGLM/tree/main/tools/pdf_to_txt)。



`extract_MDA.py`可以将上述粗糙的txt文件中的mda部分提取出来，并存储在`./text-analysis-for-investment/mdatxts`中。



`word2vec.py`将训练一个word2vec模型，利用该模型我们可以通过`get_keyword.py`获取所有相似词，并最终通过`measure.py`进行度量。这就完成了第一条路径。

