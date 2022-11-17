# STERAePub++标准化模板<br/>
<b>～ePub自动化快速精排 for ver1.2.x～</b>
<br/><br/>

## 使用条件
- <b>适用工具：</b>Sigil 1.8.0+
- <b>适用对象：</b>以[《台灣 EPUB 3 製作指引》](https://github.com/dpublishing/epub3guide)为标准的ePub电子书源
- <b>目标类型：</b>横排中文（GBK）ePub电子书
- <b>靶向适配：</b>WebKit内核浏览器/多看阅读/Starrea/iBooks/Kindle
- <b>执行标准：</b>EPUB 3.0.1/XHTML 1.1/CSS 3.0/ECMAScript 5
<br/>

## 使用方法
*（部分条目相关说明请参[注意事项](#tips)）*

>### 前期准备
>- 将`插件`内的*zip*在Sigil插件管理中直接安装，无需解压
>- 将`自动化`内的*ini*导入Sigil搜索模板，将<b>「书源处理」</b>组剪切至搜索模板根目录
>- 将`自动化`内的*txt*复制至`C:\Users\用户名\AppData\Local\sigil-ebook\sigil`
>- 在Sigil首选项中勾选<b>「EPUB可以使用JavaScript」</b>选项
><br/>
>
>### 预处理
>- 打开`[书源].epub`
>- 检查`OEBPS/Images`，寻找可能是行内图的字符图、标题图等，多为*png*
>- 检查*xhtml*，用相应字符替换字符图，统一标题图格式以便后续替换
>- 检查`[目录页].xhtml`，确保目录链接至每个章节的第一个主文本*xhtml*中相应的id元素
><br/>
>
>### 自动化执行\#1
>- 删除`OEBPS/Styles`中的所有文件
>- 规范化重命名`OEBPS/Images`内的图片文件并删除多余图片
>- 选中`OEBPS/Text`的最后一个文件，通过<b>「添加现有文件」</b>将`素材`内的文件导入
>- 打开`insert.xhtml`，并按照如下格式填写`<body>`子节点：
>	<pre><code>&lt;mark class="rit-name"&gt;[标题]&lt;mark&gt;
>	&lt;mark class="rit-number"\&gt;[卷号]&lt;/mark\&gt;
>	&lt;mark class="rit-subname"\&gt;[副标题]&lt;/mark\&gt;
>	&lt;mark class="rit-author"\&gt;[作者]&lt;/mark\&gt;
>	&lt;mark class="rit-aut-illu"\&gt;[画师]&lt;/mark\&gt;
>	&lt;mark class="rit-intro"\&gt;&lt;/mark\&gt;
>	[简介]</code></pre>
>- 检查无误后保存*epub*
>- 打开*nav*后关闭其他标签页，运行<b>「自动执行列表1」</b>，等待运行完毕
><br/>
> 
>### 自动化执行#2
>- 选中`OEBPS/Text`中除*nav*外的所有文件，合并文件
>- 打开*nav*后关闭其他标签页，运行<b>「自动执行列表2」</b>，等待运行完毕
>- 关闭*epub*且不保存
><br/>
>
>### 自动化执行#3
>- 在`桌面`找到文件名含有`"epub2"`的*epub*
>- 规范化重命名*xhtml*，调整前后顺序并删除空白/多余的*xhtml*，删除*nav*
>- 打开`[封面页].xhtml`后关闭其他标签页，运行<b>「自动执行列表3」</b>，等待运行完毕
>- 按照需求进行繁简转换，检查无误后保存*epub*
><br/>
>
>### 后期加工
>- `[章节].xhtml`头部检查章节标题，若为标题图可与正文拆分或替换为文字
>- `[章节].xhtml`中部检查正文格式，若存在特殊格式进行手动处理
>- `[章节].xhtml`尾部检查残留脚注，若存在残留依据标准注释格式进行修复
>- 检查`[目录页].xhtml`与`toc.ncx`内链接是否完整正确，补正相关链接
>- 检查`content.opf`内元数据，按需求修改元数据信息并补全ISBN号
>- 制作`[标题页].xhtml`与`[目录页].xhtml`样式
>- 检查无误后保存*epub*
>- 运行`SigilFontSubset`插件，根据插件日志检查*xhtml*中特殊符号与字体缺字，修正格式并补全字体
>- 运行`SigilCompressImg`插件，将除`cover.jpg`外的图片压缩为<b>「webp格式，80%质量」</b>
>- 参考`EpubJSReader`插件、`ReadiumReader`插件与靶向适配阅读器表现效果调整样式
>- 运行`ePub3`插件，导出*epub*并命名为`[作者].标题.～副标题～.卷号.epub`
><br/>
>
>### 制作完成！

<br/>

<h2 id="tips">注意事项</h2>
1. 模板中需使用JavaScript元素，请确保Sigil对JavaScript的正常支持<br/>
2. 模板自动化会清理<code>&lt;img&gt;</code>元素行内的字符，请提前分离行内图片<br/>
3. 标题文本自动生成需依赖<code>[目录页].xhtml</code>与<code>[章节].xhtml</code>中id元素的正确链接<br/>
4. 文件规范化命名应遵循易读原则的层进方法，要求<b>封面页</b>文档命名为<code>cover.xhtml</code>，<b>简介页</b>文档命名为<code>summary.xhtml</code>，单图文档命名需包含<code>cover/illus/intro/start/author</code>其中字符串之一