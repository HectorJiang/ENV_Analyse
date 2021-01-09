启动uwsgi出现no internal routing support, rebuild with pcre support
使用如下命令，记录下，方便后人
需要注意的是pip install uwsgi 要加上–no-cache-dir，pip 可以强制下载重新编译安装的库，不然pip会直接从缓存中拿出了上次编译后的 uwsgi 文件，并没有重新编译一份。

ubuntu环境下
pip uninstall uwsgi

sudo apt-get install libpcre3 libpcre3-dev

pip install uwsgi --no-cache-dir

centos环境下
pip uninstall uwsgi
yum install -y pcre pcre-devel pcre-static
pip install uwsgi --no-cache-dir