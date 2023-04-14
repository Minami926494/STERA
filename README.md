# STERAePub++标准化模板<br/>
<b>～ePub自动化快速精排 for ver1.3.x～</b>
<br/><br/>

## 使用条件
- <b>适用工具：</b>Sigil 1.8.0+
- <b>适用对象：</b>以[《台灣 EPUB 3 製作指引》](https://github.com/dpublishing/epub3guide)为标准，轻小说为主的ePub电子书源
- <b>目标类型：</b>横排流式中文、日文（UTF-8）ePub电子书
- <b>靶向适配：</b>WebKit内核浏览器/Reasily/多看阅读/Starrea/iBooks/Kindle/掌阅iReader
- <b>执行标准：</b>EPUB 3.0.1/XHTML 1.1/CSS 3.0/ECMAScript 5/Python 3.6
<br/>

## 使用方法
>
>### 前期准备
>- 将`插件`内的*zip*在Sigil插件管理中直接安装，无需解压
>
>- 将`列表`内的*txt*复制至`C:\Users\用户名\AppData\Local\sigil-ebook\sigil\`
>- 在Sigil首选项中勾选<b>「EPUB可以使用JavaScript」</b>选项
><br/>
>
>### 预处理
>- 打开`[书源].epub`
>
>- 检查`[书源].epub`是否为<b>EPUB 3.0</b>文件，若不是则<b>「按Sigil格式重建EPUB」</b>后运行`ePub3-itizer`插件进行转换，打开输出文件
>- 检查`OEBPS/Images/`，寻找字符图、标题图等，多为*png*
>- 检查*xhtml*，用相应字符替换字符图，按需求拆分或删除标题图
>- 拆分包含多张图片的纯图片*xhtml*，确保纯图片*xhtml*中有且仅有一张图片
>- 检查封面图是否为`cover.jpg`，若不是请重命名
>- 检查*nav*是否包含所有文字章节，如有遗漏则<b>「编辑目录」</b>补充完整
>- 导入`素材`内的所有文件，填写`info.xhtml`
><br/>
>
>### 自动执行\#1
>- 运行<b>「自动执行列表1」</b>，等待运行
>
>- 按需求在`TraSimConvert`插件弹窗中进行繁简转换，若无需求请直接关闭该窗口，不要执行
>- `STERA-X`插件将对可能存在特殊样式的HTML标签添加属性`type="check"`便于检查
><br/>
>
>### 检查加工
>- 检查含属性`type="check"`的标签，全部处理完成后删除属性
>
>- 精排处理标题页、目录页等
>- 通过<b>「编辑目录」</b>按需调整*nav*条目
>- 参考`EpubJSReader`插件、`ReadiumReader`插件与靶向适配阅读器表现效果调整样式
><br/>
>
>### 自动执行\#2与收尾处理
>- 运行<b>「自动执行列表2」</b>，等待运行
>
>- `SigilCompressImg`插件运行时，将`cover.jpg`压缩为<b>「jpg格式，80%质量」</b>，此外的所有图片压缩为<b>「webp格式，80%质量」</b>
>- `SigilFontSubset`插件运行时，根据插件日志检查*xhtml*中特殊符号与字体缺字，修正格式并补全字体
>-  检查无误后保存*epub*并命名为`[作者].标题～副标题～.卷号.epub`
><br/>
>
>### 制作完成！

<br/>

## 功能简介
1. 模板生成*epub*完全符合相关标准并具有广泛的阅读器兼容<br/>
	- 模板使用文件采用模块化，`素材`中拓展样式表`style.css`及信息采集文档`info.xhtml`更改后可保存，配合预留直排英数字体`num.ttf`及字体空位`title.ttf`、`illus1.ttf`、`illus2.ttf`、`illus3.ttf`、`illus4.ttf`、`illus5.ttf`，按需扩展、修改模板后可实现系列书籍的快速制作<br/><br/>
	
	- 模板自带检查模块除自动化检查外还可手动对标签添加属性`type="check"`用于调试，可清晰展示该元素及所有后代元素的`border`边框位置便于复杂样式实现<br/><br/>


1. 模板引入Javascript在受支持的阅读器上实现互动式弹注、大图自动旋转、背景色冒泡，`素材`中的`script.js`是经压缩的文件，其源代码在`script-original.js`中<br/>
	- 弹注除Javascript的阅读器外还兼容多看、掌阅、iBooks、Kindle，其HTML代码格式如下：
	<pre><code> &lt;note&gt;
		&lt;p&gt;[正文文本]&lt;sup&gt;&lt;a class="duokan-footnote" epub:type="noteref" href="#note[编号]" id="note_ref[编号]"&gt;&lt;img alt="note" class="zhangyue-footnote" src="../Images/note.png" zy-footnote="[注释文本]"/&gt;&lt;/a&gt;&lt;/sup&gt;[正文文本]&lt;/p&gt;
		&lt;aside epub:type="footnote" id="note[编号]"&gt;
			&lt;a href="#note_ref[编号]"&gt; 
				&lt;ol class="duokan-footnote-content"&gt;
					&lt;li class="duokan-footnote-item" id="note[编号]" value="[编号]"&gt;&lt;p&gt;[注释文本]&lt;/p&gt;&lt;/li&gt;
				&lt;/ol&gt;
			&lt;/a&gt;
		&lt;/aside&gt;
	&lt;/note&gt;</code></pre><br/>
	- 大图自动旋转功能仅在移动设备生效，要求目标*xhtml*文档中有且仅有一个被含有属性`class="kuchie"`的`<div>`标签包裹的唯一`<img>`标签，形如：
	<pre><code> &lt;div class="kuchie duokan-image-single"&gt;
		&lt;img alt="eg" src="../Images/eg.jpg"/&gt;
	&lt;/div&gt;</code></pre><br/>
	- 背景色冒泡功能用于更广泛的阅读器兼容，将获取`<body>`标签的`bgcolor`属性值映射于其父元素`<html>`的背景色<br/><br/>


1. 自动化核心`STERA-X`插件安装后可在Sigil插件目录`C:\Users\用户名\AppData\Local\sigil-ebook\sigil\plugins\STERA-X\`下找到解压后的*py*文件并可进行自定义以适用于不同的书源情况，主要提供的功能接口为正则拓展和检索回复<br/>
	- 正则拓展功能需要修改`launch_groups.py`的查找替换执行组，每个执行组都是一个由命名字符串，一个预查找正则字符串及若干子元组组成的大元组，而子元组又由一个命名字符串和一个`{查找正则:替换正则}`形式的字典组成，其中的正则相关字符串应使用`r''`注释写法防止转义。对于每个大元组，执行查找替换时会先输出其命名，然后开始在预查找匹配范围内逐个执行子元组；对于每个子元组，被执行时会按照字典先后顺序执行正则查找替换，最后输出命名及替换字符串数量，其结构如下所示，示例执行组eg将在`(?s)<body>.*?</body>`匹配范围内依序执行四条正则查找替换：
	<pre><code> eg = ('示例执行组', r'(?s)&lt;body&gt;.*?&lt;/body&gt;',
			('执行组模块1', {
				r'查找1': r'替换1',
				r'查找2': r'替换2'}),
			('执行组模块2', {
				r'查找3': r'替换3',
				r'查找4': r'替换4'}))</code></pre><br/>
	- 正则拓展包含跨页二级正则和无穷计数正则两个主模块，其中跨页二级正则模块除上述的预查找正则外，还将在初始化文档时把每个文档包裹在`<page>`标签对中后按照*spine*或*manifest*顺序首尾相连为一个长文档，*xhtml*为*spine*而其他文档类型为*manifest*，这意味着用户可以通过执行组来跨页查找替换来自同种类型多个文档的内容。`<page>`标签具有`id`和`href`属性，其值分别为此文档的*manifest* id与文档文件名，如下是插件对一个含有`OEBPS/Text/123.xhtml`和`OEBPS/Text/abc.xhtml`两个*xhtml*的*epub*处理*xhtml*时产生的初始文档示例，若预查找字符串为空或`(?s)<page.*/page>`时匹配的也是它：
	<pre><code> &lt;page id="456" href="123.xhtml"&gt;
		[manifest id="456"的OEBPS/Text/123.xhtml文档内容]
	&lt;/page&gt;
	&lt;page id="def" href="abc.xhtml"&gt;
		[manifest id="def"的OEBPS/Text/abc.xhtml文档内容]
	&lt;/page&gt;</code></pre><br/>
	- 若在查找替换中自行插入额外的`<page>`标签对，插件将自动以标签对为界将原书页后半部拆分为新的一页，`<page>`标签对的写法同上例，其开始标签必须为如下格式，且注意将新旧文档的头尾部分补充完整，保证代码规范，另一方面也应注意在查找替换中不能删除或随意改动`<page>`标签对：
	<pre><code> &lt;page id="[新文件manifest id]" href="[新文件名]"&gt;</code></pre><br/>
	- 无穷计数正则定义一个新的正则标识符<b>「`(*)`」</b>或<b>「`(*[数字])`」</b>，当标识符出现在正则表达式开头时，若标识符含数字则数字代表此条目在标识符后的部分重复执行的次数，若不含数字则条目将重复执行至不再有匹配结果为止，故若启用无穷模式请注意循环逻辑防止出现死循环。插件为提升效率没有引入传统的`\0`拓展，但在查找条目含有上述标识符时，替换条目中若存在`*`将被替换为计数正则当前的重复次数，它是一个左补零的三位数字序号，如下例所示：
	<pre><code> 原字符串：&lt;p&gt;&lt;span&gt;&lt;span&gt;&lt;span&gt;&lt;span&gt;&lt;/span&gt;&lt;/span&gt;&lt;/span&gt;&lt;/span&gt;&lt;/p&gt;
	执行组条目：r'(*3)(&lt;p&gt;.*?)&lt;span&gt;': r'\1&lt;span id="*"&gt;*'
	结果字符串：&lt;p&gt;&lt;span id="001"&gt;001&lt;span id="002"&gt;002&lt;span id="003"&gt;003&lt;span&gt;&lt;/span&gt;&lt;/span&gt;&lt;/span&gt;&lt;/span&gt;&lt;/p&gt;</code></pre><br/>
	- 除两大主模块之外正则拓展部分还合并了单行与多行正则的首末检测，单个`^`或`$`对应整个字符串的最初和最末，而连续两个，即`^^`或`$$`对应一行的行首和行尾。正则拓展模块还解决了CRLF问题和制表符问题，从文档中获取的原字符串中`\r\n`、`\r`和`\n`被统一为`\n`，而`\t`将被替换为一个空格<br/><br/>
	
	- 正则拓展功能在`launch_groups.py`的修改完成后，还需要对`plugin.py`进行修改，这部分修改包括检索回复功能的使用，都涉及`file`类型。`file`类的其他定义及传参等工作插件中已经完成，用户使用中仅需修改<b>「文件编辑」</b>部分，`file`类的书写格式如下：
	<pre><code> file([manifest id构成的元组], [右侧任务完成后输出的字符串，留空则不输出])([检索回复正则字符串或查找替换执行组]*n)</code></pre><br/>
	- 如上例，`file`后的第二个括号为任务队列，其可用逗号分隔输入多个值，并将从左到右依次执行。当队列进行至查找替换执行组时，该组执行；而当队列进行至检索回复正则字符串时，将在内存中生成一个包含所有该正则对应字符串出现位置之所属文件的*manifest* id的元组，当如下例遍历`file`对象时会依序逐个返回元组，可用于实现更高级的功能：
	<pre><code> for i in file(x)('1', a, '2', b, '3'):
	&gt;&gt; i = tuple([元组x中有'1'出现的所有文件之manifest id])
	&gt;&gt; i = tuple([元组x中有'2'出现的所有文件之manifest id])
	&gt;&gt; i = tuple([元组x中有'3'出现的所有文件之manifest id])</code></pre><br/>
	- 更多功能的拓展与修改可以参照[Sigil官方文档](https://github.com/Sigil-Ebook/Sigil/tree/master/docs)中的插件开发文档