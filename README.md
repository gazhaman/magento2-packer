Amazon Linux 2 AMI
=====================
# Install Epel
amazon-linux-extras install epel

# Install Nginx
rpm -ivh http://nginx.org/packages/rhel/7/noarch/RPMS/nginx-release-rhel-7-0.el7.ngx.noarch.rpm
yum install nginx

# Install PHP
yum install https://rpms.remirepo.net/enterprise/remi-release-7.rpm
yum-config-manager --setopt="remi-php72.priority=5" --enable remi-php72
yum-config-manager --setopt="remi.priority=5" --enable remi
yum  install php php-common php-mcrypt php-gd php-pear php-intl php-soap php-mbstring php-xml php-pdo php-mysqlnd php-pecl-zip php-fpm php-pecl-redis php-opcache php-pecl-lzf php-bcmath php-pecl-imagick


# Enable Nginx, PHP-FPM
systemctl enable nginx php-fpm

# Install additional packages
yum install git ansible rsync amazon-efs-utils

# Install composer
wget https://getcomposer.org/composer-stable.phar && chmod +x composer-stable.phar && mv composer-stable.phar /usr/local/bin/composer

# Create folders
mkdir -p /var/www/html/current
mkdir /var/www/html/tmp /var/www/html/key
mkdir -p /var/www/html/share


# Add ssh-key1 for Git 
/var/www/html/key/ssh-key1


#EFS
Mount EFS (/var/www/html/share)
Edit fstab (https://docs.aws.amazon.com/efs/latest/ug/mount-fs-auto-mount-onreboot.html)

mkdir /var/www/html/share/media /var/www/html/share/var /var/www/html/share/etc
ln -s /var/www/html/share/var /var/www/html/current/var
ln -s /var/www/html/share/media /var/www/html/current/pub/media
ln -s /var/www/html/share/etc /var/www/html/current/app/etc
ln -s /var/www/html/view_preprocessed /var/www/html/current/var/view_preprocessed


#Install Magento2
