ARG JAVA_VERSION=11.0.13_8
ARG ALPINE_TAG=3.9
FROM eclipse-temurin:"${JAVA_VERSION}"-jdk-alpine AS jre-build

RUN if [ "$TARGETPLATFORM" != 'linux/arm/v7' ]; then \
    case "$(jlink --version 2>&1)" in \
      # jlink version 11 has less features than JDK17+
      "11."*) strip_java_debug_flags="--strip-debug" ;; \
      *) strip_java_debug_flags="--strip-java-debug-attributes" ;; \
    esac; \
    jlink \
      --add-modules ALL-MODULE-PATH \
      "$strip_java_debug_flags" \
      --no-man-pages \
      --no-header-files \
      --compress=2 \
      --output /javaruntime; \
  else \
    cp -r /opt/java/openjdk /javaruntime; \
  fi

FROM alpine:"${ALPINE_TAG}" AS build

ARG user=jenkins
ARG group=jenkins
ARG uid=1000
ARG gid=1000
ARG JENKINS_AGENT_HOME=/home/${user}

ENV JENKINS_AGENT_HOME=${JENKINS_AGENT_HOME}

ARG AGENT_WORKDIR="${JENKINS_AGENT_HOME}"/agent
# Persist agent workdir path through an environment variable for people extending the image
ENV AGENT_WORKDIR=${AGENT_WORKDIR}

RUN addgroup -g "${gid}" "${group}" \
    # Set the home directory (h), set user and group id (u, G), set the shell, don't ask for password (D)
    && adduser -h "${JENKINS_AGENT_HOME}" -u "${uid}" -G "${group}" -s /bin/bash -D "${user}" \
    # Unblock user
    && passwd -u "${user}" \
    # Prepare subdirectories
    && mkdir -p "${JENKINS_AGENT_HOME}/.ssh/" "${JENKINS_AGENT_HOME}/.jenkins/" "${AGENT_WORKDIR}" \
    && chown -R "${uid}":"${gid}" "${JENKINS_AGENT_HOME}" "${AGENT_WORKDIR}"


RUN apk add --no-cache \
    bash \
    git-lfs \
    less \
    netcat-openbsd \
    openssh \
    patch \
    python3-dev \
    gcc \
    musl-dev \
    p7zip


# setup SSH server
RUN sed -i /etc/ssh/sshd_config \
        -e 's/#PermitRootLogin.*/PermitRootLogin no/' \
        -e 's/#PasswordAuthentication.*/PasswordAuthentication no/' \
        -e 's/#SyslogFacility.*/SyslogFacility AUTH/' \
        -e 's/#LogLevel.*/LogLevel INFO/' \
        -e 's/#PermitUserEnvironment.*/PermitUserEnvironment yes/' \
    && mkdir /var/run/sshd

# Install JDK

ENV JAVA_HOME=/opt/java/openjdk
COPY --from=jre-build /javaruntime "$JAVA_HOME"
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# VOLUME directive must happen after setting up permissions and content
VOLUME "${AGENT_WORKDIR}" "${JENKINS_AGENT_HOME}"/.jenkins "/tmp" "/run" "/var/run"
WORKDIR "${JENKINS_AGENT_HOME}"

RUN apk --no-cache add libaio libnsl libc6-compat curl && \
    cd /tmp && \
    curl -o instantclient-basiclite.zip https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip -SL && \
    unzip instantclient-basiclite.zip && \
    mv instantclient*/ /usr/lib/instantclient && \
    rm instantclient-basiclite.zip && \
    ln -s /usr/lib/instantclient/libclntsh.so.21.1 /usr/lib/libclntsh.so && \
    ln -s /usr/lib/instantclient/libocci.so.21.1 /usr/lib/libocci.so && \
    ln -s /usr/lib/instantclient/libociicus.so /usr/lib/libociicus.so && \
    ln -s /usr/lib/instantclient/libnnz21.so /usr/lib/libnnz21.so && \
    ln -s /usr/lib/libnsl.so.2 /usr/lib/libnsl.so.1 && \
    ln -s /lib/libc.so.6 /usr/lib/libresolv.so.2 && \
    ln -s /lib64/ld-linux-x86-64.so.2 /usr/lib/ld-linux-x86-64.so.2

ENV LD_LIBRARY_PATH /usr/lib/instantclient

# Alpine's ssh doesn't use $PATH defined in /etc/environment, so we define `$PATH` in `~/.ssh/environment`
# The file path has been created earlier in the file by `mkdir -p` and we also have configured sshd so that it will
# allow environment variables to be sourced (see `sed` command related to `PermitUserEnvironment`)
RUN echo "PATH=${PATH}" >> ${JENKINS_AGENT_HOME}/.ssh/environment

RUN ssh-keyscan github.com >>${JENKINS_AGENT_HOME}/.ssh/known_hosts

RUN ln -s /usr/bin/python3 /usr/bin/python

COPY setup-sshd /usr/local/bin/setup-sshd

EXPOSE 22

ENTRYPOINT ["setup-sshd"]