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
*（部分条目相关说明请参[注意事项](#注意事项)）*

>### 前期准备
>- 将`插件`内的*zip*在Sigil插件管理中直接安装，无需解压
>- 将`自动化`内的*ini*导入Sigil搜索模板，将<b>「`书源处理`」</b>组剪切至搜索模板根目录
>- 将`自动化`内的*txt*复制至`C:\Users\用户名\AppData\Local\sigil-ebook\sigil\`
>- 在Sigil首选项中勾选<b>「EPUB可以使用JavaScript」</b>选项
><br/>
>
>### 预处理
>- 打开`[书源].epub`
>- 检查`OEBPS/Images/`，寻找可能是行内图的字符图、标题图等，多为*png*
>- 检查*xhtml*，用相应字符替换字符图，统一标题图格式以便后续替换
>- 拆分包含多张图片的纯图片*xhtml*，确保纯图片*xhtml*中有且仅有一张图片
>- 检查`[目录页].xhtml`与`[章节页].xhtml`，确保目录链接至每个章节的第一个主文本*xhtml*中相应的id元素，且章节标题与副标题文本使用全角空格`"　"`正确分割
><br/>
>
>### 自动化执行\#1
>- 删除`OEBPS/Styles/`中的所有文件
>- 规范化重命名`OEBPS/Images/`内的图片文件并删除多余图片
>- 选中`OEBPS/Text/`的最后一个文件，通过<b>「添加现有文件」</b>将`素材`内的文件导入
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
>- 选中`OEBPS/Text/`中除*nav*外的所有文件，合并文件
>- 打开*nav*后关闭其他标签页，运行<b>「自动执行列表2」</b>，等待运行完毕
>- 关闭*epub*且不保存
><br/>
>
>### 自动化执行#3
>- 在`桌面`找到文件名含有`"epub2"`的*epub*
>- 规范化重命名*xhtml*，调整前后排列顺序并删除空白/多余的*xhtml*，删除*nav*
>- 打开`[封面页].xhtml`后关闭其他标签页，运行<b>「自动执行列表3」</b>，等待运行完毕
>- 按照需求进行繁简转换，检查无误后保存*epub*
><br/>
>
>### 后期加工
>- `[章节页].xhtml`头部检查章节标题，若为标题图可与正文拆分或替换为文字
>- `[章节页].xhtml`中部检查正文格式，若存在特殊格式进行手动处理
>- `[章节页].xhtml`尾部检查残留脚注，若残留依据标准注释格式进行修复
>- 检查`[目录页].xhtml`与`toc.ncx`内链接是否完整正确，补正相关链接
>- 检查`content.opf`内元数据，按需求修改元数据信息并补全ISBN号
>- 制作`[标题页].xhtml`与`[目录页].xhtml`样式
>- 依照书源信息与书源侧信息补全`[制作信息页].xhtml`
>- 检查无误后保存*epub*
>- 运行`SigilFontSubset`插件，根据插件日志检查*xhtml*中特殊符号与字体缺字，修正格式并补全字体
>- 运行`SigilCompressImg`插件，将除`cover.jpg`外的图片压缩为<b>「webp格式，80%质量」</b>
>- 参考`EpubJSReader`插件、`ReadiumReader`插件与靶向适配阅读器表现效果调整样式
>- 运行`ePub3`插件，导出*epub*并命名为`[作者].标题～副标题～.卷号.epub`
><br/>
>
>### 制作完成！

<br/>

## 注意事项
1. 模板中需使用JavaScript元素，请确保Sigil对JavaScript的正常支持

2. 模板自动化会清理`<img>`元素行内的字符，请提前分离行内图片
3. 基于js支持的大图自动旋转功能要求该*xhtml*内有且仅有一张图片
4. 标题文本自动生成需依赖`[目录页].xhtml`与`[章节页].xhtml`中id元素的正确链接，全角空格分割位置将影响最终生成结果
5. 文件规范化命名应遵循易读原则的层进方法，要求<b>封面页文档</b>命名为`cover.xhtml`，<b>简介页文档</b>命名为`summary.xhtml`，<b>纯图片文档</b>命名需包含`cover/illus/intro/start/author`其中一者，反之则不可使用涉及上列字符串的命名，此举将影响`ePub3`插件的运行
6. 应确保*nav*为`OEBPS/Text/`的首个文件，而`insert.xhtml`的插入位置位于最后
7. 运行<b>「自动执行列表」</b>时关闭尽可能多的标签页并减少刷新频次可长足提升运行速度
8. <b>「自动执行列表」</b>的运行过程中遇到弹窗时，<b>「警告框」</b>与<b>「确认框」</b>一律选择<b>「确认」</b>，两者分别可用<b>「Esc」</b>和<b>「Enter」</b>键代替鼠标点击
9. 若自动拆分过程中出错切勿使用自动修复，请手动修复后按如下方式继续：运行Sigil搜索模板的<b>「`书源处理/拆分后处理`」组</b>→<b>执行「按Sigil格式重建Epub」</b>→运行`ePub2`插件
10. `ePub2`插件仅支持输出半角英数字符命名文件，若`桌面`存在重名文件则会覆盖，请勿在同一设备上同时开展多个自动化任务，并在每册书籍制作完成后及时删除工程文件
11. 如需保留繁体中文版书籍，在`TraSimConvert`插件运行时直接关闭即可，无需进行转换
12. 标题图如要保留请至于章节正文之前并与正文拆分，拆分后按照<b>纯图片文档</b>标准处理
13. 检查特殊符号和特殊样式是正文检查的重要手段，请尤其注意带有方向性的特殊符号及带有类名的正文段落 
14. 标准注释格式与阅读器兼容和内置js弹注相关联，请参照如下书写，将`"X"`替换为相应序号，并保证单*xhtml*内序号不重复
<pre><code>  &lt;div&gt;
    &lt;p&gt;[正文文本]&lt;sup&gt;&lt;a class="duokan-footnote" epub:type="noteref" href="#noteX" id="note_refX"&gt;&lt;img alt="note" class="zhangyue-footnote" src="../Images/note.png" zy-footnote="[注释文本]"/&gt;&lt;/a&gt;&lt;/sup&gt;[正文文本]&lt;/p&gt;

    &lt;aside epub:type="footnote" id="noteX"&gt;
      &lt;a href="#note_refX"&gt; 
        &lt;ol class="duokan-footnote-content" style="list-style:none"&gt;
          &lt;li class="duokan-footnote-item" id="noteX" value="X"&gt;&lt;p&gt;[注释文本]&lt;/p&gt;&lt;/li&gt;
        &lt;/ol&gt;
      &lt;/a&gt;
    &lt;/aside&gt;
  &lt;/div&gt;</code></pre>
15. *ncx*和*opf*的修改可以通过Sigil内置编辑器完成，但由于EPUB 3中*nav*的存在会导致目录编辑器无法修改*ncx*，故请于EPUB 2转换后，EPUB 3导出前完成相关更改
16. 部分阅读器不支持webp格式作为封面，故`cover.jpg`不进行转码压缩
17. 阅读器预览插件表现效果与靶向适配阅读器存在出入，仅供参考且以后者为准