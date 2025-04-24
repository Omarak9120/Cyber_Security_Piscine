FROM ubuntu:20.04

RUN apt update && apt install -y vsftpd ftp

COPY vsftpd/vsftpd.conf /etc/vsftpd.conf
COPY ftp-data/ /home/ftpuser/

RUN useradd -m ftpuser && \
    echo "ftpuser:password" | chpasswd && \
    chown -R ftpuser:ftpuser /home/ftpuser/

EXPOSE 21

CMD ["/usr/sbin/vsftpd", "/etc/vsftpd.conf"]