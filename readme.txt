
Windows, Python 3.6

��Ŀ��Ϊ�����֣�
һ����ȡÿ��ͼƬ��Url���ص㣩
��������ͼƬ


һ����ȡÿ��ͼƬ��Url���ص㣩

    ####1���㷨
        1.1 ����˼·
            ��ȡһ��ͼƬ��Url��·��Ϊ������http://img.juemei.com/album/2016-09-16/57dc058315783.jpgΪ������
            ==> 1��http://www.juemei.com/mm/ 					(��·����
            ==> 2��http://www.juemei.com/mm/l.html				(SecondimgUrls/SecondimgUrls_First)
            ==> 3��http://www.juemei.com/mm/201609/5077.html			(ThirdImgUrls)
            ==> 4��http://img.juemei.com/album/2016-09-16/57dc058315783.jpg	(imgUrls)

            ��·���°������SecondimgUrls_First
            һ��SecondimgUrls_First ��Ӧ��Html�������SecondimgUrls
            һ��SecondimgUrls	    ��Ӧ��Html�������ThirdImgUrls
            һ��ThirdImgUrls	    ��Ӧ��Html�������imgUrls

            ��ˣ���ȡUrl�����ǣ�
            ==> ����SecondimgUrls_First
            ==> ����SecondimgUrls
            ==> ����ThirdImgUrls
            ==> ����imgUrls
    
        1.2 �Ż�        
            1.2.1 ��������
                ��Ϊ�п�����������ͼƬ������˲���Ҫ�����е�Url�������ꡣͨ���۲죬ƽ��һ��ThirdImgUrl��Ӧ
                ��Html������5��imgUrls�����ThirdImgUrl��������ThirdImgUrlNum = ImgNum//5(����)��֮����Ҫ��
                ���Ż�������ΪThirdImgUrl�ܶ࣬ÿ24��ThirdImgUrl�Ļ�ȡ����Ҫ���SeondImgUrl��http����Html
                ���ء�Url��ȡ�ȹ���������ThirdImgUrl����ȡ��ȽϺ�ʱ����ΪSecondImgUrl�Ǵ�SecondImgUrl_First
                �й�������ģ����������࣬����û��Ҫ����������
                ��ΪҪ�ϸ�����������еĳ�Ա������������Ҫ���������е�����в���������
            
            1.2.2 ���뾫��
                "����Html ==> ��ȡUrl" ��һ���Ǵ����ظ��������������ط���Ҫ�õ���Ϊ�˾�����룬��д��һ��
                ����:                     
                                    getUrl(url,tagName, Attrs, reg)
                                    
                    url: �����������ڵ���ַ
                tagName������������html�ı�ǩ��,����div,a,li
                  Attrs: tagName��ǩ�����ԣ�����{"class":"c1"}
                    reg���������ӵ�������ʽ������href="..."��Ӧ������ʽΪ:
                         r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
                         
                ������ͨ��url��ȡHtml�ı�������BeautifulSoup��Html���з������ڴ˻����ϣ��ҵ�����Attrs��tagName
                ��ǩ���ı����ڴ��ı���ͨ��reg�õ���Ӧ��Url
                
            1.2.3 ȥ��
                ����ThirdImgUrl�������ظ���url,�����ȥ��,�ᵼ������ͼƬ����������
                ���磬SeconImgdUrl�� http://www.juemei.com/mm/sfz/ �� http://www.juemei.com/mm/l_2.html
                ������ThirdImgUrl: http://www.juemei.com/mm/201709/12818.html,
                �����ThirdImgUrl��ȡ��imgUrls�����ظ��ġ�
                �����޷�ȥ�أ����Ե��߳����ü���ȥ�ء�
                ��ΪThirdImgUrl�����㹻�࣬ȥ���ظ��󲻱ػ�ȡ�µ���Ϊ���䡣
                �ڶ�ThirdImgUrlȥ�غ���imgUrls��������ظ�����˼���ȥ�ء���¼��ȥ�����ظ�imgUrl������
                ���»�ȡ(��Ϊ�����ǰ�濪ʼ����ͼƬ��Ϊ�˱����ظ������»�ȡ��ʱ��Ӻ����ͼƬ��ʼ)��
                ֱ��ȥ���ĸ���Ϊ0��
                
            1.2.4 ��������
                �����̴���������
    
    ####2�����ݽṹ
        ��Ϊ���̣߳�����Url���ö��д洢���ֱ��ǣ�
        imgUrls/SecondimgUrls_First/SecondimgUrls/ThirdImgUrls
        
        
��������ͼƬ
    
    �Ӷ���imgUrls��ȡ��url���أ����߳�

*�������ڸ���
	�����Ҫ��������վ��ͼƬ��ֻ��Դ�����������Ľ������к��Ĳ��֣�ͼƬ����getImg()��Tag��url��ȡgetUrl()����Ҫ�Ķ���
	ֻ��Ҫ������վ���ص㣬ȷ����ȡÿ��ͼƬurl��·�����Լ����url���ĸ�Tag���棬������Ӧ�ĸĶ����ɡ�
        
    
        
        
