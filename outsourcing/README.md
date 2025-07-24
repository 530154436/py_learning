
`python-docx-template` 是一个基于 python-docx 和 Jinja2 构建的库，旨在简化 Word 文档（.docx）模板的创建与数据填充。

其核心思想是：先使用 Microsoft Word 设计一个复杂的文档模板，插入图片、表格、页眉页脚等内容，然后在合适的位置添加 Jinja2 风格的变量和控制标签，保存为 .docx 文件即可作为模板使用。之后，只需提供相应的数据变量，即可通过代码自动生成多个定制化的 Word 文档。

+ 使用限制：由于 Word 文档的结构限制，常规的 Jinja2 标签应放在同一文本段（run）内，不能跨段落或表格行使用。如需控制更复杂的结构（如段落、表格行等），需使用特殊的标签语法。
+ 小知识：在 Word 中，“run”指的是具有相同格式的一段连续文本。如果段落中格式发生变化（如加粗、字体变化），Word 会将其拆分为多个“run”。

> [官方GitHub](https://github.com/elapouya/python-docx-template)、[官方文档](https://docxtpl.readthedocs.io/en/latest/)


[Python 使用DocxTemplate模板实现将数据写入word中](https://blog.csdn.net/Hushi1706IT/article/details/129650996)<br>

```shell
pip install openpyxl docxtpl pandas matplotlib pydantic
```