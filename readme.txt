
Windows, Python 3.6

项目分为两部分：
一、获取每张图片的Url（重点）
二、下载图片


一、获取每张图片的Url（重点）

    ####1、算法
        1.1 基本思路
            获取一张图片的Url的路径为：（以http://img.juemei.com/album/2016-09-16/57dc058315783.jpg为例）：
            ==> 1、http://www.juemei.com/mm/ 					(主路径）
            ==> 2、http://www.juemei.com/mm/l.html				(SecondimgUrls/SecondimgUrls_First)
            ==> 3、http://www.juemei.com/mm/201609/5077.html			(ThirdImgUrls)
            ==> 4、http://img.juemei.com/album/2016-09-16/57dc058315783.jpg	(imgUrls)

            主路径下包含多个SecondimgUrls_First
            一个SecondimgUrls_First 对应的Html包含多个SecondimgUrls
            一个SecondimgUrls	    对应的Html包含多个ThirdImgUrls
            一个ThirdImgUrls	    对应的Html包含多个imgUrls

            因此，获取Url步骤是：
            ==> 所有SecondimgUrls_First
            ==> 所有SecondimgUrls
            ==> 所有ThirdImgUrls
            ==> 所有imgUrls
    
        1.2 优化        
            1.2.1 控制数量
                因为有可以设置下载图片数，因此不需要把所有的Url都下载完。通过观察，平均一个ThirdImgUrl对应
                的Html含至少5个imgUrls。因此ThirdImgUrl的数量：ThirdImgUrlNum = ImgNum//5(整除)。之所以要这
                样优化，是因为ThirdImgUrl很多，每24个ThirdImgUrl的获取都需要完成SeondImgUrl的http请求、Html
                下载、Url抽取等工作，所有ThirdImgUrl都获取完比较耗时。因为SecondImgUrl是从SecondImgUrl_First
                中构造出来的，且数量不多，所以没必要控制数量。
                因为要严格控制两个队列的成员数量，所以需要对两个队列的入队列操作加锁。
            
            1.2.2 代码精简
                "下载Html ==> 获取Url" 这一步是大量重复工作，程序许多地方需要用到。为了精简代码，我写成一个
                函数:                     
                                    getUrl(url,tagName, Attrs, reg)
                                    
                    url: 所需链接所在的网址
                tagName：所需链接在html的标签名,比如div,a,li
                  Attrs: tagName标签的属性，比如{"class":"c1"}
                    reg：所需链接的正则表达式，比如href="..."对应正则表达式为:
                         r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
                         
                函数先通过url获取Html文本，再用BeautifulSoup对Html进行分析。在此基础上，找到满足Attrs的tagName
                标签的文本，在此文本中通过reg得到对应的Url
                
            1.2.3 去重
                队列ThirdImgUrl可能有重复的url,如果不去重,会导致下载图片数量不够。
                比如，SeconImgdUrl： http://www.juemei.com/mm/sfz/ 和 http://www.juemei.com/mm/l_2.html
                都包含ThirdImgUrl: http://www.juemei.com/mm/201709/12818.html,
                从这个ThirdImgUrl获取的imgUrls就是重复的。
                队列无法去重，可以单线程下用集合去重。
                因为ThirdImgUrl数量足够多，去掉重复后不必获取新的作为补充。
                在对ThirdImgUrl去重后发现imgUrls还会出现重复，因此继续去重。记录下去掉的重复imgUrl个数，
                重新获取(因为程序从前面开始下载图片，为了避免重复，重新获取的时候从后面的图片开始)，
                直到去掉的个数为0。
                
            1.2.4 防反爬虫
                从西刺代理爬代理。
    
    ####2、数据结构
        因为多线程，所有Url均用队列存储，分别是：
        imgUrls/SecondimgUrls_First/SecondimgUrls/ThirdImgUrls
        
        
二、下载图片
    
    从队列imgUrls中取出url下载，多线程

*三、关于复用
	如果需要爬其它网站的图片，只需对代码进行少量改进。其中核心部分：图片下载getImg()、Tag内url提取getUrl()不需要改动。
	只需要根据网站的特点，确定获取每张图片url的路径，以及这个url在哪个Tag里面，再做相应的改动即可。
        
    
        
        
