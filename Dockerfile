FROM centos:7
RUN yum -y install python3-pip python36 curl unzip && \
    curl -o saclient.zip -sL "https://cloud.appscan.com/api/SCX/StaticAnalyzer/SAClientUtil?os=linux" && \
    unzip saclient.zip && rm -rf saclient.zip && mv SAClientUtil* /usr/local/saclient && \
    yum -y clean all && \
    rm -Rf /var/cache/yum && \
    pip3 install --no-cache-dir bottle cryptography PyJWT requests gunicorn 

CMD python3 app.py

ENV PATH="/usr/local/saclient/bin:${PATH}"
