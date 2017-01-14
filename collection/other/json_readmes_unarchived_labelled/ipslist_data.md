

http://protectprivate.googlecode.com/svn/trunk/cloudconfig/proxys5.xml

http://protectprivate.googlecode.com/svn/trunk/ipserver/ipubuntu.sh

http://protectprivate.googlecode.com/svn/trunk/ipserver/hideipserver

 yum install php-mcrypt*

svn checkout https://protectprivate.googlecode.com/svn/trunk/ipserver2




ubuntu 32bits:
apt-get update
apt-get install vim
apt-get install subversion
apt-get install curl
apt-get install screen
; to install killall command
sudo apt-get install psmisc


svn checkout https://protectprivate.googlecode.com/svn/trunk/ipserver2
sudo vi /etc/rc.local
add:
su root -c 'chmod a+x /root/ipserver2/start.sh'
su root -c '/root/ipserver2/start.sh'


reboot

  
2. 如果是64位系统，还需要安装32位支持库:
64位ubuntu如何运行32位程序：
解决办法很简单，只需要安装32位程序的支持库就可以了。
sudo apt-get install ia32-libs

centos上  32位需要运行在64位系统上：
yum install glibc.i686
yum whatprovides libstdc++.so.6
yum install libstdc++-4.4.7-3.el6.i686

 yum -y install vim*

4. 添加到开机启动

向此文件中加，一定要指明哪个用户运行：
sudo vi /etc/rc.local


su root -c '/root/ipserver2/start.sh'

centos:
yum -y install vim*

vim  /etc/rc.d/rc.local
chmod a+x /root/ipserver2/start.sh
/root/ipserver2/start.sh



4.关闭防火墙服务：
#/etc/init.d/iptables stop
chkconfig --level 35 iptables off


#/sbin/iptables -I INPUT -p tcp -dport 8115 -j ACCEPT
#/sbin/iptables -I INPUT -p tcp -dport 8115 -j ACCEPT
#/etc/rc.d/init.d/iptables save


