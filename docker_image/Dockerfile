# Specify the image to use as a base.
# Make sure to adjust `DISTRO_CODENAME` if you change this.
ARG IMAGE_CMK_BASE
# hadolint ignore=DL3006
FROM ${IMAGE_CMK_BASE}
LABEL maintainer="feedback@checkmk.com"

# Ports:
# 5000 - Serves the Checkmk GUI
# 6557 - Serves Livestatus (if enabled via "omd config")
EXPOSE 5000 6557

# When all processes of the site are running everything should be fine
HEALTHCHECK --interval=1m --timeout=5s \
    CMD omd status || exit 1

# The following variables can be set during container init (docker run -e KEY=val)
ENV CMK_SITE_ID="cmk"
# Set this to "on" to enable livestatus via network
ENV CMK_LIVESTATUS_TCP=""
# A random password will be generated in case you don't set this
ENV CMK_PASSWORD=""

# Specify the FQDN of your relay mail server to sent mails to
ENV MAIL_RELAY_HOST=""

# Set a timezone
ENV TZ=""

# Add helper variable to better detect when running inside container.
# Used e.g. for omd update
ENV CMK_CONTAINERIZED="TRUE"

COPY docker-entrypoint.sh /
# Starts the entrypoint script and hands over CMD by default
ENTRYPOINT ["/docker-entrypoint.sh"]

# Make the list of required packages available to the following command
COPY needed-packages /needed-packages

# Install the tools we need for fetching the package and installation
# Then fetch the package and install it. This will make sure all Checkmk
# containers will share all dependencies, including this step.
#
# Also ensure that we apply the latest updates. The base image might not always
# be up-to-date, especially when they are pinned in our build environment.
#
# hadolint ignore=SC2046,DL3008
RUN set -e \
    && echo "exit 101" > /usr/sbin/policy-rc.d \
    && chmod +x /usr/sbin/policy-rc.d \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        postfix \
        libsasl2-modules \
        inetutils-syslogd \
        bsd-mailx \
        gnupg2 \
        openssh-client \
        iputils-ping \
        dpkg-sig \
        net-tools \
        git \
        $(cat needed-packages) \
    && apt-get clean \
    && rm /usr/sbin/policy-rc.d \
    && rm -rf /var/lib/apt/lists/* \
    && rm needed-packages

# Pure build time variable declarations (docker build --build-arg KEY=val)
ARG CMK_VERSION="2.5.0b1"
ARG CMK_EDITION
# Distro codename is used to find the corresponding .deb package
ARG DISTRO_CODENAME="jammy"

# Optionally copy an existing Checkmk debian package to the container. In case the file is
# available that is later used by the build procedure the file will not be downloaded.
COPY check-mk-${CMK_EDITION}-${CMK_VERSION}_0.${DISTRO_CODENAME}*.deb Check_MK-pubkey.gpg /

# Now install the Checkmk version specific things
# hadolint ignore=DL3003,DL3008,DL4006
RUN set -e \
    && mkdir -p /usr/share/man/man8 \
    && echo "exit 101" > /usr/sbin/policy-rc.d \
    && chmod +x /usr/sbin/policy-rc.d \
    && export DEBIAN_FRONTEND=noninteractive \
    && PKG_NAME="check-mk-${CMK_EDITION}-${CMK_VERSION}" \
    && PKG_FILE="${PKG_NAME}_0.${DISTRO_CODENAME}_$(dpkg --print-architecture).deb" \
    && if [ ! -e "/${PKG_FILE}" ]; then \
        echo "ERROR: Please provide ${PKG_FILE} by downloading it from https://download.checkmk.com/checkmk" \
        && return 1 ; \
       fi \
    && gpg -q --import "/Check_MK-pubkey.gpg" \
    && gpg --verify "${PKG_FILE}" \
    && dpkg -i "${PKG_FILE}" \
    && dpkg -i "$(ls /omd/versions/default/share/check_mk/agents/check-mk-agent_*-1_all.deb)" \
    && rm -f -- *.deb *.gpg \
    && apt-get clean \
    && rm /usr/sbin/policy-rc.d \
    && rm -rf /var/lib/apt/lists/*

LABEL \
    org.opencontainers.image.title="Checkmk" \
    org.opencontainers.image.version="${CMK_VERSION}" \
    org.opencontainers.image.description="Checkmk is a leading tool for Infrastructure & Application Monitoring" \
    org.opencontainers.image.vendor="Checkmk GmbH" \
    org.opencontainers.image.source="https://github.com/checkmk/checkmk" \
    org.opencontainers.image.url="https://checkmk.com/"
