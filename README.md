# STERAePub++标准化模板<br/>
<b>～ePub自动化快速精排 ver 1.3.1+～</b>
<br/><br/>

>## 使用条件
>- <b>适用工具：</b>Sigil 1.9.0+
>- <b>适用对象：</b>以[《台灣 EPUB 3 製作指引》](https://github.com/dpublishing/epub3guide)和[《電書協 EPUB 3 制作ガイド》](http://ebpaj.jp/counsel/guide)为标准，轻小说为主的ePub电子书源
>- <b>目标类型：</b>横排流式中文、日文（UTF-8）ePub电子书
>- <b>靶向适配：</b>WebKit内核浏览器/Reasily/多看阅读/Starrea/iBooks/Kindle/掌阅iReader
>- <b>执行标准：</b>EPUB 3.0.1/XHTML 1.1/CSS 3.0/ECMAScript 5/Python 3.6/Qt 5

<br/>

>## 安装方式
>-  <b>Windows：</b>运行*setup.exe*自动覆盖安装
>-  <b>MacOS/Linux及其他：</b>将*STERA-X*文件夹与*STERA-Std*文件夹分别放入<b>同名父文件夹</b>内后压缩为*zip*，通过`Sigil插件→插件管理→添加插件`安装压缩包，无需解压

<br/>

>## 功能简介
>-  <b>STERA-X：</b>集成自动化书源处理插件，包含*自动化处理*、*繁简转换*、*字体子集化*、*图片压缩*四大功能模块，其中*自动化处理*包含7个主流程与3个附加功能，皆可分离单独运行
>-  <b>STERA-Std：</b>书源规范化插件，可快速执行*EPUB规范化*与*EPUB 2转EPUB 3*操作
>-  <b>STERAePub++：</b>虚空文学旅团EPUB组标准化模板，具有广泛阅读器适配和优秀视觉效果，依赖JS可实现*互动式弹注*、*图片方向自适应*、*背景色渗透`body[bgcolor]`*，配合*STERA-X*自动化还可实现*自动样式检查与调试`[type="check"]`*