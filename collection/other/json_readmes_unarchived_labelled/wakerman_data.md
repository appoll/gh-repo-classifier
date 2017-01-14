##本项目意在收集网上前人已经做好的各种例子或者是学习方法的归纳，我们要站在巨人们的肩膀上，我们不提倡重新造轮子，但是我们希望能优化轮子，使她使用起来更加方便。

	生命如此短暂，为什么总要将青春浪费在不断的选择之中呢？罚你，回头阅读心理学家施瓦茨（BarrySchwartz）的TED演讲：
	选择之困惑——为何多即是少，1百遍啊1百遍。请记住施瓦茨的演讲要点：

	更多的选择不代表更多的自由；
	更多的选择导致决策的延迟和降低的满意感；
	快乐之秘诀，在于降低自己的期望值。

##JS/插件库（史上最全了）

[js/插件库](http://www.jsdb.io/animation/?sort=rating)
有了他就不用天天百度谷歌求他人了。


#学习方法篇
	工具
	  收集各种开发工具的使用方法和心得	
		
		
1. [如何高效利用GitHub](http://www.yangzhiping.com/tech/github.html "Title") 该文尝试谈谈GitHub的文化、技巧与影响。.
2. [git - 简易指南](http://rogerdudler.github.io/git-guide/index.zh.html/)
3. [markdown语法格式简要说明](http://blog.830725.com/post/markdown-syntax.html/)
4. [Markdown 语法说明 简体中文版](http://wowubuntu.com/markdown/)
		
##语言学习篇
	#jQuery/JavaScript
	各种案例，各种效果，当然使用最重要:)
	
1. [Node.js初学者教材](https://github.com/ManuelKiessling/NodeBeginnerBook)
2. [Node.js中文版](http://www.nodebeginner.org/index-zh-cn.html)
3. [jQuery 简易教程](https://github.com/bastengao/jquery-tutorial)
4. [阅读JQuery v1.8.1源码-好久没更新了](https://github.com/codepiano/JQuerySrcComment)
5. [impress.js的中文教程](https://github.com/kokdemo/impress.js-tutorial-in-Chinese)

## PHP篇
	这些轮子开源、许可证宽松、容易集成的PHP项目
	日志还会陆续补充更新，同时欢迎推荐补充。

##Databse 数据库ORM
#Doctrine 2
[Doctrine 2](http://www.doctrine-project.org/)
License : MIT
[Source Code](https://github.com/doctrine/doctrine2)
Allo点评：Doctrine是功能最全最完善的PHP ORM，社区一直很活跃，对NoSQL也非常迅速的作出了跟进与支持。但之所以没有说Doctrine是最好的，
是因为我对PHP究竟有没有必要使用如此庞大的ORM还心存疑虑，平心而论Doctrine的入门门槛实在有些高，尤其是DBAL的提出，更是要把开发者牢牢
绑定在Doctrine这艘大船上，用与不用，还是要仔细权衡。

#RedBeanPHP
[RedBeanPHP](http://www.redbeanphp.com/)
License : New BSD
[Source Code](https://github.com/gabordemooij/redbean)
Allo点评：相比起Doctrine，RedBean轻巧的简直要飞起来，这两个轮子就是一组最好的比照，是大而全，还是小而精，根据项目选择吧。
Documents & Testing 文档与测试

#phpDocumentor 2
[phpDocumentor 2](http://www.phpdoc.org/)
License : MIT
[Source Code](https://github.com/phpDocumentor/phpDocumentor2)
Allo点评：老牌php文档生成工具。

#Faker
[Faker](https://github.com/fzaninotto/Faker)
License : MIT
[Source Code](https://github.com/fzaninotto/Faker)
Allo点评：Faker是一个很神奇的项目，会自动生成拟真的数据，包括用户资料、长文本、IP、日期等等，在网站上线前测试时非常好用。

## Datetime 时间处理

#Carbon
[Carbon](https://github.com/briannesbitt/Carbon)
License : MIT
[Source Code](https://github.com/briannesbitt/Carbon)
Allo点评：虽然PHP5内置的Datetime类已经足够应付一般需求，不过Carbon所提供的一些更人性化的处理则更符合实际需求，
如果是时间相关的项目应该考虑使用。

##File System 文件系统
#Gaufrette
License : MIT
Source Code
Allo点评：文件系统几乎是所有项目都会遇到的问题，Gaufrette为常见的文件系统提供了一套统一接口，
包括本地文件/FTP/Dropbox/GridFS/Zip/AmazonS3等等，是大型系统必备的组件。

##Front-end 前端性能
#Assetic
License : MIT
Source Code
Allo点评：Assetic可以说生来就是为了多模块的项目而存在的，有了Assetic，可以将分散在各模块中的前端文件编译、合并、压缩。
可以让开发人员专注于代码的编写而不是前端文件的生成。

#lessphp
License : MIT
Source Code
Allo点评：LESS编译器的php版本。不过对于复杂的LESS项目，比如bootstrap，编译的结果与NodeJS原版还是有差异，只能做为Assetic的一个补充。

#minify
License : MIT
Source Code
Allo点评：PHP版本的CSS/JS压缩器。
HTTP Client HTTP客户端

#Requests
License : MIT
Source Code
Allo点评：Requests实现的非常灵巧，底层默认没有使用cURL而是采用fsockopen作为通信手段，非常适合集成在一些小型项目中。

#Buzz
License : MIT
Source Code
Allo点评：另一个轻量级的HTTP客户端实现，文档上不够丰富。独到之处在于内置了事件机制，可以更灵活的集成。

##HTML & Dom

#HTMLPurifier
License : LGPL v2.1+
Source Code
Allo点评：凡是有WYSIWYG功能的项目，XSS以及恶意的提交都会成为一个头痛的问题。HTMLPurifier提供了完整的HTML校验与纠错，又无需安装tidy扩展。

#PHP Simple HTML DOM Parser
License : MIT
Source Code
Allo点评：解析HTML为DOM并且可以使用jQuery选择器操作DOM，如果需要提取HTML页面内容而不考虑高性能，那么用PHP Simple HTML DOM可以很惬意。
Image 图形处理
Imagine
License : MIT
Source Code
Allo点评：Imagine为几大图形处理库提供了一个统一接口，即后台可以为Gd、Imagick、Gmagick的任意一种，而代码保持不变。
其实Pear也提供过类似的库Image_Transform，但是Imagine明显更胜一筹。
应用范围：缩略图生成等任何图形相关的功能。
Log处理
Monolog
License : MIT

#Source Code
Allo点评：可以非常简单的规定Log格式，并有众多的后端支持。虽然像Zend Framework也内置了Zend\Log这样的组件，
但是Monolog仍然是最全面专业的Log处理首选方案
应用范围：几乎所有需要线上调试或者收集用户信息的系统

##Markups 标记语言

#PHP Markdown
License : New BSD License
Source Code
Allo点评：Markdown在轻量级标记语言中已经俨然有一统天下的趋势，PHP Markdown应该是目前以PHP编写的最好的Markdown解析器。
当然一般来说使用Markdown作为标记语言需要搭配一个JS编辑器，比如PageDown-Bootstrap
应用范围：任何中长篇的用户数据录入，比如用户评论、Blog等场景。可以减轻用户录入负担，并且有效的防止XSS

##Payment Gateways 支付网关

#Aktive Merchant for PHP
License : MIT
Source Code
Allo点评：Ruby项目Active Merchant的php版本。对PayPal、Authorize.net等多家支付网关提供了统一的接口。
应用范围：需要支付网关的项目，有国内支付宝等网关支付需求的完全可以贡献代码

#Omnipay
License : MIT
Source Code
Allo点评：统一接口的支付网关，支持的支付接口更丰富一些。


##Queue 任务队列

#php-resque
License : MIT
Source Code
Allo点评：php-resque是Ruby项目resque在php下的实现。虽然Gearman也是一个不错的选择，但是resque的构架设计更加简洁清晰，
更加符合KISS原则。简单用法可以参看用PHP实现守护进程任务后台运行与多线程一文
应用范围：需要后台任务的系统，比如邮件发送、同步信息等需求。


##Templating 模板引擎

#Twig
License : New BSD License
Source Code
Allo点评：如果说对模板引擎的印象还停留在Smarty的阶段，那么你真的已经落后于时代了。Twig是目前关注度最高的PHP模板引擎，
比Smarty提供了更简约和易懂的语法。当然如果项目没有主题切换这样的需求，php本身就是最好的模板引擎。
应用范围：有皮肤、主题切换需求的项目，可以避免php模板带来的安全问题




[那些最好的轮子 - PHP篇](http://avnpc.com/pages/best-wheels-for-php)
以上[PHP篇]均来自 [AlloVince](http://avnpc.com/) 原创。版权采用『 知识共享署名-非商业性使用 2.5 许可协议』进行许可



#Google Maps API 2 文档
[Google Maps API 2 文档](http://www.codechina.org/doc/google/gmapapi/)




#Blog-论坛
[代码中国](http://www.codechina.org/)

#Google混搭编辑器(Google Mashup Editor) - 混搭编程框架和开发工具
[Google混搭编辑器(Google Mashup Editor) - 混搭编程框架和开发工具](http://www.codechina.org/doc/google/gme/)

# [Google文件系统论文](http://www.codechina.org/doc/google/gfs-paper/)

#修改Nginx配置，让网页变灰
让网页变灰，为雅安哀悼。程序员们可以修改Nginx的nginx.conf文件，用sub_filter指令使得每个页面都自动变灰，
不用一页一页手工修改，如www.ucloud.cn。详细配置可参考@hydra35 写的 http://t.cn/zTiZkGw
下面是具体配置：
#nginx.conf
 Nginx
   1. Make sure you have nginx sub module compiled in
   nginx -V  2>&1 | grep --color=always '\-\-with\-http_sub_module'
 
  2. add two directives below at HTTP level
 
nginx.conf

     http {
        # ......

        sub_filter  '</head>' '<style type="text/css">html{ filter:progid:DXImageTransform.Microsoft.BasicImage(grayscale=1); -webkit-filter: grayscale(100%); } img { _filter:progid:DXImageTransform.Microsoft.BasicImage(grayscale=0); -webkit-filter: grayscale(100%); } </style>';
        sub_filter_once on;
        
        # ......
       }
       
 
  3. nginx -t && /etc/init.d/nginx reload
 
  Notes:
 
1. Does not work on Firefox [filter: url("data:image/svg+xml;utf8,#grayscale"); /*Firefox*/]
2.  [解决Firefox的方法](http://www.karlhorky.com/2012/06/cross-browser-image-grayscale-with-css.html)


#Packery: 用算法将页面的元素排列，达到占满空间的效果
[Packery: 用算法将页面的元素排列，达到占满空间的效果](http://packery.metafizzy.co/)
[github](https://github.com/metafizzy/packery)

[JavaScript 原理](http://typeof.net/s/jsmech/)

这本书面向的读者
ANSI Common Lisp 这本书适合学生或者是专业的程序员去读。本书假设读者阅读前没有 Lisp 的相关知识。有别的程序语言的编程经验也许对读本书有帮助，但也不是必须的。本书从解释 Lisp 中最基本的概念开始，并对于 Lisp 最容易迷惑初学者的地方进行特别的强调。

本书也可以作为教授 Lisp 编程的课本，也可以作为人工智能课程和其他编程语言课程中，有关 Lisp 部分的参考书。想要学习 Lisp 的专业程序员肯定会很喜欢本书所采用的直截了当、注重实践的方法。那些已经在使用 Lisp 编程的人士将会在本书中发现许多有用的实例，此外，本书也是一本方便的 ANSI Common Lisp 参考书。
[ANSI Common Lisp ](http://acl.readthedocs.org/en/latest/zhCN/preface-cn.html#id2)
