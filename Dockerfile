FROM centos:7
RUN yum -y install python3-pip python36 curl unzip && \
    curl -o saclient.zip -sL "https://cloud.appscan.com/api/SCX/StaticAnalyzer/SAClientUtil?os=linux" && \
    unzip saclient.zip && rm -rf saclient.zip && mv SAClientUtil* /usr/local/saclient && \
    yum -y clean all && \
    rm -Rf /var/cache/yum && \
    pip3 install --no-cache-dir bottle cryptography PyJWT requests 

COPY app.py asoc_scan.py  download.py  /usr/bin/

ENV PATH="/usr/local/saclient/bin:${PATH}"

# tell the port number the container should expose
EXPOSE 5000

# run the application
ENTRYPOINT ["/usr/bin/app.py"]
